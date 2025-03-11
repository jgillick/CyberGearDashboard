from typing import List, cast
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from CyberGearDriver import CyberGearMotor

from CyberGearDashboard.controller.abc_control_panel import AbstractModePanel

from .idle_control_panel import IdleControlPanel
from .operation_control_panel import OperationControlPanel
from .position_control_panel import PositionControlPanel
from .velocity_control_panel import VelocityControlPanel
from .torque_control_panel import TorqueControlPanel

options = (
    ("Stopped", IdleControlPanel),
    ("Operation Control", OperationControlPanel),
    ("Position", PositionControlPanel),
    ("Velocity", VelocityControlPanel),
    ("Torque", TorqueControlPanel),
)


class MotorControllerDockWidget(QDockWidget):
    motor: CyberGearMotor
    stack: QStackedWidget
    screens: List[AbstractModePanel]

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def on_mode_change(self, index):
        """A mode has been selected in the combobox"""
        # Unload previous screen
        self.screens[self.stack.currentIndex()].unload()

        # Show screen
        self.stack.setCurrentIndex(index)

        # Load it in
        self.screens[index].load()

    def show_screen(self, index: int):
        """Show a particular screen in the stack"""
        self.stack.setCurrentIndex(index)

    def build_layout(self):
        self.setWindowTitle("Motor controller")

        self.stack = QStackedWidget()
        self.screens = []
        for name, WidgetCls in options:
            screen = WidgetCls(self.motor)
            self.stack.addWidget(screen)
            self.screens.append(screen)

        combobox = QComboBox()
        combobox.addItems([name for (name, widget) in options])
        combobox.currentIndexChanged.connect(self.on_mode_change)

        layout = QVBoxLayout()
        layout.addWidget(combobox)
        layout.addWidget(self.stack)

        root = QWidget()
        root.setLayout(layout)
        self.setWidget(root)
