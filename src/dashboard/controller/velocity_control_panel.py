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


class VelocityControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor
    velocity: SliderMotorInputWidget
    velocity_kp: SliderMotorInputWidget
    velocity_ki: SliderMotorInputWidget
    max_current: SliderMotorInputWidget

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.motor.enable()
        self.motor.mode(RunMode.VELOCITY)

        self.velocity.reset()
        self.velocity_kp.reset()
        self.velocity_ki.reset()
        self.max_current.reset()

    def unload(self):
        """The control panel is closing"""
        self.motor.stop()

    def execute(self):
        """Send the values to the motor"""
        self.max_current.send_to_motor()
        self.velocity_kp.send_to_motor()
        self.velocity_ki.send_to_motor()
        self.velocity.send_to_motor()

    def build_layout(self):
        self.velocity = SliderMotorInputWidget(
            motor=self.motor, label="Velocity (rad/s)", param_name="spd_ref"
        )
        self.velocity_kp = SliderMotorInputWidget(
            motor=self.motor, label="Velocity Kp", param_name="spd_kp", decimals=3
        )
        self.velocity_ki = SliderMotorInputWidget(
            motor=self.motor, label="Velocity Ki", param_name="spd_ki", decimals=3
        )
        self.max_current = SliderMotorInputWidget(
            motor=self.motor, label="Max current (A)", param_name="limit_cur"
        )

        button = QPushButton("Go")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout()
        layout.addWidget(self.velocity)
        layout.addWidget(self.velocity_kp)
        layout.addWidget(self.velocity_ki)
        layout.addWidget(self.max_current)
        layout.addWidget(button)
        layout.addItem(spacer)
        self.setLayout(layout)
