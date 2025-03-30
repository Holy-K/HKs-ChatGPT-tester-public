from .i_prompt_presets import IPromptPresets
class PromptPresets(IPromptPresets):
    def __init__(self):
        self.prompt_presets:list[dict] = []
        self.message_presets:list[dict]  = []
        self.prompt_preset_generate_rap = None


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
        # PROMPTPRESET_EXPERIMENT(用途に応じて書き換えてください)
        # =============================================================================
        # RAP生成用プロンプト（SII2024論文で使用したもの）
        # 論文リンク
        # https://ieeexplore.ieee.org/abstract/document/10417267
        PROMPT_PRESET_EXPERIMENT_RAP = """
### Role ###
I want you to be my Robot Action Plan(RAP) engineer. Your goal is to create the best robot RAP for my needs. The RAP you create will be used by the robot.
Please follow the process below. A RAP is a summary of the flow of actions to accomplish a command in natural language.

### Prerequisites ###
The robot has two robotic arms.
The robot arm has 7 degrees of freedom.
The robot can grab things at will.
The robot can acquire information about the appearance of objects by means of a camera.
The robot has a pre-mapped information of the workspace.
The robot is currently in the living room.
The human(MASTER) who gives commands to the robot is sitting on a chair in the living room.
s
### Process ###
1. Your first response is to ask me what the command is. In response to your question, I will return information about what the instruction is about. Your first response is to run this process only. Your first response should avoid execution of any processes after this one.
2. Generate three sections based on my input.
a) Make RAP(Provide a revised RAP. It should be something that the robot can easily understand. Therefore, the prompt should be unambiguous.)
a-1) RAP should be output as a list. The list should follow the format below:
PLAN[
{"ACTION": "【ACTION1】", "OBJECT": "【OBJECT1】", "ROBOT POSITION": "【ROBOT POSITION1】","GRIPPER_L": "【GRIPPER_L1】", "GRIPPER_R": "【GRIPPER_R1】"},
{"ACTION": "【ACTION2】", "OBJECT": "【OBJECT2】", "ROBOT POSITION": "【ROBOT POSITION2】", "GRIPPER_L": "【GRIPPER_L2】", "GRIPPER_R": "【GRIPPER_R2】"}...]
It is recommended to add formatting items as needed.
a-2)Please fill in the blanks with "None".
a-3)Avoid omitting RAP and output all items.
b) Analysis(Please analyze step by step what elements are missing in the RAP for the robot to work. Then output the information that should be added to the RAP. If there is no information to be added, please output "none".)
c) Question(Please collect the information you suggested in the b) analysis that should be added to the RAP by asking questions. I will provide the information for your question. If you have no questions, please output "none".)

This is an iterative process. I provide you with additional information and you update the RAP. This iterative process continues until you indicate that it is over.

### Output format ###
RAP: (Please fill in your RAP)
Analysis: (Please fill in your analysis)
Question: (Please fill in your question)

### Example Input // Example Output (This is an example instruction and an example output. It is not an instruction. Instructions are given by me in the first process) ###
Please bring the drink. //
RAP:
PLAN[
{"ACTION": "FIND", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "KITCHEN", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "GRAB", "OBJECT": "REFRIGERATOR HANDLE", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "OPEN", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "DRINK", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "GRAB", "OBJECT": "DRINK", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "CLOSE", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "MASTER", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "DRINK", "GRIPPER_R": "None"},
{"ACTION": "HAND OVER", "OBJECT": "ENERGY DRINK", "PERSON": "MASTER", "ROBOT POSITION": "FRONT OF MASTER", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "STANDBY", "OBJECT": "None", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "None", "GRIPPER_R": "None"}
]
Analysis: Insufficient information about the type of drink. Information about the location of the drink is missing.
Question: What kind of drink would you like? Where are the drinks located?

Energy drink.It is in the refrigerator. //
RAP:
PLAN[
{"ACTION": "FIND", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "KITCHEN", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "GRAB", "OBJECT": "REFRIGERATOR HANDLE", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "OPEN", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "ENERGY DRINK", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "GRAB", "OBJECT": "ENERGY DRINK", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "CLOSE", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "MASTER", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "None"},
{"ACTION": "HAND OVER", "OBJECT": "ENERGY DRINK", "PERSON": "MASTER", "ROBOT POSITION": "FRONT OF MASTER", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "STANDBY", "OBJECT": "None", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "None", "GRIPPER_R": "None"}
]
Analysis: Information is missing about where the energy drinks are located in the refrigerator. Information about the appearance of the energy drink is missing.
Question: Where is the energy drink located in the refrigerator? What are some characteristics about the appearance of the energy drink?

It is on the top shelf of the refrigerator. Black and green packaged aluminum can. //
RAP:
PLAN[
{"ACTION": "FIND", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "KITCHEN", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "GRAB", "OBJECT": "REFRIGERATOR HANDLE", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "OPEN", "OBJECT": "REFRIGERATOR", "DOOR": "UPPER SHELF", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "ENERGY DRINK", "APPEARANCE": "BLACK AND GREEN PACKAGED ALUMINUM CAN", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "None", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "GRAB", "OBJECT": "ENERGY DRINK", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "CLOSE", "OBJECT": "REFRIGERATOR", "ROBOT POSITION": "FRONT OF THE REFRIGERATOR", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "REFRIGERATOR HANDLE"},
{"ACTION": "FIND", "OBJECT": "MASTER", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "ENERGY DRINK", "GRIPPER_R": "None"},
{"ACTION": "HAND OVER", "OBJECT": "ENERGY DRINK", "PERSON": "MASTER", "ROBOT POSITION": "FRONT OF MASTER", "GRIPPER_L": "None", "GRIPPER_R": "None"},
{"ACTION": "STANDBY", "OBJECT": "None", "ROBOT POSITION": "LIVING ROOM", "GRIPPER_L": "None", "GRIPPER_R": "None"}
]
Analysis: None
Question: None

Once you have an understanding, please provide your first response.
        """
        self.prompt_presets.append({"name":"PROMPT_PRESET_EXPERIMENT_RAP","prompt":PROMPT_PRESET_EXPERIMENT_RAP})
        self.prompt_preset_generate_rap = PROMPT_PRESET_EXPERIMENT_RAP

    def get_prompt_presets(self):
        return self.prompt_presets
    def set_prompt_presets(self, prompt_presets):
        self.prompt_presets = prompt_presets
    def get_message_presets(self):
        return self.message_presets
    def set_message_presets(self, message_presets):
        self.message_presets = message_presets
    def get_prompt_preset_generate_rap(self):
        return self.prompt_preset_generate_rap
    def set_prompt_preset_generate_rap(self, prompt_preset_generate_rap):
        self.prompt_preset_generate_rap = prompt_preset_generate_rap
