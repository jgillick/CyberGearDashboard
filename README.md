# CyberGear Dashboard

A GUI dashboard for controlling the Xiaomi CyberGear micromotor.

<img src="./images//screenshot.png" width="500" alt="" />

## Getting started

Install the package from pip:

```bash
pip install CyberGearDashboard
```

Launch it with CAN bus connection details.

```bash
# Connect to motor ID 127 with the serial USB to CAN adapter device /dev/cu.usbmodem101
python -m CyberGearDashboard --motor 127 --channel /dev/cu.usbmodem101 --interface slcan
```

(see more about CAN devices, below)

## CAN bus connection

Unlike the stock Xiaomi CyberGear software, this tool can use any CAN adapter supported by the [Python CAN library](https://python-can.readthedocs.io/en/stable/interfaces.html). If you have trouble connecting, start by connecting to one of the [Python CAN tools](https://python-can.readthedocs.io/en/stable/scripts.html), in order to get the correct connection settings.

### Serial adapters

If you have a CAN to serial adapter, you'll likely be connecting with the [slcan](https://python-can.readthedocs.io/en/stable/interfaces/slcan.html) interface.

```bash
# Replace /dev/cu.usbmodem101 with the device port for the adapter on your computer
python -m CyberGearDashboard --channel /dev/cu.usbmodem101 --interface slcan --motor 127
```

If that doesn't work, try the [serial](https://python-can.readthedocs.io/en/stable/interfaces/serial.html) interface

```bash
# Replace /dev/ttyUSB0 with the device port for the adapter on your computer
python -m CyberGearDashboard --channel /dev/ttyUSB0 --interface serial --motor 127
```

### SocketCAN / candlelight / Geschwister Schneider

**Linux**

On Linux, you can connect using the [SocketCAN](https://python-can.readthedocs.io/en/stable/interfaces/slcan.html) interface. This will not work on Windows or Mac.

```bash
python -m CyberGearDashboard  --interface socketcan --channel can0 --motor 127
```

**Mac/Windows**

For Mac and Windows, you can connect to SocketCAN and candleLight devices with the [Geschwister Schneider](https://python-can.readthedocs.io/en/stable/interfaces/slcan.html) interface. NOTE: you might have to disconnect and reconnect the adapter between uses.

```bash
python -m CyberGearDashboard  --interface gs_usb --channel 0 --motor 127
```

### Troubleshooting

If the dashboard has trouble connecting to your device, try connecting via one of the [Python CAN tools](https://python-can.readthedocs.io/en/stable/scripts.html). Once you're able to connect with one of those tools, use the same arguments to open the dashboard.

For example

```shell
# If this connects without error
python -m can.viewer --interface gs_usb --channel 0

# Open the dashboard with the same connection values
python -m CyberGearDashboard --motor 127 --interface gs_usb --channel 0
```
