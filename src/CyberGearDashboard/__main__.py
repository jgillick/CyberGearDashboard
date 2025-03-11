import sys

from CyberGearDashboard import openDashboard
from CyberGearDashboard.args_parser import parse_args


def launch() -> None:
    """Launch the CyberGear Dashboard"""
    args = parse_args(sys.argv[1:])
    openDashboard(
        channel=args.channel,
        interface=args.interface,
        motor_id=args.motor_id,
        verbose=args.verbose,
        bitrate=args.bitrate,
    )


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        pass
