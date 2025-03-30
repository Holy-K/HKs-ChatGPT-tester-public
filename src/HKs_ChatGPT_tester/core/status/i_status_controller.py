from abc import ABC, abstractmethod

class IStatusController(ABC):

    @abstractmethod
    def __init__(self, settings):
        pass
    @abstractmethod
    def _set_status_package(self):
        pass
    @abstractmethod
    def processing_at_end_of_turn(self)->None:
        pass
    @abstractmethod
    def _update_status_every_turn_end(self):
        pass
    @abstractmethod
    def _update_status_after_record_log(self)->None:
        pass

    @abstractmethod
    def update_status_end(self):
        pass

    def create_log_entry(self) -> dict:
        pass

    def _record_log(self):
        pass

    def _ask_save_logs2excel(self):
        pass
