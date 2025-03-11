from PySide6.QtWidgets import QLabel, QDockWidget, QVBoxLayout, QWidget

from motor import CyberGearMotor

from .generic_table import GenericParamTable


class ConfigDockWidget(QDockWidget):
    motor: CyberGearMotor
    table: GenericParamTable

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()
        self.table.reload()

    def build_layout(self):
        self.setWindowTitle("Configuration")

        descriptions = QLabel(
            "These values are stored in nonvolatile memory and are retained between power cycles.",
            wordWrap=True,
        )
        self.table = GenericParamTable(self.motor, type="config")

        root = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(descriptions)
        layout.addWidget(self.table)
        root.setLayout(layout)
        self.setWidget(root)
