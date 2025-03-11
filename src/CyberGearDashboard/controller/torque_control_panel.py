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


class TorqueControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor
    form: QWidget
    enabled: QCheckBox
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
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.form.setEnabled(False)
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

    def set_enabled_changed(self, state: Qt.CheckState):
        """The enabled checkbox has changed"""
        is_enabled = True if state == Qt.CheckState.Checked else False
        self.form.setEnabled(is_enabled)
        if is_enabled:
            self.motor.enable()
            self.motor.mode(RunMode.TORQUE)
        else:
            self.motor.stop()

    def build_layout(self):
        self.enabled = QCheckBox("Enabled")
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.enabled.checkStateChanged.connect(self.set_enabled_changed)

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

        button = QPushButton("Send")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.current)
        form_layout.addWidget(self.current_kp)
        form_layout.addWidget(self.current_ki)
        form_layout.addWidget(self.current_filter_gain)
        form_layout.addWidget(button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.enabled)
        layout.addWidget(self.form)
        layout.addItem(spacer)
        self.setLayout(layout)
