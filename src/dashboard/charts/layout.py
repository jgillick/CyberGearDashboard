from typing import Literal, List, Tuple
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from motor import CyberGearMotor, StateName, ParameterName
from dashboard.watcher import MotorWatcher

ValueType = Literal["state", "param"]
ValueName = Literal[StateName, ParameterName]
ChartConfig = Tuple[ValueType, ValueName]


class ChartLayout(QVBoxLayout):
    motor: CyberGearMotor
    watcher: MotorWatcher
    configs: List[ChartConfig]

    def __init__(self, motor: CyberGearMotor, watcher: MotorWatcher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.watcher = watcher
        self.configs = []

    def has_chart(self, type: ValueType, name: ValueName):
        """Check if this chart config already exists"""
        return (type, name) in self.configs

    def remove_chart(self, type: ValueType, name: ValueName):
        """Remove a chart config"""
        if not self.has_chart(type, name):
            return
        if type == "param":
            self.watcher.unwatch_param(name)
        self.configs.remove((type, name))

    def add_chart(self, type: ValueType, name: ValueName):
        """Add a chart cofig"""
        if self.has_chart(type, name):
            return
        self.configs.append((type, name))
        if type == "param":
            self.watcher.watch_param(name)
