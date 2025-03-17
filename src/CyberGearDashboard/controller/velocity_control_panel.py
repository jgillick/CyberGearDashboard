from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDockWidget,
)

from CyberGearDriver import CyberGearMotor, RunMode

from .abstract_classes import AbstractControlPanel
from .slider_input_widgets import SliderMotorInputWidget


class VelocityControlPanel(QWidget, metaclass=AbstractControlPanel):
    motor: CyberGearMotor
    velocity: SliderMotorInputWidget
    velocity_kp: SliderMotorInputWidget
    velocity_ki: SliderMotorInputWidget
    max_current: SliderMotorInputWidget
    form: QWidget
    send_button: QPushButton

    def __init__(self, motor: CyberGearMotor, parent=QDockWidget, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.motor = motor
        self.build_layout()
        parent.motor_enabled.connect(self.motor_is_enabled)

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.velocity.reset()
        self.velocity_kp.reset()
        self.velocity_ki.reset()
        self.max_current.reset()

    def unload(self):
        """The control panel is closing"""
        pass

    def execute(self):
        """Send the values to the motor"""
        self.max_current.send_to_motor()
        self.velocity_kp.send_to_motor()
        self.velocity_ki.send_to_motor()
        self.velocity.send_to_motor()
        self.motor.mode(RunMode.VELOCITY)

    def motor_is_enabled(self, is_enabled: bool):
        """Enable the send button when the motor is enabled"""
        self.send_button.setEnabled(is_enabled)

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

        self.send_button = QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.velocity)
        form_layout.addWidget(self.velocity_kp)
        form_layout.addWidget(self.velocity_ki)
        form_layout.addWidget(self.max_current)
        form_layout.addWidget(self.send_button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addItem(spacer)
        self.setLayout(layout)
