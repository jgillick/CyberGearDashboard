import math
from typing import List
from pyqtgraph.Qt import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout

import pyqtgraph as pg

from CyberGearDriver import CyberGearMotor, StateName

MAX_DATA_POINTS = 100
UPDATE_RATE_MS = 100


class Chart(QWidget):
    motor: CyberGearMotor
    plot: pg.PlotDataItem
    data_name: StateName
    x: List[int]
    y: List[float]

    def __init__(self, motor: CyberGearMotor, data_name: StateName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.data_name = data_name
        self.x = list(range(MAX_DATA_POINTS))
        self.y = [math.nan] * MAX_DATA_POINTS

        self.build_layout()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.start()

    def start(self):
        """Start/resume displaying data in the chart"""
        self.timer.start(UPDATE_RATE_MS)

    def pause(self):
        """Pause sending new data to the chart"""
        self.timer.stop()

    def clear(self):
        """Clear the chart data"""
        self.y = [math.nan] * MAX_DATA_POINTS
        self.plot.setData(self.y)

    def update_data(self):
        value = self.motor.state.get(self.data_name)
        if value is None:
            return

        # Shift the data over
        self.y[1:] = self.y[:-1]
        self.y[0] = value

        # Plot
        self.plot.setData(self.y)

    def build_layout(self):
        graph = pg.PlotWidget()
        graph.setTitle(self.data_name)

        self.plot = graph.plot(self.x, self.y, connect="finite")
        self.plot.setClipToView(True)

        layout = QVBoxLayout()
        layout.addWidget(graph)
        self.setLayout(layout)
