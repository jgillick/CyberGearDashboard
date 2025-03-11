import sys
import can
import traceback
from PySide6.QtCore import Qt, QSettings, QPoint, QSize
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from motor import CyberGearMotor, CyberMotorMessage

from dashboard.parameters import ParametersDockWidget, ConfigDockWidget
from dashboard.controller.controller_dock import MotorControllerDockWidget
from dashboard.motor_state import MotorStateWidget
from dashboard.watcher import MotorWatcher
from dashboard.charts import ChartLayout

CAN_BITRATE = 1000000


class AppWindow(QMainWindow):
    bus: can.Bus = None
    bus_notifier: can.Notifier
    motor: CyberGearMotor = None
    watcher: MotorWatcher
    settings: QSettings
    charts: ChartLayout

    def __init__(
        self,
        channel: str,
        interface: str,
        motor_id: int,
        verbose: bool = False,
        bitrate=CAN_BITRATE,
    ):
        super().__init__()
        self.settings = QSettings("jgillick", "PyCyberGearDashboard")

        # Connect to motor
        self.connect(channel, interface, motor_id, verbose, bitrate)

        # UI
        self.restore_window_pos()
        self.setWindowTitle("CyberGear Dashboard")
        self.build_layout()
        self.build_menubar()

    def build_layout(self):
        """Construct the layout"""
        layout = QVBoxLayout()

        self.charts = ChartLayout(self.motor, self.watcher)
        self.state_dock = MotorStateWidget(self.motor, charts=self.charts)
        self.parameter_dock = ParametersDockWidget(self.motor)
        self.config_dock = ConfigDockWidget(self.motor)
        self.controller_dock = MotorControllerDockWidget(self.motor)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.controller_dock)

        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.state_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.config_dock)
        self.tabifyDockWidget(self.config_dock, self.parameter_dock)

        layout.addLayout(self.charts)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def build_menubar(self):
        """Setup the app menubar"""
        menu = self.menuBar()

        view_menu = menu.addMenu("&View")
        view_menu.addAction(self.controller_dock.toggleViewAction())
        view_menu.addAction(self.state_dock.toggleViewAction())
        view_menu.addAction(self.parameter_dock.toggleViewAction())
        view_menu.addAction(self.config_dock.toggleViewAction())

    def send_bus_message(self, message: CyberMotorMessage):
        """Send a CyberMotor message on the CAN bus"""
        self.bus.send(
            can.Message(
                arbitration_id=message.arbitration_id,
                data=message.data,
                is_extended_id=message.is_extended_id,
            )
        )

    def connect(
        self, channel: str, interface: str, motor_id: int, verbose: bool, bitrate: int
    ) -> bool:
        """Connect to the CAN bus and the motor controller"""
        try:
            self.bus = can.interface.Bus(
                interface=interface,
                channel=channel,
                bitrate=bitrate,
            )

            # Create the motor controller
            self.motor = CyberGearMotor(
                motor_id, send_message=self.send_bus_message, verbose=verbose
            )
            self.bus_notifier = can.Notifier(self.bus, [self.motor.message_received])

            self.motor.enable()
            self.motor.stop()

            # Regularly poll the motor for updates
            self.watcher = MotorWatcher(self.motor)
            self.watcher.start()
        except Exception as e:
            alert = QMessageBox()
            alert.setText(f"Could not connect to the motor\n{e}")
            alert.exec()
            self.close()
        return True

    def save_window_pos(self):
        """Save the window position and size to settings"""
        self.settings.setValue("win.pos", self.pos())
        self.settings.setValue("win.size", self.size())

    def restore_window_pos(self):
        """Restore the window size and position from last session"""
        pos = self.settings.value("win.pos", defaultValue=QPoint(50, 50))
        size = self.settings.value("win.size", defaultValue=QSize(900, 600))
        self.move(pos)
        self.resize(size)

    def closeEvent(self, event: QCloseEvent):
        """Cleanup before we exit"""
        if self.watcher is not None:
            self.watcher.stop_watching()
        if self.motor is not None:
            self.motor.stop()
        if self.bus is not None:
            # Only save window position if we had connected to the bus
            self.save_window_pos()

            #  Close the bus
            self.bus.shutdown()
        event.accept()


def openDashboard(
    channel: str,
    interface: str,
    motor_id: int,
    verbose: bool = False,
    bitrate=CAN_BITRATE,
):
    app = QApplication(sys.argv)
    window = AppWindow(channel, interface, motor_id, verbose, bitrate)
    window.show()
    app.exec()
