import can
import time
import sys


class ExCanIdInfo:
    """Represents a custom CAN ID structure with bit fields"""

    def __init__(self):
        self.id = 0  # 8 bits - motor ID
        self.data = 0  # 16 bits - data field in arbitration ID
        self.mode = 0  # 5 bits - mode
        self.res = 0  # 3 bits - reserved

    @classmethod
    def from_int(cls, value):
        """Create an ExCanIdInfo from a 32-bit value"""
        result = cls()
        result.id = value & 0xFF
        result.data = (value >> 8) & 0xFFFF
        result.mode = (value >> 24) & 0x1F
        result.res = (value >> 29) & 0x7
        return result


def can_listener(interface="slcan", channel="COM3", bitrate=1000000, timeout=None):
    """
    Listen for CAN messages and print details

    Parameters:
    - interface: CAN interface type (default 'slcan')
    - channel: CAN channel (default 'COM3', common for slcan on Windows)
    - bitrate: CAN bus bitrate
    - timeout: How long to listen in seconds (None = indefinitely)
    """
    try:
        # Set up CAN bus
        bus = can.interface.Bus(channel=channel, bustype=interface, bitrate=bitrate)
        print(f"Listening on {interface} {channel}...")

        start_time = time.time()
        msg_count = 0

        # Main loop
        while timeout is None or time.time() - start_time < timeout:
            message = bus.recv(1)  # 1 second timeout for each receive attempt

            if message:
                msg_count += 1
                # Extract the custom ID structure
                id_info = ExCanIdInfo.from_int(message.arbitration_id)

                # Format data nicely
                data_hex = " ".join(f"{b:02X}" for b in message.data)

                # Print the decoded information
                print(f"Message #{msg_count}:")
                print(f"  Timestamp: {message.timestamp:.6f}")
                print(f"  Motor ID: {id_info.id}")
                print(f"  Mode: {id_info.mode}")
                print(f"  Arbitration ID data field: {id_info.data}")
                print(f"  Reserved bits: {id_info.res}")
                print(f"  Data: [{data_hex}]")
                print("")

                # Flush output to ensure real-time display
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\nListener stopped by user")
    except can.CanError as e:
        print(f"CAN Error: {e}")
    finally:
        if "bus" in locals():
            bus.shutdown()
            print("CAN interface closed")


if __name__ == "__main__":
    import argparse

    # Create command line argument parser
    parser = argparse.ArgumentParser(
        description="CAN bus listener for motor control messages"
    )
    parser.add_argument(
        "--interface",
        type=str,
        default="slcan",
        help="CAN interface type (default: slcan)",
    )
    parser.add_argument(
        "--channel", type=str, default="COM3", help="CAN channel (default: COM3)"
    )
    parser.add_argument(
        "--bitrate", type=int, default=1000000, help="CAN bitrate (default: 1000000)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=None,
        help="Listening timeout in seconds (default: None)",
    )

    args = parser.parse_args()

    # Run the listener with provided arguments
    can_listener(
        interface=args.interface,
        channel=args.channel,
        bitrate=args.bitrate,
        timeout=args.timeout,
    )
