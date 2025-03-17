from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
    QDockWidget,
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

from .abstract_classes import AbstractControlPanel
from .slider_input_widgets import SliderInputWidget


class OperationControlPanel(QWidget, metaclass=AbstractControlPanel):
    motor: CyberGearMotor

    form: QWidget
    send_button: QPushButton
    position: SliderInputWidget
    torque: SliderInputWidget
    velocity: SliderInputWidget
    kp: SliderInputWidget
    kd: SliderInputWidget

    def __init__(self, motor: CyberGearMotor, parent=QDockWidget, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.motor = motor
        self.build_layout()
        parent.motor_enabled.connect(self.motor_is_enabled)

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.position.set_value(0.0)
        self.torque.set_value(0.0)
        self.velocity.set_value(0.0)

    def unload(self):
        """The control panel is closing, stop the motor"""
        pass

    def execute(self):
        """Send the values to the motor"""
        self.motor.mode(RunMode.OPERATION_CONTROL)
        self.motor.control(
            self.position.value,
            self.velocity.value,
            self.torque.value,
            self.kp.value,
            self.kd.value,
        )

    def motor_is_enabled(self, is_enabled: bool):
        """Enable the send button when the motor is enabled"""
        self.send_button.setEnabled(is_enabled)

    def build_layout(self):
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

        self.send_button = QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.execute)

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.position)
        form_layout.addWidget(self.torque)
        form_layout.addWidget(self.velocity)
        form_layout.addWidget(self.kp)
        form_layout.addWidget(self.kd)
        form_layout.addWidget(self.send_button)

        self.form = QWidget()
        self.form.setLayout(form_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.form)
        layout.addItem(spacer)

        self.setLayout(layout)
