from numbers import Real
from typing import List, Callable
from PySide6.QtCore import QAbstractTableModel, Qt


class ParameterTableModel(QAbstractTableModel):
    name_list: List[str]

    get_value: Callable[[str], Real]
    on_change: Callable[[str, Real], None]
    can_edit: Callable[[str, bool], None]

    headers = ("Name", "Value")

    def __init__(
        self,
        name_list: List[str],
        get_value: Callable[[str], Real],
        on_change: Callable[[str, Real], None],
        can_edit: Callable[[str, bool], None],
    ):
        super().__init__()
        self.get_value = get_value
        self.on_change = on_change
        self.can_edit = can_edit

        self.name_list = name_list
        self.name_list.sort()

    def data_did_change(self, name: str):
        if name not in self.name_list:
            self.name_list.append(name)
            self.name_list.sort()

        # Let the table know to reload the data row
        idx = self.name_list.index(name)
        if idx > -1:
            data_index = self.index(idx, len(self.headers) - 1)
            self.dataChanged.emit(data_index, data_index)

    def rowCount(self, index):
        return len(self.name_list)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            col = index.column()
            row = index.row()
            name = self.name_list[row]
            if col == 0:
                return name
            else:
                value = self.get_value(name)
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
            name = self.name_list[row]
            is_editable = self.can_edit(name)
            if is_editable:
                flags = flags | Qt.ItemIsEditable

        return flags

    def setData(self, index, value, /, role=...):
        try:
            if role == Qt.EditRole:
                row = index.row()
                name = self.name_list[row]
                is_editable = self.can_edit(name)
                if is_editable:
                    self.on_change(name, float(value))
                    return True
        except Exception as e:
            print(e)
        return False
