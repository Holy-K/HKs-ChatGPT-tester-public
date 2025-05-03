# 基本環境-------------------------------------------------------------
# DIコンテナ環境
from injector import inject
# ---------------------------------------------------------------------

# 外部ライブラリ-----------------------------------------------------
import os
import openai
import tkinter as tk
import time
import tkinter as tk
from tkinter import filedialog
import base64
# --------------------------------------------------------------------

# 自前ファイル--------------------------------------------------------
from ..services.i_llm_client import ILlmClient
from ..utils.print_thread_icon_loading import PrintThreadIconLoading
from ..config.i_settings import ISettings
# ---------------------------------------------------------------------


class ChatgptClient(ILlmClient):
    @inject
    def __init__(self,settings:ISettings):
        self.update_settings(settings)

    def update_settings(self, settings: ISettings) -> None:
        self.settings = settings
        openai.api_key = settings.openai_api_key
        self.llm_model = settings.llm_model
        self.llm_temperature = settings.llm_temperature
        self.llm_max_tokens = settings.llm_max_tokens

    def extract_answer_text_from_response(self, response)->str:
        return response.choices[0].message.content

    def extract_prompt_tokens_from_response(self, response) -> int:
        tokens = response.usage.prompt_tokens
        return tokens
    def extract_answer_text_tokens_from_response(self, response) -> int:
        answer_text_tokens = response.usage.completion_tokens
        return answer_text_tokens

    def extract_total_tokens_from_response(self, response) -> int:
        total_tokens = response.usage.total_tokens
        return total_tokens

    # =============================================================================
    # d.1.1 ChatGPTに回答を申請する関数
    # messagesとllm_modelを入力し，ChatGptのresponseを返す
    # =============================================================================
    def request_llm(self, messages:list):
        with PrintThreadIconLoading("Waiting ChatGPT's response...",""):
            for message in messages:
                if not isinstance(message, dict):
                    raise TypeError("Each message must be a dictionary")
            if self.llm_max_tokens ==None:
                response = openai.chat.completions.create(
                    model = self.llm_model,
                    messages = messages,
                    temperature = self.llm_temperature,
                )
            else:
                response = openai.chat.completions.create(
                    model=self.llm_model,
                    messages=messages,
                    temperature=self.llm_temperature,
                    max_tokens=self.llm_max_tokens
                )
        return response

    # =============================================================================
    # d.1.2 ChatGPTに回答を申請し，やり取りをmessagesに格納する関数
    # promptとmessagesを入力し，ChatGptのresponseとChatGptのresponseを格納済みのmessagesを返す
    # =============================================================================
    def talk_llm(self, prompt:str = "", messages:list =[]) -> tuple[str, list]:
        if prompt != "" and prompt != None:
            custom_prompt = [
                {"role": "user", "content": prompt}
            ]
            messages = messages + custom_prompt
        response = self.request_llm(messages)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return (response, messages)
    # =============================================================================
    # d.1.2β RAP用の忘却有りのd.1.2
    # 回答を出力後に入力と一つ前の出力を忘れる
    # =============================================================================
    def talk_llm_history_reset4RAP(self, prompt:str = "", messages:list =[]) -> tuple[str, list]:
        if prompt != "" and prompt != None:
            custom_prompt = [
                {"role": "user", "content": prompt}
            ]
            messages = messages + custom_prompt
        response = self.talk_llm(prompt, messages)
        messages.pop(-2)
        messages.pop(-2)
        return response, messages

    # =============================================================================
    # d.2.1.1 _select_file
    # エクスプローラーでファイルのパスを指定して返す関数
    # import base64
    # =============================================================================
    def select_file(self, path_initial_dir:str=os.path.dirname(os.path.abspath(__file__)))->str:
        root = tk.Tk()#tkウィンドウを開く（エクスプローラーも一緒に開かれる）
        root.withdraw()#tkウィンドウを閉じる
        root.attributes('-topmost', True)  # エクスプローラーウィンドウを最前面に表示する
        file_path = filedialog.askopenfilename(initialdir = path_initial_dir)# ファイルダイアログを開いてファイルを選択
        print("\033[38;2;148;0;211m" + "Input image:",file_path+ "\033[0m")
        return file_path


    # =============================================================================
    # d.2.1.2 _encode_image
    # 画像をエンコードする。
    # base64.b64encode()関数はバイナリデータをbase64にエンコードし、base64.b64decode()関数はbase64エンコードされたデータをデコードします。base64エンコードは、データをテキストとして扱う必要がある場合や、データをテキスト形式で安全に転送する必要がある場合に便利です。例えば、画像データをJSON形式でやり取りする際などがあります。
    # import base64
    # =============================================================================
    def _encode_image(self, image_path:str):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')


    # =============================================================================
    # d.2.2 gpt-4vに回答を申請し，responseとmessageを返す関数
    # =============================================================================
    def talk_llm_vision(self, prompt:str = "", messages:list =[],file_path:str = None) -> tuple[str, list]:
        if isinstance(file_path, str) and file_path != "":
            base64_image =self._encode_image(file_path)
            custom_message = [
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                    ]
                }
            ]
            messages = messages + custom_message
        elif prompt != "" and prompt != None:
            custom_message = [
                {"role": "user", "content": prompt}
            ]
            messages = messages + custom_message
        response = self.request_llm(messages)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )
        return response, messages
    #複数枚画像のリスト入力に対応したVer
    def talk_llm_vision_multiple(self, prompt:str = None, messages:list = [], file_paths:list = []) -> tuple[str, list]:
        if isinstance(file_paths, list) and file_paths != []:
            base64_images = [self._encode_image(fp) for fp in file_paths]
            custom_message = [
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    *[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        } for base64_image in base64_images
                    ]
                ]}
            ]
            messages = messages + custom_message
        elif prompt != "" and prompt != None:
            custom_message = [
                {"role": "user", "content": prompt}
            ]
            messages = messages + custom_message
        response = self.request_llm(messages)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content})
        return response, messages
