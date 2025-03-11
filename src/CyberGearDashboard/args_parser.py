import sys
import errno
import argparse
from typing import List
import can

from CyberGearDashboard.constants import DEFAULT_CAN_BITRATE


def parse_args(args: List[str]) -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Connect to the CyberGear motor and launch dashboard",
    )

    parser.add_argument(
        "-m", "--motor-id", type=int, help="The ID of the motor on the CAN bus"
    )

    parser.add_argument(
        "-c",
        "--channel",
        help=r"The CAN interface channel. "
        r'For example with the serial interface the channel might be "/dev/ttyACM0".'
        r"With gs_usb (socketcan for mac/windows) the interface would likely be: 0."
        r'With the socketcan on Linux, valid channel examples include: "can0", "vcan0".'
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
