from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QWidget,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QPushButton,
    QSizePolicy,
    QLabel,
    QVBoxLayout,
    QFrame,
)

from CyberGearDriver import CyberGearMotor

from CyberGearDashboard.controller.abstract_classes import AbstractControlPanel


class IdleControlPanel(QWidget, metaclass=AbstractControlPanel):
    motor: CyberGearMotor
    zero_btn: QPushButton

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

        timer = QTimer(self)
        timer.timeout.connect(self.check_motor_state)
        timer.start(500)

    def load(self):
        """Reset the screen and put the motor in the correct mode"""
        self.motor.stop()

    def unload(self):
        """The control panel is closing"""
        pass

    def check_motor_state(self):
        """Check the motor state for changes"""
        # Enable the zero button if the motor is not at zero
        position = self.motor.state.get("position")
        if position is not None:
            corse_pos = round(position * 10)
            self.zero_btn.setDisabled(corse_pos == 0)

    def set_zero_position(self):
        """Set the motor zero position"""
        self.motor.set_zero_position()
        self.zero_btn.setDisabled(True)

    def change_can_id(self):
        """Change the motor CAN ID"""
        new_id = self.motor_id_field.value()
        self.motor.change_motor_id(new_id)
        self.change_id_btn.setDisabled(True)

    def motor_id_field_changed(self, value: int):
        """Enable the motor ID button if it's a different ID than the motor"""
        self.change_id_btn.setDisabled(value == self.motor.motor_id)

    def build_id_field_form(self):
        """Build the form for changing the motor ID"""
        # Motor ID
        label = QLabel("Change your motor CAN ID")

        self.motor_id_field = QSpinBox()
        self.motor_id_field.setRange(1, 127)
        self.motor_id_field.setValue(self.motor.motor_id)
        self.motor_id_field.valueChanged.connect(self.motor_id_field_changed)

        self.change_id_btn = QPushButton("Change")
        self.change_id_btn.setDisabled(True)
        self.change_id_btn.clicked.connect(self.change_can_id)

        field_row = QHBoxLayout()
        hspacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        field_row.addWidget(self.motor_id_field)
        field_row.addWidget(self.change_id_btn)
        field_row.addItem(hspacer)

        hline = QFrame()
        hline.setFrameShape(QFrame.Shape.HLine)
        hline.setFrameShadow(QFrame.Shadow.Plain)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.addWidget(hline)
        layout.addWidget(label)
        layout.addLayout(field_row)

        return layout

    def build_layout(self):
        # Zero button
        self.zero_btn = QPushButton("Set zero position")
        self.zero_btn.clicked.connect(self.set_zero_position)

        change_id_form = self.build_id_field_form()

        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout()
        layout.addWidget(self.zero_btn)
        layout.addItem(spacer)
        layout.addLayout(change_id_form)
        self.setLayout(layout)
