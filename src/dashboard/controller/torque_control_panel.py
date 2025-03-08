from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
)

from motor import CyberGearMotor, RunMode

from dashboard.controller.abc_control_panel import AbstractModePanel
from .slider_input_widgets import SliderMotorInputWidget


class TorqueControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor
    current: SliderMotorInputWidget
    current_kp: SliderMotorInputWidget
    current_ki: SliderMotorInputWidget
    current_filter_gain: SliderMotorInputWidget

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.motor.enable()
        self.motor.mode(RunMode.TORQUE)

        self.current.reset()
        self.current_kp.reset()
        self.current_ki.reset()
        self.current_filter_gain.reset()

    def unload(self):
        """The control panel is closing"""
        self.motor.stop()

    def execute(self):
        """Send the values to the motor"""
        self.current_filter_gain.send_to_motor()
        self.current_kp.send_to_motor()
        self.current_ki.send_to_motor()
        self.current.send_to_motor()

    def build_layout(self):
        self.current = SliderMotorInputWidget(
            motor=self.motor, label="Current (A)", param_name="iq_ref"
        )
        self.current_kp = SliderMotorInputWidget(
            motor=self.motor, label="Current Kp", param_name="cur_kp", decimals=3
        )
        self.current_ki = SliderMotorInputWidget(
            motor=self.motor, label="Current Ki", param_name="cur_ki", decimals=3
        )
        self.current_filter_gain = SliderMotorInputWidget(
            motor=self.motor, label="Current filter gain", param_name="cur_filt_gain"
        )

        button = QPushButton("Go")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout()
        layout.addWidget(self.current)
        layout.addWidget(self.current_kp)
        layout.addWidget(self.current_ki)
        layout.addWidget(self.current_filter_gain)
        layout.addWidget(button)
        layout.addItem(spacer)
        self.setLayout(layout)
