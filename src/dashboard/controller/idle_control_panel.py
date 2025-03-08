from PySide6.QtWidgets import QWidget

from motor import (
    CyberGearMotor,
)

from dashboard.controller.abc_control_panel import AbstractModePanel
from .slider_input_widgets import SliderInputWidget


class IdleControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.motor.stop()

    def unload(self):
        """The control panel is closing"""
        pass
