from typing import List, Literal
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QPushButton,
)

from CyberGearDriver import CyberGearMotor
from CyberGearDashboard.watcher import MotorWatcher

from .chart import Chart

CHART_STATE = ["position", "velocity", "torque"]


class ChartLayout(QVBoxLayout):
    motor: CyberGearMotor
    watcher: MotorWatcher
    data_list: List[str]
    charts: List[Chart]
    state: Literal["running", "paused"]

    def __init__(self, motor: CyberGearMotor, watcher: MotorWatcher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.watcher = watcher
        self.state = "running"
        self.build_layout()

    def toggle_running(self):
        """Toggle pause on all charts"""
        if self.state == "running":
            self.toggle.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
            self.state = "paused"
        else:
            self.toggle.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
            self.state = "running"

        for chart in self.charts:
            if self.state == "running":
                chart.start()
            else:
                chart.pause()

    def clear_charts(self):
        """Clear all chart data"""
        for chart in self.charts:
            chart.clear()

    def build_layout(self):
        # Toolbar
        self.toggle = QPushButton()
        self.toggle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.toggle.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause))
        self.toggle.clicked.connect(self.toggle_running)

        clear = QPushButton()
        clear.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        clear.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear))
        clear.clicked.connect(self.clear_charts)

        hspacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        toolbar = QHBoxLayout()
        toolbar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        toolbar.addWidget(self.toggle)
        toolbar.addItem(hspacer)
        toolbar.addWidget(clear)
        self.addLayout(toolbar)

        # Charts
        self.charts = []
        for data in CHART_STATE:
            chart = Chart(self.motor, data)
            self.charts.append(chart)
            self.addWidget(chart)

        vspacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.addItem(vspacer)
