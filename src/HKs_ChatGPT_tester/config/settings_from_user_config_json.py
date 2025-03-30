# 基本環境-------------------------------------------------------------
# DIコンテナ環境
from injector import inject
# ---------------------------------------------------------------------

from ..config.i_settings import ISettings
import json

class SettingsFromUserConfigJson(ISettings):
    @inject
    def __init__(self, config_path:str):
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        self.openai_api_key = config.get('OPENAI_API_KEY', '')
        self.google_api_key = config.get('GOOGLE_API_KEY', '')
        self.LLM_model = config.get('LLM_MODEL', 'gpt-4')
        self.LLM_temperature = config.get('LLM_TEMPERATURE', 1.0)
        self.LLM_max_tokens = config.get('LLM_MAX_TOKENS', None)
        if self.LLM_max_tokens == "":
            self.LLM_max_tokens = None
        self.path_log_excel_file = config.get('PATH_LOG_EXCELFILE', 'log/sample.xlsx')
        self.on_sound_notification = config.get('SOUND_NOTIFICATION', False)
        self.path_sound_notification = config.get('PATH_SOUND_NOTIFICATION', 'sounds/holy_notification_sound_1.wav')
        self.initial_image_directory = config.get('INITIAL_IMAGE_DIRECTORY',  None)
    def display_all_settings(self):
        for attribute, value in self.__dict__.items():
            print(f"{attribute}: {value}")

    def get_openai_api_key(self):
        return self.openai_api_key

    def set_openai_api_key(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def get_LLM_model(self):
        return self.LLM_model

    def set_LLM_model(self, LLM_model):
        self.LLM_model = LLM_model

    def get_LLM_temperature(self):
        return self.LLM_temperature

    def set_LLM_temperature(self, LLM_temperature):
        self.LLM_temperature = LLM_temperature

    def get_path_log_excel_file(self):
        return self.path_log_excel_file

    def set_path_log_excel_file(self, path_log_excel_file):
        self.path_log_excel_file = path_log_excel_file

    def get_on_sound_notification(self):
        return self.on_sound_notification

    def set_on_sound_notification(self, on_sound_notification):
        self.on_sound_notification = on_sound_notification

    def get_path_sound_notification(self):
        return self.path_sound_notification

    def set_path_sound_notification(self, path_sound_notification):
        self.path_sound_notification = path_sound_notification
    def get_LLM_max_tokens(self):
        return self.LLM_max_tokens

    def set_LLM_max_tokens(self, LLM_max_tokens):
        self.LLM_max_tokens = LLM_max_tokens

    def get_initial_image_directory(self):
        return self.initial_image_directory
    def get_google_api_key(self):
        return self.google_api_key

