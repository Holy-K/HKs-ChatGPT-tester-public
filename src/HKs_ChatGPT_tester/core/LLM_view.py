import os

from .i_llm_view import ILlmView
from ..config.i_settings import ISettings
class LlmView(ILlmView):
    # 起動メッセージを表示する関数
    def print_startup_message(self,settings:ISettings,dict_command:dict):
        # 起動時メッセージの表示
        print("Model:", settings.get_llm_model())
        print("【Hello World! I am "+settings.get_llm_model()+". Ask me anything.】")
        print("【If you input...】")
        #dict_commandを参照し，コマンドリストを表示
        for index,(key,value) in enumerate(dict_command.items(), start=0):
            print("  [", index, "]",value[0])

    # =============================================================================
    # responseを表示
    # =============================================================================
    def print_llm_text(self, lLM_text,settings:ISettings, color_chatgpt="\033[32m", END='\033[0m',)->None:
        print(f"{color_chatgpt}【{settings.get_llm_model()}】{END}")
        print(f"{color_chatgpt}{lLM_text}{END}","\n")

    # =============================================================================
    # ターンバーを表示（例：turn 1==================）
    # =============================================================================
    def print_turnBar(self, count_turn)->None:
        print("Turn", count_turn, end=" ")
        width = os.get_terminal_size().columns-len("\nTurn"+str(count_turn))-1
        for i in range(width):
            print("=", end="")
