from PySide6.QtWidgets import (
    QWidget,
)

from motor import CyberGearMotor
from dashboard.controller.slider_motor_control import SliderMotorControlWidget


class OperationControlPanel(QWidget):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def build_layout(self):
        position = SliderMotorControlWidget(self.motor, "loc_ref", "Position")
        self.setLayout(position)
