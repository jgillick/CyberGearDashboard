from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QAbstractScrollArea,
    QVBoxLayout,
)

from CyberGearDriver import CyberGearMotor

REFRESH_RATE_MS = 250


class FaultListWidget(QWidget):
    motor: CyberGearMotor
    list: QListWidget

    has_fault = Signal(bool)

    def __init__(self, motor: CyberGearMotor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.build_layout()

        timer = QTimer(self)
        timer.timeout.connect(self.update_list)
        timer.start(REFRESH_RATE_MS)

    def update_list(self):
        """Update the items in the fault list"""
        in_fault = [in_fault for in_fault in self.motor.faults.values() if in_fault]
        if len(in_fault) == 0:
            self.list.clear()
            self.list.setVisible(False)
        else:
            for name, in_fault in self.motor.faults.items():
                list_item = self.list.findItems(name, Qt.MatchExactly)
                # Add fault, if it's not already in the list
                if in_fault and len(list_item) == 0:
                    item = QListWidgetItem(name)
                    item.setForeground(QColor("red"))
                    self.list.addItem(item)
                # Remove fault, if it was in the list
                elif not in_fault and len(list_item) > 0:
                    self.list.takeItem(self.list.row(list_item[0]))
            self.setVisible(True)
            self.list.adjustSize()
            self.adjustSize()

    def build_layout(self):
        self.setVisible(False)

        self.list = QListWidget()
        self.list.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum
        )
        self.list.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        layout = QVBoxLayout()
        layout.addWidget(self.list)
        self.setLayout(layout)
