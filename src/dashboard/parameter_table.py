from PySide6.QtCore import (
    QAbstractTableModel,
    QSortFilterProxyModel,
    Qt,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QLabel,
    QPushButton,
    QSizePolicy,
    QLineEdit,
)

from motor import CyberGearMotor
from motor.parameters import Parameters, ParamNames, TYPE_FLOAT, TYPE_STRING


class ParameterTableModel(QAbstractTableModel):
    motor: CyberGearMotor

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor

        # Filter out string value rows
        self.table_rows = [
            (id, name, type, *rest)
            for (id, name, type, *rest) in Parameters
            if type != TYPE_STRING
        ]

        motor.on("param_changed", self.onItemChanged)
        self.reload()

    def reload(self):
        """Fetch all parameter values from the motor"""
        for param in self.table_rows:
            self.motor.request_parameter(param[1])

    def onItemChanged(self, param_name, value):
        # Find index for parameter name
        idx = -1
        for i in range(len(self.table_rows)):
            if self.table_rows[i][1] == param_name:
                data_index = i
                break

        data_index = self.index(idx, 2)
        self.dataChanged.emit(data_index, data_index)

    def rowCount(self, index):
        return len(self.table_rows)

    def columnCount(self, parent=None):
        return 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            col = index.column()
            row = index.row()
            (id, name, *rest) = self.table_rows[row]
            if col == 0:
                return name
            else:
                return self.motor.params.get(name)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return "Name"
            else:
                return "Value"
        return None

    def flags(self, index):
        flags = Qt.ItemIsEnabled

        col = index.column()
        row = index.row()
        (id, name, type, range, permissions) = self.table_rows[row]
        if col == 1 and permissions == "rw":
            flags = flags | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return flags

    def setData(self, index, value, /, role=...):
        print("Set data!")
        if role == Qt.EditRole:
            col = index.column()
            row = index.row()
            (id, name, type, range, permissions) = self.table_rows[row]
            if permissions == "rw":
                if type == TYPE_FLOAT:
                    value = float(value)
                else:
                    value = int(value)
                self.motor.set_parameter(name, value)
                self.motor.request_parameter(name)
                return True
            return False


class ParameterTable(QVBoxLayout):
    motor: CyberGearMotor
    model: ParameterTableModel
    filtered_model: QSortFilterProxyModel

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor

        self.model = ParameterTableModel(self.motor)
        self.filtered_model = QSortFilterProxyModel()
        self.filtered_model.setSourceModel(self.model)

        self.build_layout()

    def build_layout(self):
        title = QLabel("Motor Parameters")
        refresh_btn = QPushButton()
        refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        refresh_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_btn.clicked.connect(self.model.reload)

        search_field = QLineEdit(placeholderText="search", clearButtonEnabled=True)
        search_field.textChanged.connect(self.search)

        table = QTableView()
        table.setModel(self.filtered_model)

        title_layout = QHBoxLayout()
        title_layout.addWidget(title)
        title_layout.addWidget(refresh_btn)
        self.addLayout(title_layout)
        self.addWidget(search_field)
        self.addWidget(table)
        self.setSpacing(0)

    def search(self, text):
        self.filtered_model.setFilterFixedString(text)
        self.filtered_model.setFilterKeyColumn(0)
