from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
)

from CyberGearDriver import CyberGearMotor, RunMode

from CyberGearDashboard.controller.abc_control_panel import AbstractModePanel
from .slider_input_widgets import SliderMotorInputWidget


class PositionControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor
    position: SliderMotorInputWidget
    position_kp: SliderMotorInputWidget
    velocity: SliderMotorInputWidget
    current: SliderMotorInputWidget
    form: QWidget
    enabled: QCheckBox

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.form.setEnabled(False)
        self.position.reset()
        self.position_kp.reset()
        self.velocity.reset()
        self.current.reset()

    def unload(self):
        """The control panel is closing"""
        self.motor.stop()

    def execute(self):
        """Send the values to the motor"""
        self.position_kp.send_to_motor()
        self.velocity.send_to_motor()
        self.position.send_to_motor()
        self.current.send_to_motor()

    def set_enabled_changed(self, state: Qt.CheckState):
        """The enabled checkbox has changed"""
        is_enabled = True if state == Qt.CheckState.Checked else False
        self.form.setEnabled(is_enabled)
        if is_enabled:
            self.motor.enable()
            self.motor.mode(RunMode.POSITION)
        else:
            self.motor.stop()

    def build_layout(self):
        self.enabled = QCheckBox("Enabled")
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.enabled.checkStateChanged.connect(self.set_enabled_changed)

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

        button = QPushButton("Send")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.position)
        form_layout.addWidget(self.position_kp)
        form_layout.addWidget(self.velocity)
        form_layout.addWidget(self.current)
        form_layout.addWidget(button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.enabled)
        layout.addWidget(self.form)
        layout.addItem(spacer)
        self.setLayout(layout)
