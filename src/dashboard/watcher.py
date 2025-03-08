import threading
import time

from motor import CyberGearMotor

# How often to request updates from the motor (in seconds)
UPDATE_RATE = 0.5


class MotorWatcher(threading.Thread):
    motor: CyberGearMotor

    def __init__(self, motor=CyberGearMotor, *args, **kwargs):
        self.motor = motor
        super().__init__(daemon=True, *args, **kwargs)

    def run(self):
        while True:
            self.motor.request_motor_state()
            self.motor.request_motor_fault_status()
            time.sleep(UPDATE_RATE)
