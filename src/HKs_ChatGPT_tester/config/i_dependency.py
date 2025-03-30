from abc import ABC, abstractmethod


class IDependency(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def bind_config(cls, binder):
        pass

    @abstractmethod
    def resolve(self, cls):
        pass
