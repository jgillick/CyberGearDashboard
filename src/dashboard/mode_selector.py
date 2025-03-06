from PySide6.QtWidgets import QHBoxLayout, QComboBox, QLabel, QSizePolicy

from motor import CyberGearMotor, RunMode

options = (
    ("Stopped", RunMode.STOPPED),
    ("Operation Control", RunMode.OPERATION_CONTROL),
    ("Position", RunMode.POSITION),
    ("Velocity", RunMode.VELOCITY),
    ("Torque", RunMode.VELOCITY),
)


class ModeSelector(QHBoxLayout):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor
        self.build_layout()

    def on_change(self, text):
        for name, mode in options:
            if name == text:
                if mode != RunMode.STOPPED:
                    self.motor.enable()
                self.motor.mode(mode)
                break

    def build_layout(self):
        title = QLabel("Mode")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        combobox = QComboBox()
        combobox.addItems([name for (name, mode) in options])
        combobox.currentTextChanged.connect(self.on_change)

        self.addWidget(title)
        self.addWidget(combobox)
