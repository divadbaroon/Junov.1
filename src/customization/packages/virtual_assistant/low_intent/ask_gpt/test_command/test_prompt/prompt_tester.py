import json
import os
from configuration.secrets import config
from src.utilities.settings.master_settings.master_settings_manager import BotSettingsManager
from src.customization.packages.virtual_assistant.low_intent.ask_gpt.ask_gpt import AskGPT

# Relative path to mock_prompt.json file
mock_prompt_path = os.path.join('src/components/commands/ask_gpt/test_command/test_prompt/mock_prompt.json')

class TestPrompt:
    """A class for testing prompts on the AskGPT command"""
    
    def __init__(self):
        self.openai_key = config.retrieve_secret('OpenAI-API')
        self.master_settings = BotSettingsManager()
        self.bot_name = self.master_settings.retrieve_property('bot_name')
        
        #self.prompt = self._read_prompt()
        self.prompt = f"You are a helpful virtual assistant named Sarah. Keep your responses concise yet informative to the user."
        self.ask_gpt = AskGPT(self.openai_key, self.master_settings, self.bot_name, self.prompt)
        
    def _ask_GPT(self):
        response = self.ask_gpt.ask_GPT(speech='What are your thoughts on climate change?', model='gpt-4', manual_request=True)
        return response
    
    def _read_prompt(self):
        with open(mock_prompt_path, 'r') as file:
            data = json.load(file)
        return data["prompt"]
            
if __name__ == '__main__':
    test_prompt = TestPrompt()
    print(test_prompt._ask_GPT())