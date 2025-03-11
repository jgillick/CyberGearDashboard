from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QCheckBox,
)

from CyberGearDriver import (
    CyberGearMotor,
    RunMode,
    P_MIN,
    P_MAX,
    V_MIN,
    V_MAX,
    KP_MIN,
    KP_MAX,
    KD_MIN,
    KD_MAX,
    T_MIN,
    T_MAX,
)

from CyberGearDashboard.controller.abc_control_panel import AbstractModePanel
from .slider_input_widgets import SliderInputWidget


class OperationControlPanel(QWidget, metaclass=AbstractModePanel):
    motor: CyberGearMotor

    form: QWidget
    position: SliderInputWidget
    torque: SliderInputWidget
    velocity: SliderInputWidget
    kp: SliderInputWidget
    kd: SliderInputWidget

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.form.setEnabled(False)
        self.position.set_value(0.0)
        self.torque.set_value(0.0)
        self.velocity.set_value(0.0)

    def unload(self):
        """The control panel is closing, stop the motor"""
        self.motor.stop()

    def execute(self):
        """Send the values to the motor"""
        self.motor.control(
            self.position.value,
            self.velocity.value,
            self.torque.value,
            self.kp.value,
            self.kd.value,
        )

    def set_enabled_changed(self, state: Qt.CheckState):
        is_enabled = True if state == Qt.CheckState.Checked else False
        self.form.setEnabled(is_enabled)
        if is_enabled:
            self.motor.enable()
            self.motor.mode(RunMode.OPERATION_CONTROL)
        else:
            self.motor.stop()

    def build_layout(self):
        self.enabled = QCheckBox("Enabled")
        self.enabled.setCheckState(Qt.CheckState.Unchecked)
        self.enabled.checkStateChanged.connect(self.set_enabled_changed)

        self.position = SliderInputWidget(
            label="Position (rad)", value=1.0, range=(P_MIN, P_MAX)
        )
        self.torque = SliderInputWidget(
            label="Torque (Nm)", value=0.5, range=(T_MIN, T_MAX)
        )
        self.velocity = SliderInputWidget(
            label="Velocity (rad/s)", value=1, range=(V_MIN, V_MAX)
        )
        self.kp = SliderInputWidget(
            label="Kp", value=0.1, range=(KP_MIN, KP_MAX), decimals=3
        )
        self.kd = SliderInputWidget(
            label="Kd", value=0.1, range=(KD_MIN, KD_MAX), decimals=3
        )

        button = QPushButton("Send")
        button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.position)
        form_layout.addWidget(self.torque)
        form_layout.addWidget(self.velocity)
        form_layout.addWidget(self.kp)
        form_layout.addWidget(self.kd)
        form_layout.addWidget(button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.enabled)
        layout.addWidget(self.form)
        layout.addItem(spacer)

        self.setLayout(layout)
