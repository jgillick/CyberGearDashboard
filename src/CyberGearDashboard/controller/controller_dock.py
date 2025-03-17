from typing import List
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
    QCheckBox,
)

from CyberGearDriver import CyberGearMotor

from CyberGearDashboard.controller.abstract_classes import AbstractControlPanel

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
    screens: List[AbstractControlPanel]
    motor_enabled = Signal(bool)

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def on_mode_change(self, index):
        """A mode has been selected in the combobox"""
        # Disable the motor
        self.enable_checkbox.setChecked(False)
        can_enable_motor = index != 0
        self.enable_checkbox.setEnabled(can_enable_motor)

        # Unload previous screen
        self.screens[self.stack.currentIndex()].unload()

        # Show screen
        self.stack.setCurrentIndex(index)

        # Load it in
        self.screens[index].load()

    def show_screen(self, index: int):
        """Show a particular screen in the stack"""
        self.stack.setCurrentIndex(index)

    def enable_motor(self, state: Qt.CheckState):
        is_enabled = True if state == Qt.CheckState.Checked else False
        if is_enabled:
            self.motor.enable()
        else:
            self.motor.stop()
        self.motor_enabled.emit(is_enabled)

    def build_layout(self):
        self.setWindowTitle("Motor controller")

        self.enable_checkbox = QCheckBox("Enable motor")
        self.enable_checkbox.checkStateChanged.connect(self.enable_motor)
        self.enable_checkbox.setCheckState(Qt.CheckState.Unchecked)
        self.enable_checkbox.setDisabled(True)

        enable_layout = QVBoxLayout()
        enable_layout.setContentsMargins(0, 5, 0, 10)
        enable_layout.addWidget(self.enable_checkbox)

        self.stack = QStackedWidget()
        self.screens = []
        for name, WidgetCls in options:
            screen = WidgetCls(self.motor, parent=self)
            self.stack.addWidget(screen)
            self.screens.append(screen)

        combobox = QComboBox()
        combobox.addItems([name for (name, widget) in options])
        combobox.currentIndexChanged.connect(self.on_mode_change)

        layout = QVBoxLayout()
        layout.addLayout(enable_layout)
        layout.addWidget(combobox)
        layout.addWidget(self.stack)

        root = QWidget()
        root.setLayout(layout)
        self.setWidget(root)
        self.enable_checkbox.clearFocus()
