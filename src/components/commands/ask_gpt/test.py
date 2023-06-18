from src.components.commands.ask_gpt.ask_gpt import AskGPT
from configuration.secrets import config
from settings.settings_orchestrator import SettingsOrchestrator

class TestAskGPT:
    """Class for testing the AskGPT command"""
    
    def __init__(self):
        self.openai_key = config.retrieve_secret('OpenAI-API')
        self.bot_settings = SettingsOrchestrator()
        self.bot_name = self.bot_settings.retrieve_bot_property('bot_name')
        
        self.ask_gpt = AskGPT(self.openai_key, self.bot_settings, self.bot_name)
        self.ask_gpt_incorrect = AskGPT("wrong_key", self.bot_settings, self.bot_name)
        
    def _ask_GPT(self):
        response = self.ask_gpt.ask_GPT("What are you?")
        print(response)

    def _ask_GPT_with_incorrect_key(self):
        # Use a wrong key to provoke an error
        response = self.ask_gpt_incorrect.ask_GPT("What is the capital of France?")
        print(response)
        
if __name__ == '__main__':
    new_test = TestAskGPT()
    new_test._ask_GPT()
    new_test._ask_GPT_with_incorrect_key()