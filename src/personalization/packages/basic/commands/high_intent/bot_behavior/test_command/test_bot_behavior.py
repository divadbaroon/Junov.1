import unittest
from unittest.mock import Mock, patch
from src.personalization.packages.basic.high_intent.bot_behavior.bot_behavior import BotBehavior

class TestBotBehavior(unittest.TestCase):
    """Class for testing the AskGPT command"""
    
    def setUp(self):
        self.speech_verbalizer = Mock()
        self.bot_behavior = BotBehavior(self.speech_verbalizer)
        self.bot_behavior.master_settings = Mock()  # replace SettingsOrchestrator with a mock
        
    def test_mute(self):
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = False
        response = self.bot_behavior.mute()
        self.bot_behavior.master_settings.save_bot_property.assert_called_once_with('mute_status', True)
        self.assertEqual(response, 'I am now muted.')
        
    def test_unmute(self):
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = True
        response = self.bot_behavior.unmute()
        self.bot_behavior.master_settings.save_bot_property.assert_called_once_with('mute_status', False)
        self.assertEqual(response, 'I am now unmuted.')
        
    @patch('builtins.input', return_value='')
    def test_pause(self, mock_input):
        response = self.bot_behavior.pause()
        self.assertEqual(response, 'I am unpaused')
        
    def test_change_role(self):
        new_role = 'new_role'
        response = self.bot_behavior.change_role(new_role)
        self.bot_behavior.master_settings.save_bot_property.assert_called_once_with('role', new_role)
        self.assertEqual(response, f'Ok, I have changed my role to {new_role}.')

    def test_change_gender(self):
        new_gender = 'male'
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = 'English'
        response = self.bot_behavior.change_gender(new_gender)
        self.bot_behavior.master_settings.save_bot_property.assert_any_call('gender', new_gender)
        self.assertEqual(response, f'Ok, I have changed my gender to {new_gender}.')

    def test_change_language(self):
        new_language = 'Spanish'
        self.bot_behavior.master_settings.retrieve_available_languages.return_value = ['spanish', 'english']
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = 'male'
        response = self.bot_behavior.change_language(new_language)
        self.bot_behavior.master_settings.save_bot_property.assert_any_call('language', new_language.lower())
        self.assertEqual(response, f'Ok, I have changed my language to {new_language}.')


    def test_change_voice(self):
        voices = ['voice1', 'voice2']
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = 'voice1'
        self.bot_behavior.master_settings.retrieve_voice_names.return_value = voices
        response = self.bot_behavior.change_voice()
        self.assertEqual(response, 'Ok, I have changed my voice.')

    def test_randomize_voice(self):
        voices = ['voice1', 'voice2']
        self.bot_behavior.master_settings.retrieve_bot_property.return_value = 'voice1'
        self.bot_behavior.master_settings.retrieve_voice_names.return_value = voices
        response = self.bot_behavior.randomize_voice()
        self.assertEqual(response, 'Ok, I have changed to a random voice.')
    
if __name__ == '__main__':
    unittest.main()
