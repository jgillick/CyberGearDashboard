from typing import List, Tuple, Union
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QDoubleSpinBox,
)

from CyberGearDriver import CyberGearMotor
from CyberGearDriver.parameters import ParameterName, DataType, get_parameter_by_name

RageValue = Tuple[Union[int, float], Union[int, float]]


class SliderInputWidget(QWidget):
    """Creates an input of a slider and a input field"""

    value: Union[int, float]
    label_text: str
    parameter: List
    range: RageValue
    type: DataType
    decimals: int
    float_multiplier: int

    input: QDoubleSpinBox
    slider: QSlider

    def __init__(
        self,
        label: str,
        value: Union[int, float],
        range: RageValue,
        type: DataType = DataType.FLOAT,
        decimals: int = 2,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.label_text = label
        self.type = type
        self.range = range
        self.value = value
        self.decimals = decimals if self.type == DataType.FLOAT else 0
        self.float_multiplier = 10**decimals

        self.build_layout()

    def on_slider_change(self, value: int):
        """Set the input value from the slider"""
        if self.type == DataType.FLOAT:
            value = value / self.float_multiplier
        self.input.setValue(value)

    def on_input_change(self, value: Union[int, float]):
        """Set the slider value from the input field"""
        self.value = value
        if self.slider:
            if self.type == DataType.FLOAT:
                slider_value = value * self.float_multiplier
            self.slider.setValue(round(slider_value))

    def set_value(self, value: Union[int, float]):
        """Set the value of the input"""
        self.input.setValue(value)

    def build_layout(self):
        label = QLabel(self.label_text)

        # Slider widget
        if self.range:
            (slider_min, slider_max) = self.range
            if self.type == DataType.FLOAT:
                slider_min *= self.float_multiplier
                slider_max *= self.float_multiplier

            self.slider = QSlider(
                tickPosition=QSlider.TickPosition.TicksBelow,
                tickInterval=(abs(slider_min) + abs(slider_max)) / 2,
            )
            self.slider.setMinimum(slider_min)
            self.slider.setMaximum(slider_max)
            self.slider.setOrientation(Qt.Orientation.Horizontal)
            self.slider.valueChanged.connect(self.on_slider_change)

        # Input widget
        self.input = QDoubleSpinBox(singleStep=0.1)
        self.input.setDecimals(self.decimals)
        self.input.setSingleStep(0.1 if self.type == DataType.FLOAT else 1)
        if self.range:
            (min, max) = self.range
            self.input.setMinimum(min)
            self.input.setMaximum(max)
        self.input.valueChanged.connect(self.on_input_change)
        self.input.setValue(self.value)

        field_layout = QHBoxLayout()
        if self.slider:
            field_layout.addWidget(self.slider)
        field_layout.addWidget(self.input)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(field_layout)
        self.setLayout(layout)


class SliderMotorInputWidget(SliderInputWidget):
    """Creates an input of a slider and a input field that gets it's value from a motor property"""

    motor: CyberGearMotor
    param_name: str

    def __init__(
        self,
        label: str,
        motor: CyberGearMotor,
        param_name: ParameterName,
        decimals: int = 2,
        *args,
        **kwargs,
    ):
        # Get parameter config and value from motor
        self.motor = motor
        self.param_name = param_name
        self.parameter = get_parameter_by_name(param_name)
        (id, name, type, range, permissions) = self.parameter
        value = motor.params.get(param_name, 0)

        super().__init__(
            label=label,
            value=value,
            type=type,
            range=range,
            decimals=decimals,
            *args,
            **kwargs,
        )

    def reset(self):
        """Reset the value from the motor parameters"""
        self.set_value(self.motor.params.get(self.param_name, 0))

    def send_to_motor(self):
        """Send the value to the motor"""
        self.motor.set_parameter(self.param_name, self.value)
