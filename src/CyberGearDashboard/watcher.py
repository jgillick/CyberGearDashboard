import threading
import time
from typing import Set

from CyberGearDriver import CyberGearMotor, ParameterName

# How often to request updates from the motor (in seconds)
UPDATE_RATE = 0.1


class MotorWatcher(threading.Thread):
    is_watching: bool
    motor: CyberGearMotor
    params: Set[ParameterName]

    def __init__(self, motor=CyberGearMotor, *args, **kwargs):
        self.motor = motor
        self.params = set()
        super().__init__(daemon=True, *args, **kwargs)

    def watch_param(self, name: ParameterName):
        """Add a parameter to watch"""
        self.params.add(name)

    def unwatch_param(self, name: ParameterName):
        """Remove a parameter to watch"""
        self.params.remove(name)

    def stop_watching(self):
        """Stop watching the motor"""
        self.is_watching = False

    def run(self):
        self.is_watching = True
        while self.is_watching:
            self.motor.request_motor_state()
            for param in self.params:
                self.motor.request_parameter(param)
            self.motor.request_motor_fault_status()

            time.sleep(UPDATE_RATE)
