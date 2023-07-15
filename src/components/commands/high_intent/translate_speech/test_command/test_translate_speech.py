import unittest
from configuration.secrets import config
from src.components.commands.translate_speech.translate_speech import TranslateSpeech

class TestTranslateSpeech(unittest.TestCase):
    """Class for testing the TranslateSpeech command"""
    
    def setUp(self):
        self.translator_key = config.retrieve_secret('Translator-API')
        self.translator = TranslateSpeech(self.translator_key)
        self.translator_incorrect = TranslateSpeech("wrong key")
        
    def test_translator(self):
        response = self.translator.translate_speech("Hello", "English", "Spanish", one_shot_translation=True)
        self.assertEqual(response, "Hola")

    def test_translator_with_incorrect_key(self):
        response = self.translator_incorrect.translate_speech("Hello", "English", "Spanish", one_shot_translation=True)
        self.assertEqual(response, 'Sorry, there was an error while trying to translate: Hello. Try asking again.')
        
if __name__ == '__main__':
    unittest.main()
