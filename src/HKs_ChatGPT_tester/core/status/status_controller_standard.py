# 基本環境-------------------------------------------------------------
# DIコンテナ環境
from datetime import date
import datetime
from injector import inject
# ---------------------------------------------------------------------

import json

# 自前ファイル--------------------------------------------------------
from .i_status_controller import IStatusController
from .i_status_package import IStatusPackage
from ...config.i_settings import ISettings
from ...services.i_llm_client import ILlmClient
from ...utils.save_dict_array_to_excel import save_dict_array_to_excel
from ...utils.save_json2excel import ask_save_json2excel
# ---------------------------------------------------------------------
class StatusControllerStandard(IStatusController):
    @inject
    def __init__(self,settings:ISettings,statusPackage:IStatusPackage,lLMClient:ILlmClient):
        self.logs = []
        self._set_status_package(statusPackage)
        self.update_status_settings(settings)
        self.lLMClient = lLMClient
    def _set_status_package(self,statusPackage:IStatusPackage):
        self.statusPackage = statusPackage

    def processing_at_end_of_turn(self, prompt:str = "", response:dict = {}, messages:list = [], path_input_image:str = "", response_time = None)->None:
        self._update_status_every_turn_end(prompt, response, messages ,path_input_image, response_time)
        self._record_log()
        self._update_status_after_record_log()
        return

    # ターンの終了時に実行するステータス更新
    def _update_status_every_turn_end(self, prompt:str = None, response:dict = None, messages = None, path_input_image:str = None, response_time = None):
        if messages != None:
            self.statusPackage.statusStandard.set_messages(messages)
        if response != None:
            # responseに関するステータスの反映
            self.statusPackage.statusStandard.set_answer_text(self.lLMClient.extract_answer_text_from_response(response))
            self.statusPackage.statusStandard.set_detailed_response(response)
            self.statusPackage.statusStandard.set_prompt_tokens(self.lLMClient.extract_prompt_tokens_from_response(response))
            self.statusPackage.statusStandard.set_answer_test_tokens(self.lLMClient.extract_answer_text_tokens_from_response(response))
            self.statusPackage.statusStandard.set_total_tokens(self.lLMClient.extract_total_tokens_from_response(response))
        if prompt != None:
            self.statusPackage.statusStandard.set_prompt(prompt)
        if path_input_image != None:
            self.statusPackage.statusStandard.set_path_input_image(path_input_image)
        if response_time != None:
            self.statusPackage.statusStandard.set_response_time(response_time)

    def _update_status_after_record_log(self):
        # logの記録後のステータス更新
        self.statusPackage.statusStandard.increase_turn()

        # logの記録後のステータスクリア
        self.statusPackage.statusStandard.set_path_input_image(None)
        self.statusPackage.statusStandard.set_response_time(None)

    def update_status_end(self):
       return
    def create_log_entry(self) -> dict:
        log_entry = {
            "date": self.statusPackage.statusStandard.get_date_time().strftime("%Y%m%d%H%M%S") ,
            "messages": self.statusPackage.statusStandard.get_messages(),
            "LLM_model": self.statusPackage.statusStandard.get_llm_model(),
            "temperature": self.statusPackage.statusStandard.get_temperature(),
            "turn": self.statusPackage.statusStandard.get_turn(),
            "prompt": self.statusPackage.statusStandard.get_prompt(),
            "answer_text": self.statusPackage.statusStandard.get_answer_text(),
            "detailed_response": self.statusPackage.statusStandard.get_detailed_response(),
            "prompt_tokens": self.statusPackage.statusStandard.get_prompt_tokens(),
            "answer_text_tokens":self.statusPackage.statusStandard.get_answer_text_tokens(),
            "total_tokens": self.statusPackage.statusStandard.get_total_tokens(),
            "path_input_image": self.statusPackage.statusStandard.get_path_input_image(),
            "response_time": self.statusPackage.statusStandard.get_response_time()
        }
        return log_entry

    # settingsクラス更新時に実行するステータス更新
    def update_status_settings(self,settings):
        self.statusPackage.statusStandard.set_llm_model(settings.get_llm_model())
        self.statusPackage.statusStandard.set_temperature(settings.get_llm_temperature())

    def _record_log(self):
        log_entry = self.create_log_entry()
        self.logs.append(log_entry)

    def save_messages2excel(self, file_path):
        save_dict_array_to_excel(self.statusPackage.statusStandard.get_messages(),file_path)

    def ask_save_logs2excel(self, file_path: str, date=datetime.datetime.now(), sheet_name=None):
        if hasattr(self, 'logs'):
            ask_save_json2excel(self.logs, file_path, date, sheet_name)
        else:
            print("There are no log.")
