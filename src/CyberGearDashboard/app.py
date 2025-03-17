import sys
import can
from PySide6.QtCore import Qt, QSettings, QPoint, QSize
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QMessageBox,
)

from CyberGearDriver import CyberGearMotor, CyberMotorMessage

from CyberGearDashboard.constants import DEFAULT_CAN_BITRATE
from CyberGearDashboard.parameters import ParametersTableDock
from CyberGearDashboard.controller.controller_dock import MotorControllerDockWidget
from CyberGearDashboard.motor_state import MotorStateWidget
from CyberGearDashboard.watcher import MotorWatcher
from CyberGearDashboard.charts import ChartLayout


class AppWindow(QMainWindow):
    bus: can.Bus = None
    motor: CyberGearMotor = None
    did_load: bool = False
    bus_notifier: can.Notifier
    watcher: MotorWatcher
    settings: QSettings
    charts: ChartLayout

    def __init__(
        self,
        channel: str,
        interface: str,
        motor_id: int,
        verbose: bool = False,
        bitrate=DEFAULT_CAN_BITRATE,
    ):
        super().__init__()
        self.settings = QSettings("jgillick", "CyberGearDriverDashboard")

        # Connect to motor
        self.connect(channel, interface, motor_id, verbose, bitrate)
        self.did_load = True

        # UI
        self.restore_window_pos()
        self.setWindowTitle("CyberGear Dashboard")
        self.build_layout()

    def build_layout(self):
        """Construct the layout"""
        layout = QVBoxLayout()

        charts = ChartLayout(self.motor, self.watcher)
        state_dock = MotorStateWidget(self.motor, charts=charts)
        parameter_dock = ParametersTableDock(self.motor)
        controller_dock = MotorControllerDockWidget(self.motor)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, controller_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, state_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, parameter_dock)

        menu = self.menuBar()
        view_menu = menu.addMenu("&View")
        view_menu.addAction(controller_dock.toggleViewAction())
        view_menu.addAction(state_dock.toggleViewAction())
        view_menu.addAction(parameter_dock.toggleViewAction())

        layout.addLayout(charts)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setFocus()

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
        if self.did_load:
            # Save window position
            self.save_window_pos()
        if self.watcher is not None:
            self.watcher.stop_watching()
        if self.motor is not None:
            self.motor.stop()
        if self.bus_notifier is not None:
            self.bus_notifier.stop()
        if self.bus is not None:
            self.bus.shutdown()
        event.accept()


def openDashboard(
    channel: str,
    interface: str,
    motor_id: int,
    verbose: bool = False,
    bitrate=DEFAULT_CAN_BITRATE,
):
    app = QApplication(sys.argv)
    window = AppWindow(channel, interface, motor_id, verbose, bitrate)
    window.show()
    app.exec()
