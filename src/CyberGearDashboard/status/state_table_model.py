from PySide6.QtCore import QAbstractTableModel, Qt, QTimer

from CyberGearDashboard.charts import ChartLayout
from CyberGearDriver import CyberGearMotor

REFRESH_RATE_MS = 100


class StateTableModel(QAbstractTableModel):
    motor: CyberGearMotor
    prev_data: dict
    headers = ["Name", "Value"]
    state_list = ["position", "velocity", "torque", "temperature"]

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor
        self.prev_data = {}

        timer = QTimer(self)
        timer.timeout.connect(self.update_data)
        timer.start(REFRESH_RATE_MS)

    def update_data(self):
        """Check for updated data"""
        data = self.motor.state
        for name in self.state_list:
            value = data.get(name)
            prev_value = self.prev_data.get(name)
            if prev_value is None or value != prev_value:
                self.data_did_change(name)
        self.prev_data = self.motor.state.copy()

    def data_did_change(self, name: str):
        """The data for a state item (by name) has changed"""
        idx = self.state_list.index(name)
        if idx > -1:
            data_index = self.index(idx, len(self.headers) - 1)
            self.dataChanged.emit(data_index, data_index)

    def rowCount(self, index):
        return len(self.state_list)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            col = index.column()
            row = index.row()
            name = self.state_list[row]
            if col == 0:
                return name
            else:
                value = self.motor.state.get(name)
                if value is None:
                    return value
                return "{:.3f}".format(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None
