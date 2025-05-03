# 基本環境-------------------------------------------------------------
import os
script_dir = os.path.dirname(__file__)
# DIコンテナ環境;
from injector import inject
# ---------------------------------------------------------------------
# 標準・外部ライブラリ-----------------------------------------------------
import datetime
# --------------------------------------------------------------------
# 自前ファイル--------------------------------------------------------
from .status.i_status_controller import IStatusController
from .i_llm_view import ILlmView
from ..services.i_llm_client import ILlmClient
from ..config.i_prompt_presets import IPromptPresets
from ..config.i_settings import ISettings
# --------------------------------------------------------------------
class ChatCommandProcessor():
    @inject
    def __init__(
        self,
        statusController:IStatusController,
        settings:ISettings,
        llmClient:ILlmClient,
        llmView:ILlmView,
        promptPresets:IPromptPresets=None,
        ):
        self.statusController = statusController
        self.settings = settings
        if promptPresets:
            self.promptPresets = promptPresets
        self.llmClient = llmClient
        self.lLMView =llmView
        self.dict_command = {
            "COMMAND_EXIT": ["Exit", self._exit_program],
            "COMMAND_SAVE_MESSAGES_TO_EXCEL": ["Save messages to Excel", self._ask_save_logs2excel],
            "COMMAND_RE_GENERATE_RESPONSE": ["Regenerate response", self._regenerate_response],
            "COMMAND_SHOW_MESSAGES": ["Show messages", self._show_messages],
            "COMMAND_SHOW_FULL_RESPONSE": ["Show full response", self._show_full_response],
            "COMMAND_INPUT_WITH_IMAGE": ["Input prompt with image", self._input_with_image],
            "COMMAND_INPUT_PROMPT_PRESET": ["Input prompt preset", self._input_prompt_preset],
            "COMMAND_INPUT_MESSAGE_PRESET": ["Input message preset", self._input_message_preset],
        }
        self.order_dict_command = list(self.dict_command)
    def conversation_loop(self) -> str:
        self.tester_mode_change = None
        self.lLMView.print_startup_message(self.settings,self.dict_command)
        while self.tester_mode_change == None:
            self.lLMView.print_turnBar(self.statusController.statusPackage.statusStandard.get_turn())
            print("【You】")
            input_text = input()
            self._handle_command_input(input_text)#TODOデバッグが終わったら戻す
            # try:
            #     self._handle_command_input(input_text)
            # except Exception as e:
            #     print("\033[31m" + "Error: " + str(e) + '\033[0m')
            #     print("Error is occurred in conversation_loop()")
            #     self._ask_save_logs2excel()
        return self.tester_mode_change

    def _handle_command_input(self, input_text):
        if input_text.isdigit():
            input_index = int(input_text)
            if 0 <= input_index < len(self.order_dict_command):
                command = self.order_dict_command[input_index]
                if command:
                    print(f"Command recognized: {command}")
                    self._execute_command(command)
                else:
                    print("Unrecognized command.")
            else:
                print("Input index out of range." + "Please enter a number between 0 and " + str(len(self.order_dict_command) - 1))
        else:
            self._normal_process(input_text)

    def _execute_command(self, command):
        # 各コマンドに対する処理をここに追加
        action = self.dict_command.get(command)[1]
        if action:
            action()
        else:
            print("No action defined for this command.")

    # =============================================================================
    # 通常処理
    # =============================================================================
    def _normal_process(self,prompt=None,messages=None):
        if prompt is None:
            prompt = self.statusController.statusPackage.statusStandard.get_prompt()
        if messages is None:
            messages = self.statusController.statusPackage.statusStandard.get_messages()
        time = datetime.datetime.now()
        if self.statusController.statusPackage.statusStandard.get_path_input_image() in [None,'']:
            response, messages = self.llmClient.talk_llm(prompt, messages,)
        else:
            response, messages = self.llmClient.talk_llm_vision_multiple(
                        prompt,
                        messages,
                        [self.statusController.statusPackage.statusStandard.get_path_input_image()],

                    )
        response_time = datetime.datetime.now() - time
        self.lLMView.print_llm_text(self.llmClient.extract_answer_text_from_response(response),self.settings)
        self.statusController.processing_at_end_of_turn(prompt, response, messages,response_time = response_time)

    # =============================================================================
    # コマンド処理
    # =============================================================================
    #プログラムを終了
    def _exit_program(self):
        if hasattr(self.statusController, 'log') and len(self.statusController.log) >= 1:
            self.statusController.update_status_end()
        self._ask_save_logs2excel()
        print("Exiting program...")
        self.tester_mode_change = "Exit"

    # ログをExcelに保存するかどうかを確認する関数
    def _ask_save_logs2excel(self):
        datetime = self.statusController.statusPackage.statusStandard.get_date_time()
        self.statusController.ask_save_logs2excel(self.settings.get_path_log_excel_file(),datetime)

    # レスポンスを再生成する関数
    def _regenerate_response(self):
        if len(self.statusController.statusPackage.statusStandard.get_messages()) >= 2:
            del self.statusController.statusPackage.statusStandard.messages[-2]
            time = datetime.datetime.now()
            response, messages = self.llmClient.talk_llm(
                self.statusController.statusPackage.statusStandard.get_prompt(),
                self.statusController.statusPackage.statusStandard.get_messages(),
            )
            response_time = datetime.datetime.now() - time
            self.lLMView.print_llm_text(self.llmClient.extract_answer_text_from_response(response),self.settings)
            self.statusController.processing_at_end_of_turn(response = response, messages = messages, response_time = response_time)
        else:
            print("\033[31m"+"Error: There are no message."+'\033[0m')

    # メッセージを表示する関数
    def _show_messages(self):
        print(self.statusController.statusPackage.statusStandard.get_messages())

    # 完全なレスポンスを表示する関数
    def _show_full_response(self):
        print(self.statusController.statusPackage.statusStandard.get_detailed_response())

    # 画像を伴う入力を処理する関数
    def _input_with_image(self):
        while True:
            path_initial_image_directory = self.settings.get_initial_image_directory()
            path_input_image=self.llmClient.select_file(path_initial_image_directory)
            if path_input_image=="":
                print("\033[31m"+"Error!!"+'\033[0m',"File not selected. Would you like to retry selecting the file?(y/n)")
                while True:
                    _yn = input()
                    if _yn=="y":
                        break
                    elif _yn=="n":
                        break
                    else:
                        print("\033[31m"+"Error!!"+'\033[0m',"Input correct key(y/n)")
                        continue
                if _yn=="y":
                    continue
            break
        self.statusController.statusPackage.statusStandard.set_path_input_image(path_input_image)
    # プロンプトプリセットを入力する関数
    def _input_prompt_preset(self):
        if not self.promptPresets or not self.promptPresets.get_prompt_presets():
            print("No prompt has been registered")
            return

        # prompt presetの一覧を表示
        print("[ 0 ] Cancel input prompt preset")
        for index, preset in enumerate(self.promptPresets.get_prompt_presets()):
            print(f"[ {index + 1} ] {preset['name']}")
        max_index = len(self.promptPresets.get_prompt_presets())
        print(f"Input preset number [0-{max_index}] (0 to cancel)")

        # prompt presetを選択
        prompt = None
        while True:
            index = int(input("Enter the index of the prompt preset: "))
            if index == 0:
                print("Prompt preset input canceled.")
                return
            elif 1 <= index <= max_index:
                selected_preset = self.promptPresets.get_prompt_presets()[index - 1]
                print(f"Selected preset: {selected_preset['name']}")
                print(selected_preset['prompt'])
                prompt = selected_preset['prompt']
                break
            else:
                print("\033[31m" + "Error: Invalid index." + '\033[0m')

        self._normal_process(prompt)


    # message presetを入力する関数
    def _input_message_preset(self):
        if not self.promptPresets or not self.promptPresets.message_presets:
            print("No message has been registered")
            return

        # message presetの一覧を表示
        print("[ 0 ] Cancel input message preset")
        for index, preset in enumerate(self.promptPresets.message_presets):
            print(f"[ {index + 1} ] {preset['name']}")
        max_index = len(self.promptPresets.message_presets)
        print(f"Input message number [0-{max_index}] (0 to cancel)")

        # message presetを選択
        messages = None
        while True:
            index = int(input("Enter the index of the message preset: "))
            if index == 0:
                print("Message preset input canceled.")
                return
            elif 1 <= index <= max_index:
                selected_preset = self.promptPresets.message_presets[index - 1]
                print(f"Selected preset: {selected_preset['name']}")
                print(selected_preset['message'])
                messages = selected_preset['message']
                break
            else:
                print("\033[31m" + "Error: Invalid index." + '\033[0m')
