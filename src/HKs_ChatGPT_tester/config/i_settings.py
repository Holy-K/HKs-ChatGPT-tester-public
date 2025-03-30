from abc import ABC, abstractmethod

class ISettings(ABC):
    @abstractmethod
    def __init__(self):
        pass
