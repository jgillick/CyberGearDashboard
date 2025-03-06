import sys
import can
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from motor import CyberGearMotor

from dashboard.parameter_table import ParameterTable
from dashboard.mode_selector import ModeSelector
from dashboard.state_table import StateTable

CAN_BITRATE = 1000000


class MainWindow(QMainWindow):
    bus: can.Bus
    motor: CyberGearMotor

    def __init__(
        self, channel: str, interface: str, motor_id: int, verbose: bool = False
    ):
        super().__init__()

        connected = self.connect(channel, interface, motor_id, verbose)

        self.setWindowTitle("CyberGear Dashboard")

        widget = QWidget()
        if connected:
            layout = self.build_layout()
            widget.setLayout(layout)

        self.setCentralWidget(widget)

    def build_layout(self):
        """Construct the layout"""
        layout = QVBoxLayout()

        mode = ModeSelector(self.motor)
        state = StateTable(self.motor)
        params = ParameterTable(self.motor)

        layout.addLayout(mode)
        layout.addLayout(state)
        layout.addLayout(params)
        return layout

    def connect(
        self, channel: str, interface: str, motor_id: int, verbose: bool
    ) -> bool:
        """Connect to the CAN bus and the motor controller"""
        try:
            self.bus = can.interface.Bus(
                interface=interface,
                channel=channel,
                bitrate=CAN_BITRATE,
            )
            print("Connected!")

            # Create the motor controller
            self.motor = CyberGearMotor(motor_id, bus=self.bus, verbose=verbose)
        except Exception as e:
            alert = QMessageBox()
            alert.setText(f"Could not connect to the motor\n{e}")
            alert.exec()
        return True

    def closeEvent(self, event: QCloseEvent):
        """Cleanup before we exit"""
        if self.motor:
            self.motor.stop()
            self.motor.disconnect()
        if self.bus:
            self.bus.shutdown()
        event.accept()


def openDashboard(channel: str, interface: str, motor_id: int, verbose: bool = False):
    app = QApplication(sys.argv)
    window = MainWindow(channel, interface, motor_id, verbose)
    window.show()
    app.exec()
