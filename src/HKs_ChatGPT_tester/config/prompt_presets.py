from .i_prompt_presets import IPromptPresets
class PromptPresets(IPromptPresets):
    def __init__(self):
        self.prompt_presets:list[dict] = []
        self.message_presets:list[dict]  = []


        # =============================================================================
        # PROMPT_PRESET_1(用途に応じて書き換えてください)
        # =============================================================================
        PROMPT_PRESET_1 = """
This is a sample prompt. You can register your favorite prompts as presets by editing prompt_presets.py.
"""
        self.prompt_presets.append({"name":"PROMPT_PRESET_1","prompt":PROMPT_PRESET_1})

        # =============================================================================
        # PROMPT_PRESET_2(用途に応じて書き換えてください)
        # =============================================================================
        PROMPT_PRESET_2 = """
This is a sample prompt. You can register your favorite prompts as presets by editing prompt_presets.py.
        """
        self.prompt_presets.append({"name":"PROMPT_PRESET_2","prompt":PROMPT_PRESET_2})

        # =============================================================================
        # PROMPT_PRESET_3(用途に応じて書き換えてください)
        # =============================================================================
        PROMPT_PRESET_3 = """
This is a sample prompt. You can register your favorite prompts as presets by editing prompt_presets.py.
        """
        self.prompt_presets.append({"name":"PROMPT_PRESET_3","prompt":PROMPT_PRESET_3})
        # =============================================================================
        # MESSAGE_PRESET(用途に応じて書き換えてください)
        # =============================================================================
        MESSAGE_PRESET_1 = [{'role': 'user', 'content': 'hi'}, {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}]
        self.message_presets.append({"name":"MESSAGE_PRESET_1","message":MESSAGE_PRESET_1})
        # =============================================================================
        # PROMPT_PRESET_EXPERIMENT(用途に応じて書き換えてください)
        # =============================================================================

    def get_prompt_presets(self):
        return self.prompt_presets
    def set_prompt_presets(self, prompt_presets):
        self.prompt_presets = prompt_presets
    def get_message_presets(self):
        return self.message_presets
    def set_message_presets(self, message_presets):
        self.message_presets = message_presets
