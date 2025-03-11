from PySide6.QtWidgets import QLabel, QDockWidget, QVBoxLayout, QWidget

from CyberGearDriver import CyberGearMotor

from .generic_table import GenericParamTable


class ParametersDockWidget(QDockWidget):
    motor: CyberGearMotor
    table: GenericParamTable

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor

        self.build_layout()
        self.table.reload()

    def build_layout(self):
        self.setWindowTitle("Parameters")

        descriptions = QLabel(
            "These parameters are stored in RAM and are reset between power cycles.",
            wordWrap=True,
        )
        self.table = GenericParamTable(self.motor, type="ram")

        layout = QVBoxLayout()
        layout.addWidget(descriptions)
        layout.addWidget(self.table)

        root = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(descriptions)
        layout.addWidget(self.table)
        root.setLayout(layout)
        self.setWidget(root)
