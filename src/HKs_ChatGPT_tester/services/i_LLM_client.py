from abc import ABC, abstractmethod

from httpx import request
from ..config.i_settings import ISettings

class ILLMClient(ABC):
    @abstractmethod
    def __init__(self)->None:
        pass

    @abstractmethod
    def update_settings(self, settings: ISettings) -> None:
        pass

    @abstractmethod
    def extract_answer_text_from_response(self, response)->str:
        pass
    @abstractmethod
    def extract_prompt_tokens_from_response(self, response) -> int:
        pass
    @abstractmethod
    def extract_answer_text_tokens_from_response(self, response) -> int:
        pass
    @abstractmethod
    def extract_total_tokens_from_response(self, response) -> int:
        pass
    @abstractmethod
    def request_LLM(self, messages:list):
        pass

    @abstractmethod
    def talk_LLM(self, prompt = None, messages:list = [])-> tuple[str, list]:
        pass
