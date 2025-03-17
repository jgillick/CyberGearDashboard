from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QDockWidget,
    QAbstractItemView,
)

from CyberGearDashboard.charts import ChartLayout
from CyberGearDriver import CyberGearMotor

from .state_table_model import StateTableModel
from .fault_list import FaultListWidget


class MotorStateWidget(QDockWidget):
    model: StateTableModel
    motor: CyberGearMotor
    charts: ChartLayout

    def __init__(self, motor: CyberGearMotor, charts: ChartLayout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.charts = charts
        self.model = StateTableModel(self.motor)
        self.build_layout()

    def build_layout(self):
        self.setWindowTitle("Motor state")

        fault_list = FaultListWidget(motor=self.motor)

        table = QTableView()
        table.setModel(self.model)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        root = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(fault_list)
        layout.addWidget(table)
        root.setLayout(layout)
        self.setWidget(root)
