from src.hks_chatgpt_tester.config.dependency_gemini import DependencyGemini
from src.hks_chatgpt_tester.config.dependency import Dependency
from src.hks_chatgpt_tester.core.chatgpt_tester import ChatgptTester
if __name__ == "__main__":
    injector = Dependency()
    chatgpt_tester = injector.resolve(ChatgptTester)
