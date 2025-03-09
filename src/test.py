import sys
import errno
import argparse
from typing import List
import can
import time

from motor.motor_controller import CyberGearMotor, RunMode

bus: can.Bus
motor: CyberGearMotor

DEFAULT_CAN_BITRATE = 1000000


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Connect to the CyberGear CAN bus interface",
    )

    parser.add_argument(
        "-m", "--motor-id", type=int, help="The ID of the motor on the CAN bus"
    )

    parser.add_argument(
        "-c",
        "--channel",
        help=r"Most backend interfaces require some sort of channel. For "
        r"example with the serial interface the channel might be"
        r'"/dev/ttyACM0". With the socketcan interface valid '
        r'channel examples include: "can0", "vcan0".'
        r"(more info: https://python-can.readthedocs.io/en/stable/interfaces.html)",
    )

    parser.add_argument(
        "-i",
        "--interface",
        dest="interface",
        help="""Specify the Python CAN interface to use (for example 'slcan'). See: https://python-can.readthedocs.io/en/stable/interfaces.html""",
        choices=sorted(can.VALID_INTERFACES),
    )

    parser.add_argument(
        "-b",
        "--bitrate",
        dest="bitrate",
        help="""CAN bus communication bitrate""",
        default=DEFAULT_CAN_BITRATE,
        type=int,
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="""Verbose output""",
        action=argparse.BooleanOptionalAction,
    )

    if not args:
        parser.print_help(sys.stderr)
        raise SystemExit(errno.EINVAL)
    parsed_args, unknown_args = parser.parse_known_args(args)

    return parsed_args


def main() -> None:
    global bus, motor
    args = parse_args(sys.argv[1:])

    # Connect to the bus
    print("Connecting...")
    bus = can.interface.Bus(
        interface=args.interface,
        channel=args.channel,
        bitrate=args.bitrate,
    )
    print("Connected!")

    # Create the motor controller
    motor = CyberGearMotor(args.motor_id, bus=bus, verbose=args.verbose)

    # Init motor
    motor.enable()
    motor.mode(RunMode.POSITION)
    motor.set_parameter("limit_spd", 10)

    # Loop back and forth
    while True:
        # motor.control_position(position=-6, velocity=1, torque=1, kp=10, kd=0.25)
        motor.set_parameter("loc_ref", -6)
        motor.get_position()
        time.sleep(2)

        # motor.control_position(position=5, velocity=1, torque=1, kp=10, kd=0.25)
        motor.set_parameter("loc_ref", 4)
        motor.get_position()
        time.sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if motor:
            motor.stop()
        if bus:
            bus.shutdown()
