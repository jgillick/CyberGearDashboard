from PySide6.QtCore import QAbstractTableModel, Qt, QPoint
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QDockWidget,
    QListWidget,
    QAbstractItemView,
    QListWidgetItem,
    QSizePolicy,
    QAbstractScrollArea,
    QMenu,
)

from CyberGearDashboard.charts import ChartLayout
from CyberGearDriver import CyberGearMotor


class StateTableModel(QAbstractTableModel):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor
        motor.on("state_changed", self.onItemChanged)
        self.reload()

    def reload(self):
        """Fetch all parameter values from the motor"""
        self.motor.request_motor_state()

    def onItemChanged(self):
        top = self.index(0, 0)
        bottom = self.index(len(self.motor.state), 1)
        self.dataChanged.emit(top, bottom)

    def rowCount(self, index):
        return len(self.motor.state)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            col = index.column()
            row = index.row()
            names = list(self.motor.state.keys())
            values = list(self.motor.state.values())
            if col == 0:
                return names[row]
            else:
                return values[row]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Name"
            else:
                return "Value"
        return None


class MotorStateWidget(QDockWidget):
    model: StateTableModel
    motor: CyberGearMotor
    charts: ChartLayout
    table: QTableView
    fault_list: QListWidget

    def __init__(self, motor: CyberGearMotor, charts: ChartLayout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.charts = charts
        self.model = StateTableModel(self.motor)
        self.build_layout()

        self.update_fault_list()
        motor.on("has_fault", self.update_fault_list)
        motor.on("fault_cleared", self.update_fault_list)

    def update_fault_list(self):
        """Update the list of faults reported by the motor"""
        self.fault_list.clear()
        has_fault = False
        for name, in_fault in self.motor.faults.items():
            if in_fault:
                item = QListWidgetItem(name)
                item.setForeground(QColor("red"))
                self.fault_list.addItem(item)
                has_fault = True
        self.fault_list.setVisible(has_fault)
        self.fault_list.adjustSize()

    # def open_context_menu(self, position: QPoint):
    #     index = self.table.indexAt(position)
    #     if index.isValid():
    #         row = index.row()
    #         name = self.model.data(self.model.index(row, 0))
    #         has_chart = self.charts.has_chart("state", name)

    #         menu = QMenu(self)
    #         graph_action = menu.addAction(
    #             f"Chart {name}" if not has_chart else "Remove chart"
    #         )
    #         action = menu.exec(self.table.viewport().mapToGlobal(position))
    #         if action == graph_action:
    #             if has_chart:
    #                 self.charts.remove_chart("state", name)
    #             else:
    #                 self.charts.add_chart("state", name)

    def build_layout(self):
        self.setWindowTitle("Motor state")

        self.fault_list = QListWidget()
        self.fault_list.setVisible(False)
        self.fault_list.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
        )
        self.fault_list.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.fault_list.setStyleSheet("background-color:transparent;")

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        # self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # self.table.customContextMenuRequested.connect(self.open_context_menu)

        root = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.fault_list)
        layout.addWidget(self.table)
        root.setLayout(layout)
        self.setWidget(root)
