from PySide6.QtWidgets import (
    QComboBox,
    QDockWidget,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from motor import CyberGearMotor, RunMode
from dashboard.controller.op_control import OperationControlPanel


class EmptyControlWidget(QWidget):
    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)


options = (
    ("Stopped", RunMode.STOPPED, EmptyControlWidget),
    ("Operation Control", RunMode.OPERATION_CONTROL, OperationControlPanel),
    ("Position", RunMode.POSITION, EmptyControlWidget),
    ("Velocity", RunMode.VELOCITY, EmptyControlWidget),
    ("Torque", RunMode.VELOCITY, EmptyControlWidget),
    ("Zero Position", None, EmptyControlWidget),
)


class MotorControllerDockWidget(QDockWidget):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def on_change(self, text):
        for name, mode, widget in options:
            if name == text:
                if mode != RunMode.STOPPED:
                    self.motor.enable()
                self.motor.mode(mode)
                break

    def build_layout(self):
        self.setWindowTitle("Motor controller")

        combobox = QComboBox()
        combobox.addItems([name for (name, action, widget) in options])
        combobox.currentTextChanged.connect(self.on_change)

        stack = QStackedWidget()
        for name, action, WidgetCls in options:
            screen = WidgetCls(self.motor)
            stack.addWidget(screen)
        combobox.activated.connect(stack.setCurrentIndex)

        layout = QVBoxLayout()
        layout.addWidget(combobox)
        layout.addWidget(stack)

        root = QWidget()
        root.setLayout(layout)
        self.setWidget(root)
