import sys
import can
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from motor import CyberGearMotor

from dashboard.parameters import ParameterDockWidget
from dashboard.controller import MotorControllerDockWidget
from dashboard.motor_state import MotorStateWidget

CAN_BITRATE = 1000000


class MainWindow(QMainWindow):
    bus: can.Bus
    motor: CyberGearMotor

    def __init__(
        self, channel: str, interface: str, motor_id: int, verbose: bool = False
    ):
        super().__init__()

        # Connect to motor
        self.connect(channel, interface, motor_id, verbose)

        # UI
        self.resize(800, 600)
        self.setWindowTitle("CyberGear Dashboard")
        self.build_layout()
        self.build_menubar()

    def build_layout(self):
        """Construct the layout"""
        layout = QVBoxLayout()

        self.state_dock = MotorStateWidget(self.motor, self)
        self.parameter_dock = ParameterDockWidget(self.motor, self)
        self.controller_dock = MotorControllerDockWidget(self.motor, self)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.state_dock)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.parameter_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.controller_dock)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def build_menubar(self):
        """Setup the app menubar"""
        view_motor_state = QAction("Motor state", self)
        view_motor_state.setCheckable(True)

        view_parameters = QAction("Parameters", self)
        view_parameters.setCheckable(True)

        view_control = QAction("Control", self)
        view_control.setCheckable(True)

        menu = self.menuBar()

        view_menu = menu.addMenu("&View")
        view_menu.addAction(view_motor_state)
        view_menu.addAction(view_parameters)
        view_menu.addAction(view_control)

        # Connect menus to dock widgets
        view_motor_state.toggled.connect(self.state_dock.setVisible)
        self.state_dock.visibilityChanged.connect(view_motor_state.setChecked)

        self.parameter_dock.visibilityChanged.connect(view_parameters.setChecked)
        view_parameters.toggled.connect(self.parameter_dock.setVisible)

        view_control.toggled.connect(self.controller_dock.setVisible)
        self.controller_dock.visibilityChanged.connect(view_control.setChecked)

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
            self.close()
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
