from numbers import Real
from PySide6.QtCore import QSortFilterProxyModel, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QSizePolicy,
    QLineEdit,
    QDockWidget,
    QAbstractItemView,
)

from CyberGearDriver import CyberGearMotor
from CyberGearDriver.parameters import (
    parameter_names,
    get_parameter_by_name,
    READ_WRITE,
)

from .table_model import ParameterTableModel

REFRESH_RATE_MS = 500


class ParametersTableDock(QDockWidget):
    motor: CyberGearMotor
    model: ParameterTableModel
    table: QTableView
    filtered_model: QSortFilterProxyModel
    last_data: dict

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.type = type
        self.last_data = {}

        self.model = ParameterTableModel(
            name_list=parameter_names,
            get_value=self.get_value,
            on_change=self.change_param,
            can_edit=self.can_edit,
        )
        self.filtered_model = QSortFilterProxyModel()
        self.filtered_model.setSourceModel(self.model)

        timer = QTimer(self)
        timer.timeout.connect(self.check_for_updates)
        timer.start(REFRESH_RATE_MS)

        self.reload()
        self.build_layout()

    def get_data(self):
        return self.motor.config if self.type == "config" else self.motor.params

    def get_value(self, name: str) -> Real:
        """Return the parameter value for the given name"""
        return self.get_data().get(name, None)

    def reload(self):
        """Reload all param valuse from the motor"""
        for name in parameter_names:
            self.motor.request_parameter(name)

    def check_for_updates(self):
        """Check the motor data for updates"""
        data = self.get_data()
        for name, value in data.items():
            if self.last_data.get(name) is None or value != self.last_data.get(name):
                self.model.data_did_change(name)
        self.last_data = data

    def change_param(self, name: str, value: Real):
        """Change the parameter value for the given name"""
        self.motor.set_parameter(name, value)
        self.motor.request_parameter(name)

    def can_edit(self, name: str) -> bool:
        """Return whether the parameter value for the given name can be edited"""
        try:
            (_, _, _, _, permission) = get_parameter_by_name(name)
            return permission == READ_WRITE
        except:
            return False

    def build_layout(self):
        self.setWindowTitle("Parameters")

        refresh_btn = QPushButton()
        refresh_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        refresh_btn.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        refresh_btn.clicked.connect(self.reload)

        search_field = QLineEdit(placeholderText="search", clearButtonEnabled=True)
        search_field.textChanged.connect(self.search)

        self.table = QTableView()
        self.table.setModel(self.filtered_model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

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
