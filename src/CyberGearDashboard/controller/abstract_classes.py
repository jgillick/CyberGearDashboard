from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget


class AbstractControlPanel(ABC, type(QWidget)):
    @abstractmethod
    def load(self):
        """The screen is showing."""
        pass

    @abstractmethod
    def unload(self):
        """Shutdown the motor actions and unload the screen"""
        pass
