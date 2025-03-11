from PySide6.QtWidgets import QTabWidget, QDockWidget, QVBoxLayout

from CyberGearDriver import CyberGearMotor

from .generic_table import GenericParamTable


class ParametersTabboxWidget(QDockWidget):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor

        self.build_layout()

    def build_layout(self):
        tabbox = QTabWidget()
        tabbox.contentsMargins(10, 10, 10, 10)
        param_table = GenericParamTable(self.motor, type="ram")
        config_table = GenericParamTable(self.motor, type="config")
        tabbox.addTab(param_table, "RAM Params")
        tabbox.addTab(config_table, "Configuration")

        self.setWidget(tabbox)

    def search(self, text):
        self.filtered_model.setFilterFixedString(text)
        self.filtered_model.setFilterKeyColumn(0)
