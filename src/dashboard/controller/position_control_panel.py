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


class PositionControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor
    position: SliderMotorInputWidget
    position_kp: SliderMotorInputWidget
    velocity: SliderMotorInputWidget
    current: SliderMotorInputWidget

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.motor.enable()
        self.position.reset()
        self.position_kp.reset()
        self.velocity.reset()
        self.current.reset()
        self.motor.mode(RunMode.POSITION)

    def unload(self):
        """The control panel is closing"""
        self.motor.stop()

    def execute(self):
        """Send the values to the motor"""
        self.position_kp.send_to_motor()
        self.velocity.send_to_motor()
        self.position.send_to_motor()
        self.current.send_to_motor()

    def build_layout(self):
        self.position = SliderMotorInputWidget(
            motor=self.motor, label="Position (rad)", param_name="loc_ref"
        )
        self.position_kp = SliderMotorInputWidget(
            motor=self.motor, label="Position Kp", param_name="loc_kp", decimals=3
        )
        self.velocity = SliderMotorInputWidget(
            motor=self.motor, label="Velocity (rad/s)", param_name="limit_spd"
        )
        self.current = SliderMotorInputWidget(
            motor=self.motor, label="Limit Current (A)", param_name="limit_spd"
        )

        button = QPushButton("Go")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout()
        layout.addWidget(self.position)
        layout.addWidget(self.position_kp)
        layout.addWidget(self.velocity)
        layout.addWidget(self.current)
        layout.addWidget(button)
        layout.addItem(spacer)
        self.setLayout(layout)
