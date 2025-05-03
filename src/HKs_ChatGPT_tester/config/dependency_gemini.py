# 参考：https://qiita.com/Jazuma/items/9fa15b36f61f9d1e770c
# 基本環境-------------------------------------------------------------
# DIコンテナ環境
from injector import Injector
# ---------------------------------------------------------------------

# 自前ファイル--------------------------------------------------------
from ..core.i_chat_command_processor import IChatCommandProcessor
from ..core.chat_command_processor import ChatCommandProcessor
from ..core.i_llm_view import ILlmView
from ..core.llm_view import LlmView
from ..core.status.i_status_controller import IStatusController
from ..core.status.i_status_package import IStatusPackage
from ..core.status.status_controller_standard import StatusControllerStandard
from ..core.status.status_package_standard import StatusPackageStandard

from ..services.i_llm_client import ILlmClient
from ..services.gemini_client import GeminiClient

from ..config.i_prompt_presets import IPromptPresets
from ..config.i_settings import ISettings
from ..config.i_dependency import IDependency
from ..config.prompt_presets import PromptPresets
from ..config.settings_from_user_config_json import SettingsFromUserConfigJson
# --------------------------------------------------------------------

class DependencyGemini(IDependency):
    """依存関係の定義を記載, DIコンテナの定義を記載"""
    def __init__(self):
        # 依存関係を設定する関数を読み込む
        self.injector = Injector(self.__class__.bind_config)

    @classmethod
    def bind_config(cls, binder):
        # coreパッケージの依存関係
        binder.bind(IChatCommandProcessor, ChatCommandProcessor)
        binder.bind(IStatusController, StatusControllerStandard)
        binder.bind(IStatusPackage, StatusPackageStandard)
        binder.bind(ILlmView, LlmView)

        # configパッケージの依存関係
        settings = SettingsFromUserConfigJson ("src/hks_chatgpt_tester/user_config.json")
        binder.bind(ISettings, settings)
        binder.bind(IPromptPresets, PromptPresets)

        # servicesパッケージの依存関係
        binder.bind(ILlmClient, GeminiClient)

    def resolve(self, cls):
        return self.injector.get(cls)
