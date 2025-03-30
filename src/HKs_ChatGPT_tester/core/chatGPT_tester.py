# ----------------------------------------------------------------------------
# chatGPT_tester.py
# 概要：
# 制作者：堀 和希
# 早稲田大学　基幹理工学部　表現工学科　尾形研究室
# Email: horikazuki28@akane.waseda.jp
# -----------------------------------------------------------------------------

# 基本環境-------------------------------------------------------------
# sys.path を明示する
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
# DIコンテナ環境
from injector import inject
# ---------------------------------------------------------------------

# 自前ファイル---------------------------------------------------------
from ..services.i_LLM_client import ILLMClient
from ..config.i_prompt_presets import IPromptPresets
from ..config.i_settings import ISettings
from .status.i_status_controller import IStatusController
from ..core.i_chat_command_processor import IChatCommandProcessor
#------------------------------------------------------------------------

class ChatGPTTester:
    @inject
    def __init__(
        self,
        settings:ISettings,
        promptPresets:IPromptPresets,
        lLMClient:ILLMClient,
        statusController: IStatusController,
        chatCommandProcessor: IChatCommandProcessor,
        )-> None:

        # 各種クラスのセットアップ
        self.settings = settings
        self.promptPresets = promptPresets
        self.lLMClient = lLMClient
        self.statusController = statusController
        self.chatCommandProcessor = chatCommandProcessor

        # パラメーターのセットアップ
        self.tester_mode = "Standard"

        # ループの開始
        self._start_chatGPT_tester()

    def _start_chatGPT_tester(self):
        while True:
            if self.tester_mode == "Exit":
                exit()
            elif self.tester_mode == "Standard":
                self.tester_mode = self.chatCommandProcessor.conversation_loop()
