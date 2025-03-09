from typing import List
from PySide6.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt, QPoint
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QDockWidget,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QSizePolicy,
    QLineEdit,
    QWidget,
    QAbstractItemView,
    QMenu,
)

from motor import CyberGearMotor
from motor.parameters import (
    Parameters,
    DataType,
    get_parameter_by_name,
)


class ParameterTableModel(QAbstractTableModel):
    motor: CyberGearMotor
    param_list: List[str]
    headers = ("Name", "Value")

    def __init__(self, motor: CyberGearMotor):
        super().__init__()
        self.motor = motor

        # Filter out string type params
        self.param_list = [
            name for (id, name, type, *rest) in Parameters if type != DataType.STRING
        ]
        self.param_list.sort()

        motor.on("param_changed", self.onItemChanged)
        self.reload()

    def reload(self):
        """Fetch all parameter values from the motor"""
        for name in self.param_list:
            self.motor.request_parameter(name)

    def onItemChanged(self, param_name, value):
        # Find index for parameter name
        idx = self.param_list.index(param_name)
        if idx > -1:
            data_index = self.index(idx, 1)
            self.dataChanged.emit(data_index, data_index)

    def rowCount(self, index):
        return len(self.param_list)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            col = index.column()
            row = index.row()
            name = self.param_list[row]
            if col == 0:
                return name
            else:
                value = self.motor.params.get(name)
                if value is None:
                    return value
                return "{:.3f}".format(value)  # Format to 3 decimal positions
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

    def flags(self, index):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        col = index.column()
        row = index.row()
        if col == 1:
            (id, name, type, range, permissions) = get_parameter_by_name(
                self.param_list[row]
            )
            if permissions == "rw":
                flags = flags | Qt.ItemIsEditable

        return flags

    def setData(self, index, value, /, role=...):
        if role == Qt.EditRole:
            row = index.row()
            (id, name, type, range, permissions) = get_parameter_by_name(
                self.param_list[row]
            )
            if permissions == "rw":
                if type == DataType.FLOAT:
                    value = float(value)
                else:
                    value = int(value)
                self.motor.set_parameter(name, value)
                self.motor.request_parameter(name)
                return True
            return False


class MotorParametersWidget(QDockWidget):
    motor: CyberGearMotor
    model: ParameterTableModel
    table: QTableView
    filtered_model: QSortFilterProxyModel

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor

        self.model = ParameterTableModel(self.motor)
        self.filtered_model = QSortFilterProxyModel()
        self.filtered_model.setSourceModel(self.model)

        self.build_layout()

    def open_context_menu(self, position: QPoint):
        index = self.table.indexAt(position)
        print("context?")
        if index.isValid():
            menu = QMenu(self)
            graph_action = menu.addAction("Graph")
            action = menu.exec(self.table.viewport().mapToGlobal(position))
            if action == graph_action:
                print(f"Action 1 triggered on row {index.row()}")

    def build_layout(self):
        self.setWindowTitle("Parameters")

        refresh_btn = QPushButton()
        refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        refresh_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_btn.clicked.connect(self.model.reload)

        search_field = QLineEdit(placeholderText="search", clearButtonEnabled=True)
        search_field.textChanged.connect(self.search)

        self.table = QTableView()
        self.table.setModel(self.filtered_model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)

        search_layout = QHBoxLayout()
        search_layout.addWidget(refresh_btn)
        search_layout.addWidget(search_field)

        layout = QVBoxLayout()
        layout.addLayout(search_layout)
        layout.addWidget(self.table)

        root = QWidget()
        root.setLayout(layout)
        self.setWidget(root)

    def search(self, text):
        self.filtered_model.setFilterFixedString(text)
        self.filtered_model.setFilterKeyColumn(0)
