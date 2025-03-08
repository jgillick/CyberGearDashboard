import can
import time
import struct
from enum import Enum
from typing import Union

from motor.utils import float_to_uint, uint_to_float
from motor.event_emitter import EventEmitter
from motor.parameters import (
    ParameterName,
    DataType,
    get_parameter_by_name,
    get_parameter_by_addr,
)

HOST_CAN_ID = 0
PAUSE_AFTER_SEND = 0.01

P_MIN = -12.5
P_MAX = 12.5
V_MIN = -30.0
V_MAX = 30.0
KP_MIN = 0.0
KP_MAX = 500.0
KD_MIN = 0.0
KD_MAX = 5.0
T_MIN = -12.0
T_MAX = 12.0
IQ_MIN = -27.0
IQ_MAX = 27.0


class ModeStatus(Enum):
    RESET = 0
    CALIBRATION = 1
    RUN = 2


class RunMode(Enum):
    STOPPED = -1
    OPERATION_CONTROL = 0
    POSITION = 1
    VELOCITY = 2
    TORQUE = 3


class Command(Enum):
    GET_DEVICE_ID = 0
    POSITION = 1
    STATE = 2
    ENABLE = 3
    STOP = 4
    SET_ZERO = 6
    CHANGE_CAN_ID = 7
    READ_PARAM = 17
    WRITE_PARAM = 18
    FAULT = 21


class MotorState:
    position: int
    velocity: int
    torque: int
    temperature: int
    has_fault: bool
    is_calibrated: bool
    hall_encoding_failure: bool
    magnetic_encoding_failure: bool
    over_temperature: bool
    over_current: bool
    under_voltage: bool
    most_status: ModeStatus


