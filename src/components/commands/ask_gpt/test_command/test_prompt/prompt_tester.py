import json
import os
from configuration.secrets import config
from settings.settings_manager import SettingsOrchestrator
from src.components.commands.ask_gpt.ask_gpt import AskGPT

# Relative path to mock_prompt.json file
mock_prompt_path = os.path.join('src/components/commands/ask_gpt/test_command/test_prompt/mock_prompt.json')

class TestPrompt:
    """A class for testing prompts on the AskGPT command"""
    
    def __init__(self):
        self.openai_key = config.retrieve_secret('OpenAI-API')
        self.bot_settings = SettingsOrchestrator()
        self.bot_name = self.bot_settings.retrieve_bot_property('bot_name')
        
        self.prompt = self._read_prompt()
        self.ask_gpt = AskGPT(self.openai_key, self.bot_settings, self.bot_name, self.prompt)
        
    def _ask_GPT(self):
        response = self.ask_gpt.ask_GPT('Hi, what are you?')
        return response
    
    def _read_prompt(self):
        with open(mock_prompt_path, 'r') as file:
            data = json.load(file)
        return data["prompt"]
            
if __name__ == '__main__':
    test_prompt = TestPrompt()
    print(test_prompt._ask_GPT())