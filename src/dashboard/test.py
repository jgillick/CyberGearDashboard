import can
import time

# Constants
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


class ExCanIdInfo:
    """Represents a custom CAN ID structure with bit fields"""

    def __init__(self):
        self.id = 0  # 8 bits
        self.data = 0  # 16 bits
        self.mode = 0  # 5 bits
        self.res = 0  # 3 bits

    def to_int(self):
        """Convert the bit fields to a single 32-bit value"""
        return (
            (self.id & 0xFF)
            | ((self.data & 0xFFFF) << 8)
            | ((self.mode & 0x1F) << 24)
            | ((self.res & 0x7) << 29)
        )

    @classmethod
    def from_int(cls, value):
        """Create an ExCanIdInfo from a 32-bit value"""
        result = cls()
        result.id = value & 0xFF
        result.data = (value >> 8) & 0xFFFF
        result.mode = (value >> 24) & 0x1F
        result.res = (value >> 29) & 0x7
        return result


def float_to_uint(x, x_min, x_max, bits):
    """Convert a float to an unsigned integer with specified range and resolution"""
    span = x_max - x_min
    offset = x_min
    if x > x_max:
        x = x_max
    elif x < x_min:
        x = x_min
    return int((x - offset) * ((1 << bits) - 1) / span)


class MotorController:
    """Controls motor using CAN bus"""

    def __init__(
        self, can_interface="slcan", channel="/dev/cu.usbmodem1101", bitrate=1000000
    ):
        """Initialize the CAN bus connection"""
        self.bus = can.interface.Bus(
            channel=channel, interface=can_interface, bitrate=bitrate
        )

    def close(self):
        """Close the CAN bus connection"""
        self.bus.shutdown()

    def send_message(self, arbitration_id, data):
        """Send a CAN message with the given ID and data"""
        message = can.Message(
            arbitration_id=arbitration_id, data=data, is_extended_id=True
        )
        try:
            print(f"Send: {message}")
            self.bus.send(message)
            return True
        except can.CanError:
            print("Error sending CAN message")
            return False

    def receive_message(self, timeout=1.0):
        """Receive a CAN message"""
        message = self.bus.recv(timeout)
        if message:
            id_info = ExCanIdInfo.from_int(message.arbitration_id)
            return id_info, message.data
        return None, None

    def create_arbitration_id(self, mode, motor_id, data_value=0, res=0):
        """Create a CAN arbitration ID from the component fields"""
        id_info = ExCanIdInfo()
        id_info.mode = mode
        id_info.id = motor_id
        id_info.res = res
        id_info.data = data_value
        return id_info.to_int()

    def motor_enable(self, motor_id, master_id):
        """Enable the motor with the specified ID"""
        arbitration_id = self.create_arbitration_id(
            mode=3, motor_id=motor_id, data_value=master_id
        )
        # Second message with data value 0
        arbitration_id_2 = self.create_arbitration_id(
            mode=3, motor_id=motor_id, data_value=0
        )
        return self.send_message(arbitration_id_2, bytearray(8))

    def motor_controlmode(self, motor_id, torque, mech_position, speed, kp, kd):
        """Control the motor with the specified parameters"""
        torque_value = float_to_uint(torque, T_MIN, T_MAX, 16)
        arbitration_id = self.create_arbitration_id(
            mode=1, motor_id=motor_id, data_value=torque_value
        )

        data = bytearray(8)

        position_value = float_to_uint(mech_position, P_MIN, P_MAX, 16)
        data[0] = (position_value >> 8) & 0xFF
        data[1] = position_value & 0xFF

        speed_value = float_to_uint(speed, V_MIN, V_MAX, 16)
        data[2] = (speed_value >> 8) & 0xFF
        data[3] = speed_value & 0xFF

        kp_value = float_to_uint(kp, KP_MIN, KP_MAX, 16)
        data[4] = (kp_value >> 8) & 0xFF
        data[5] = kp_value & 0xFF

        kd_value = float_to_uint(kd, KD_MIN, KD_MAX, 16)
        data[6] = (kd_value >> 8) & 0xFF
        data[7] = kd_value & 0xFF

        return self.send_message(arbitration_id, data)

    def motor_reset(self, motor_id, master_id):
        """Reset the motor with the specified ID"""
        arbitration_id = self.create_arbitration_id(
            mode=4, motor_id=motor_id, data_value=master_id
        )
        return self.send_message(arbitration_id, bytearray(8))

    def listen_for_motor_responses(self, motor_id=None, timeout=5.0):
        """Listen for responses from motors"""
        print(f"Listening for CAN messages for {timeout} seconds...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            id_info, data = self.receive_message(timeout=0.1)
            if id_info:
                if motor_id is None or id_info.id == motor_id:
                    print(
                        f"Received from Motor ID: {id_info.id}, Mode: {id_info.mode}, Data: {id_info.data}"
                    )
                    print(f"Message data: {[hex(b) for b in data]}")


# Example usage
if __name__ == "__main__":
    try:
        motor_id = 254

        # Create motor controller (adjust interface and channel as needed)
        controller = MotorController(
            can_interface="slcan", channel="/dev/cu.usbmodem1101"
        )

        # Enable motor with ID 1
        controller.motor_enable(motor_id, 0x1234)

        # Control motor
        controller.motor_controlmode(motor_id, 5.0, 3.2, 10.5, 200.0, 2.5)

        # Listen for responses
        controller.listen_for_motor_responses(timeout=2.0)

        # Reset motor
        controller.motor_reset(motor_id, 0x1234)

    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        # Clean up
        if "controller" in locals():
            controller.close()
        print("CAN connection closed")