class CyberGearMotor(EventEmitter):
    """Controller and state manager for the CyberGear motor"""

    motor_id: int
    bus: can.Bus
    notifier: can.Notifier
    verbose: bool
    state: dict
    params: dict
    errors: dict

    def __init__(self, motor_id: int, bus: can.Bus, verbose: bool = False) -> None:
        self.verbose = verbose
        self.motor_id = motor_id
        self.params = {}
        self.state = {}
        self.errors = {}

        self.bus = bus
        self.notifier = can.Notifier(self.bus, [self._message_received])

        super().__init__()

    def disconnect(self):
        """Disconnect the motor from the bus"""
        self.notifier.stop()

    def enable(self):
        self._send(Command.ENABLE)

    def stop(self):
        self._send(Command.STOP, extended_data=HOST_CAN_ID)

    def mode(self, mode: RunMode):
        """Set the motor run mode"""
        if mode == RunMode.STOPPED:
            self.set_parameter("run_mode", RunMode.OPERATION_CONTROL.value)
            self.stop()
        else:
            self.set_parameter("run_mode", mode.value)

    def request_motor_state(self):
        """Request the current motor state"""
        self._send(Command.STATE)

    def request_motor_fault_status(self):
        """Request any active faults from the motor"""
        self._send(Command.FAULT)

    def control(
        self, position: float, velocity: float, torque: float, kp: float, kd: float
    ):
        """Move to a position in operation control mode."""
        data = bytearray(8)

        # Convert values
        position_value = float_to_uint(position, P_MIN, P_MAX, 16)
        velocity_value = float_to_uint(velocity, V_MIN, V_MAX, 16)
        kp_value = float_to_uint(kp, KP_MIN, KP_MAX, 16)
        kd_value = float_to_uint(kd, KD_MIN, KD_MAX, 16)

        # data[0] = position_value >> 8
        # data[1] = position_value & 0xFF

        # Velocity data (bytes 2-3)
        # data[2] = velocity_value >> 8
        # data[3] = velocity_value & 0xFF

        # Kp data (bytes 4-5)
        # data[4] = kp_value >> 8
        # data[5] = kp_value & 0xFF

        # Kd data (bytes 6-7)
        # data[6] = kd_value >> 8
        # data[7] = kd_value & 0xFF

        # Pack the data as big-endian 16-bit values ('>H')
        data = struct.pack(">HHHH", position_value, velocity_value, kp_value, kd_value)

        # Torque data
        torque_value = float_to_uint(torque, T_MIN, T_MAX, 16)

        # Send
        self._send(Command.POSITION, data=data, extended_data=torque_value)

    def get_position(self):
        """Get the current motor position"""
        self.request_parameter("mechPos")

    def set_parameter(self, param_name: ParameterName, value: Union[int, float]):
        """Send a parameter value to the motor"""
        param = get_parameter_by_name(param_name)
        if param is None:
            self._log(f"ERROR: Could not find parameter by name: '{param_name}'")
            return
        (addr, _name, data_type, range, permission) = param
        if permission != "rw":
            self._log(f"ERROR: Cannot write to parameter '{param_name}'")
            return

        # Clamp value to range
        if range is not None:
            (min, max) = range
            if value > max:
                self._log(f"WARN: Max value for {param_name} is {max}")
                value = max
            elif value < min:
                self._log(f"WARN: Min value for {param_name} is {min}")
                value = min

        # Create message data
        data = bytearray(8)
        data[0] = addr & 0x00FF
        data[1] = addr >> 8

        # Encode types
        if data_type == DataType.UINT8:
            data[4] = value
        elif data_type == DataType.INT16:
            data[4:6] = struct.pack("<h", value)
        elif data_type == DataType.UINT16:
            data[4:6] = struct.pack("<H", value)
        elif data_type == DataType.INT32:
            data[4:8] = struct.pack("<i", value)
        elif data_type == DataType.UINT32:
            data[4:8] = struct.pack("<I", value)
        elif data_type == DataType.FLOAT:
            data[4:8] = struct.pack("<f", float(value))
        else:
            self._log(f"ERROR: No type processing for '{param_name}' ({data_type})")
            return

        self._send(Command.WRITE_PARAM, data=data)

    def request_parameter(self, param_name: ParameterName):
        """Send a request to receive a motor parameter"""
        param = get_parameter_by_name(param_name)
        if param is None:
            self._log(f"ERROR: Could not find parameter by name: '{param_name}'")
            return
        addr = param[0]

        # Copy the parameter value (as bytes) into the first 2 bytes of data
        data = bytearray(8)
        data[0:2] = addr.to_bytes(2, byteorder="little")

        # Send
        self._log(f"Send: {Command.READ_PARAM.name} - {param_name}")
        self._send(Command.READ_PARAM, data=data, log=False)

    def _log(self, message: str):
        """If verbose is True, output some logging"""
        if self.verbose:
            print(message)

    def _send(
        self,
        command: Command,
        data: bytearray = bytearray(8),
        extended_data: int = 0,
        log: bool = True,
    ):
        """Send a message to the motor."""

        # Encode ID
        id = command.value << 24 | extended_data << 8 | self.motor_id

        # Create message
        msg = can.Message(
            arbitration_id=id,
            data=data,
            is_extended_id=True,
        )

        # Send
        self.bus.send(msg)
        if log:
            self._log(f"Send: {command.name}")
        time.sleep(PAUSE_AFTER_SEND)

    def _message_received(self, msg: can.Message):
        """A message was received on the CAN bus"""

        # Parse values out of arbitration ID
        destination_id = msg.arbitration_id & 0xFF
        from_id = (msg.arbitration_id >> 8) & 0xFF

        command_num = (msg.arbitration_id >> 24) & 0x1F
        command = Command(command_num)

        extended_data = (msg.arbitration_id >> 8) & 0xFFFF
        ext_data_bytes = extended_data.to_bytes(16, "little")

        # Filter out messages not from our motor
        if destination_id != HOST_CAN_ID:
            return
        if from_id != self.motor_id:
            return

        if command == Command.STATE:
            self._process_received_state(msg.data, ext_data_bytes)
        elif command == Command.READ_PARAM:
            self._processed_received_param(msg.data)
        elif command == Command.FAULT:
            self._process_fault_data(msg.data)

    def _process_received_state(self, data: bytearray, ext_data: bytearray):
        """Convert the motor feedback response into the current motor state"""
        pos_data = data[1] | data[0] << 8
        vel_data = data[3] | data[2] << 8
        torque_data = data[5] | data[4] << 8

        raw_temp = data[7] | data[6] << 8
        motor_id = int.from_bytes(ext_data[0:7], byteorder="little")

        self.state["temperature"] = raw_temp / 10 if raw_temp else 0
        self.state["position"] = uint_to_float(pos_data, P_MIN, P_MAX)
        self.state["velocity"] = uint_to_float(vel_data, V_MIN, V_MAX)
        self.state["torque"] = uint_to_float(torque_data, T_MIN, T_MAX)

        # mode_status = int.from_bytes(ext_data[14:15], byteorder="little")
        # self.state["mode_status"] = ModeStatus(mode_status)

        # Errors and warnings
        errors = self.errors.copy()
        errors["Encoder not calibrated"] = bool(ext_data[13])
        errors["Hall encoder failure"] = bool(ext_data[12])
        errors["Magnetic encoder failure"] = bool(ext_data[11])
        errors["Over_temperature"] = bool(ext_data[10])
        errors["Over current"] = bool(ext_data[9])
        errors["Under voltage"] = bool(ext_data[8])

        # Filter out falsy vales
        self.errors = {k: v for k, v in errors.items() if v}
        if len(self.errors):
            self.emit("fault")

        self.emit("state_changed")

        # Log state
        self._log(f" > Motor ID: {motor_id}")
        self._log(f" > Position: {self.state['position']}")
        self._log(f" > Velocity: {self.state['velocity']}")
        self._log(f" > Torque: {self.state['torque']}")

        # Log errors
        for err in self.errors:
            self._log(f" ! {err}")

    def _processed_received_param(self, data: bytearray):
        """A requested motor prarameter has been received"""
        log_name = ""
        try:
            # Get the property config by address
            addr = data[1] << 8 | data[0]
            parameter = get_parameter_by_addr(addr)
            if parameter is None:
                self._log(f"ERROR: Unknown parameter address: '{hex(addr)}'")
                return
            (_addr, param_name, data_type, range, _permission) = parameter
            log_name = param_name

            # Read the value
            value = 0
            if data_type == DataType.UINT8:
                value = data[4]
            elif data_type == DataType.INT16:
                value = struct.unpack("<h", data[4:6])[0]
            elif data_type == DataType.UINT16:
                value = struct.unpack("<H", data[4:6])[0]
            elif data_type == DataType.INT32:
                value = struct.unpack("<i", data[4:8])[0]
            elif data_type == DataType.UINT32:
                value = struct.unpack("<I", data[4:8])[0]
            elif data_type == DataType.FLOAT:
                value = struct.unpack("<f", data[4:8])[0]
            else:
                self._log(f"ERROR: No type processing for '{param_name}' ({data_type})")
                return

            self._log(f" > {param_name} = {value}")
            self.params[param_name] = value
            self.emit("param_changed", param_name, value)
        except Exception as e:
            self._log(f"ERROR: Could not process parameter value ({log_name}): {e}")

    def _process_fault_data(self, data: bytearray):
        """Process the fault feedback message"""
        # Extract fault value (bytes 0-3)
        fault_value = int.from_bytes(data[0:4], byteorder="little")

        # Extract individual fault bits
        errors = self.errors.copy()
        errors["Phase A over current"] = bool(fault_value & (1 << 16))
        errors["Phase B over current"] = bool(fault_value & (1 << 4))
        errors["Phase C over current"] = bool(fault_value & (1 << 5))
        errors["Overload"] = (fault_value >> 8) & 0xFF  # Bits 15-8
        errors["Encoder not calibrated"] = bool(fault_value & (1 << 7))
        errors["Over voltage"] = bool(fault_value & (1 << 3))
        errors["Under voltage"] = bool(fault_value & (1 << 2))
        errors["Driver chip"] = bool(fault_value & (1 << 1))
        errors["Over temperature"] = bool(fault_value & (1 << 0))

        # Filter out falsy values
        self.errors = {k: v for k, v in errors.items() if v}
        if fault_value:
            self.emit("fault")

        # Log errors
        for err in self.errors:
            self._log(f" ! {err}")
