# ----------------------------------------------------------------------------
# gemini_client.py
# 概要： gemini APIを使ったLLMクライアント
# 制作者：堀 和希
# Email: horikazuki28@akane.waseda.jp
# 参考：https://ai.google.dev/gemini-api/docs/quickstart?hl=ja&lang=python
# -----------------------------------------------------------------------------
# 基本環境-------------------------------------------------------------
# DIコンテナ環境
from httpx import request
from injector import inject
# ---------------------------------------------------------------------

# 外部ライブラリ-----------------------------------------------------
import os
import sys
import tkinter as tk
import time
import tkinter as tk
from tkinter import filedialog
import base64
import google.generativeai as genai
from http import client
from pyexpat import model

# --------------------------------------------------------------------
# 自前ファイル--------------------------------------------------------
from .i_llm_client import ILlmClient
from ..utils.print_thread_icon_loading import PrintThreadIconLoading
from ..config.i_settings import ISettings
# ---------------------------------------------------------------------

class GeminiClient(ILlmClient):
    @inject
    def __init__(self,settings:ISettings)->None:
        self.update_settings(settings)

    def extract_answer_text_from_response(self, response)->str:
        answer_text = response.candidates[0].content.parts[0].text
        return answer_text

    def extract_prompt_tokens_from_response(self, response) -> int:
        prompt_tokens = response.usage_metadata.prompt_token_count
        return prompt_tokens

    def extract_answer_text_tokens_from_response(self, response) -> int:
        answer_text_tokens = response.usage_metadata.candidates_token_count
        return answer_text_tokens

    def extract_total_tokens_from_response(self, response) -> int:
        total_tokens = response.usage_metadata.total_token_count
        return total_tokens

    def update_settings(self,settings:ISettings)->None:
        self.settings = settings
        genai.configure(api_key = self.settings.get_google_api_key())
        self.model = genai.GenerativeModel(model_name = settings.get_llm_model())
        self.temperature = settings.get_llm_temperature()
        self.max_output_tokens = settings.get_llm_max_tokens()
        self.config = {
            "temperature": self.settings.get_llm_temperature(),
            "max_output_tokens": self.settings.get_llm_max_tokens(),
        }
    def request_llm(self, messages:list):
        with PrintThreadIconLoading(("Waiting ",self.settings.get_llm_model(),"'s response..."),""):
            response = self.model.generate_content(messages, generation_config=self.config)
        return response

    def talk_llm(self, prompt = None, messages:list = [])-> tuple[str, list]:
        if prompt:
            messages.append({'role':'user','parts': prompt})
        with PrintThreadIconLoading(("Waiting ",self.settings.get_llm_model(),"'s response..."),""):
            response = self.request_llm(messages)
            messages.append({'role':'assistant','parts': self.extract_answer_text_from_response(response)})
        return response, messages

    def select_file(self, path_initial_dir:str=os.path.dirname(os.path.abspath(__file__)))->str:
        root = tk.Tk()#tkウィンドウを開く（エクスプローラーも一緒に開かれる）
        root.withdraw()#tkウィンドウを閉じる
        root.attributes('-topmost', True)  # エクスプローラーウィンドウを最前面に表示する
        file_path = filedialog.askopenfilename(initialdir = path_initial_dir)# ファイルダイアログを開いてファイルを選択
        print("\033[38;2;148;0;211m" + "Input image:",file_path+ "\033[0m")
        return file_path

    def _encode_image(self, image_path:str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def talk_llm_vision_multiple(self, prompt:str = None, messages:list = [], file_paths:list = []) -> tuple[str, list]:
        if isinstance(file_paths, list) and file_paths != []:
            base64_images = [self._encode_image(fp) for fp in file_paths]
            image_parts = [{"mime_type": "image/jpeg", "data": base64.b64decode(img)} for img in base64_images]
            parts = []
            if prompt:
                parts.append({"text": prompt})
            parts.extend(image_parts)
            custom_message = {
                "role": "user",
                "parts": parts
            }
            messages.append(custom_message)
        elif prompt != "" and prompt != None:
            custom_message = {
                "role": "user",
                "parts": [{"text": prompt}]
            }
            messages.append(custom_message)
        response = self.request_llm(messages)
        messages.append({'role':'assistant','parts': self.extract_answer_text_from_response(response)})
        return response, messages
