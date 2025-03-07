from typing import List, Tuple, Union
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSlider, QDoubleSpinBox

from motor import CyberGearMotor
from motor.parameters import ParameterName, TYPE_FLOAT, get_parameter_by_name


class SliderMotorControlWidget(QVBoxLayout):
    value: Union[int, float]
    motor: CyberGearMotor
    label_text: str
    parameter: List
    range: Tuple
    type: str

    input: QDoubleSpinBox
    slider: QSlider

    def __init__(
        self,
        motor: CyberGearMotor,
        param_name: ParameterName,
        label: str,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.motor = motor
        self.label_text = label

        self.parameter = get_parameter_by_name(param_name)
        (id, name, type, range, permissions) = self.parameter
        self.range = range
        self.type = type
        self.value = motor.params.get(param_name, 0)

        self.build_layout()

    def on_slider_change(self, value: int):
        """Set the input value from the slider"""
        if self.type == TYPE_FLOAT:
            value = value / 100
        self.input.setValue(value)

    def on_input_change(self, value: Union[int, float]):
        """Set the slider value from the input field"""
        if self.slider:
            if self.type == TYPE_FLOAT:
                value = value * 100
            self.slider.setValue(round(value))

    def build_layout(self):
        label = QLabel(self.label_text)

        if self.range:
            (min, max) = self.range
            self.slider = QSlider()
            self.slider.setOrientation(Qt.Orientation.Horizontal)
            if self.type == TYPE_FLOAT:
                self.slider.setMinimum(min * 100)
                self.slider.setMaximum(max * 100)
            else:
                self.slider.setMinimum(min)
                self.slider.setMaximum(max)
            self.slider.valueChanged.connect(self.on_slider_change)

        self.input = QDoubleSpinBox()
        if self.range:
            (min, max) = self.range
            self.input.setMaximum(max)
            self.input.setMinimum(min)
        self.input.valueChanged.connect(self.on_input_change)

        field_layout = QHBoxLayout()
        if self.slider:
            field_layout.addWidget(self.slider)
        field_layout.addWidget(self.input)

        self.addWidget(label)
        self.addLayout(field_layout)
