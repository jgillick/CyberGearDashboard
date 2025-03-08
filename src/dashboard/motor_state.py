from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import (
    QTableView,
    QDockWidget,
)

from motor import CyberGearMotor


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

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.model = StateTableModel(self.motor)
        self.build_layout()

    def build_layout(self):
        self.setWindowTitle("Motor state")

        table = QTableView()
        table.setModel(self.model)
        self.setWidget(table)
