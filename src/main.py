from src.HKs_ChatGPT_tester.config.dependency_gemini import DependencyGemini
from src.HKs_ChatGPT_tester.config.dependency import Dependency
from src.HKs_ChatGPT_tester.core.chatGPT_tester import ChatGPTTester
if __name__ == "__main__":
    injector = DependencyGemini()
    chatgpt_tester = injector.resolve(ChatGPTTester)
