import datetime

class StatusStandard:
    def __init__(self):
        # Standard
        self.date = datetime.datetime.now()

        # GPT Experiment
        self.messages: list = []
        self.LLM_model: str = ""
        self.temperature: float = None
        self.turn :int= 1
        self.prompt: str = ""
        self.answer_text: str = ""
        self.detailed_response = dict
        self.prompt_tokens: int = 0
        self.answer_text_tokens: int = 0
        self.total_tokens: int = 0
        self.path_input_image: str = None
        self.response_time: float = 0.0

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_messages(self):

        return self.messages

    def set_messages(self, messages):
        self.messages = messages

    def add_response2messages(self,response):
        self.messages.append(response)

    def get_LLM_model(self):
        return self.LLM_model

    def set_LLM_model(self, LLM_model):
        self.LLM_model = LLM_model

    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def increase_turn(self):
        """
        Increase the turn number by one.

        Returns
        -------
        None
        """

        self.turn += 1

    def get_prompt(self):
        return self.prompt

    def set_prompt(self, prompt):
        self.prompt = prompt

    def get_answer_text(self):
        return self.answer_text

    def set_answer_text(self, answer_text):
        self.answer_text = answer_text

    def get_detailed_response(self):
        return self.detailed_response

    def set_detailed_response(self, detailed_response):
        self.detailed_response = detailed_response

    def get_prompt_tokens(self):
        return self.prompt_tokens

    def set_prompt_tokens(self, prompt_tokens):
        self.prompt_tokens = prompt_tokens

    def get_answer_text_tokens(self):
        return self.answer_text_tokens

    def set_answer_test_tokens(self, answer_text_tokens):
        self.answer_text_tokens = answer_text_tokens

    def get_total_tokens(self):
        return self.total_tokens

    def set_total_tokens(self, total_tokens):
        self.total_tokens = total_tokens

    def get_path_input_image(self):
        return self.path_input_image

    def set_path_input_image(self, path_input_image):
        self.path_input_image = path_input_image

    def get_response_time(self):
        return self.response_time

    def set_response_time(self, response_time):
        self.response_time = response_time
