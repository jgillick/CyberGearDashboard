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


class TorqueControlPanel(QWidget, metaclass=AbstractControlPanel):
    motor: CyberGearMotor
    form: QWidget
    send_button: QPushButton
    current: SliderMotorInputWidget
    current_kp: SliderMotorInputWidget
    current_ki: SliderMotorInputWidget
    current_filter_gain: SliderMotorInputWidget

    def __init__(self, motor: CyberGearMotor, parent=QDockWidget, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.motor = motor
        self.build_layout()
        parent.motor_enabled.connect(self.motor_is_enabled)

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.current.reset()
        self.current_kp.reset()
        self.current_ki.reset()
        self.current_filter_gain.reset()

    def unload(self):
        """The control panel is closing"""
        pass

    def execute(self):
        """Send the values to the motor"""
        self.current_filter_gain.send_to_motor()
        self.current_kp.send_to_motor()
        self.current_ki.send_to_motor()
        self.current.send_to_motor()
        self.motor.mode(RunMode.TORQUE)

    def motor_is_enabled(self, is_enabled: bool):
        """Enable the send button when the motor is enabled"""
        self.send_button.setEnabled(is_enabled)

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

        self.send_button = QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.current)
        form_layout.addWidget(self.current_kp)
        form_layout.addWidget(self.current_ki)
        form_layout.addWidget(self.current_filter_gain)
        form_layout.addWidget(self.send_button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addItem(spacer)
        self.setLayout(layout)
