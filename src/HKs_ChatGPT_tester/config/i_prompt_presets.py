from abc import ABC, abstractmethod

class IPromptPresets(ABC):
    @abstractmethod
    def __init__(self):
        prompt_presets = []
