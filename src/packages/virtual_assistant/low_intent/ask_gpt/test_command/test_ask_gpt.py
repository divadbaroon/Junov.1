import unittest
from configuration.secrets import config
from src.utils.settings.master_settings.master_settings_manager import BotSettingsManager
from src.packages.virtual_assistant.low_intent.ask_gpt.ask_gpt import AskGPT

class TestAskGPT(unittest.TestCase):
    """Class for testing the AskGPT command"""

    def setUp(self):
        self.openai_key = config.retrieve_secret('OpenAI-API')
        self.master_settings = BotSettingsManager()
        self.bot_name = self.master_settings.retrieve_property('name')
        
        self.ask_gpt = AskGPT(self.openai_key, self.master_settings, self.bot_name)
        self.ask_gpt_incorrect = AskGPT("wrong_key", self.master_settings, self.bot_name)
        
    def test_ask_GPT(self):
        response = self.ask_gpt.ask_GPT("What are you?")
        self.assertNotEqual(response, "Sorry, I am currently experiencing technical difficulties. Please try again later.")

    def test_ask_GPT_with_incorrect_key(self):
        # Use a wrong key to provoke an error
        response = self.ask_gpt_incorrect.ask_GPT("What are you?")
        self.assertEqual(response, "Sorry, I am currently experiencing technical difficulties. Please try again later.")
        
if __name__ == '__main__':
    unittest.main()
