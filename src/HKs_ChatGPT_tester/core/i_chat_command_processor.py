from abc import ABC, abstractmethod

class IChatCommandProcessor(ABC):
    @abstractmethod
    def __init__(self):
        pass
    def _nomal_process(prompt:str):
        pass
