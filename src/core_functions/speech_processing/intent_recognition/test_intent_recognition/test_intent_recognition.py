from ..intent_recognition import LuisIntentRecognition
import configuration.secrets.key_vault as key_vault
import unittest

class TestIntentRecogniton(unittest.TestCase):
    
    def setUp(self):
        self.api_keys = {'luis_app_id': key_vault.retrieve_secret('LUIS-App-ID'), 'luis_key': key_vault.retrieve_secret('LUIS-API')}
        self.luis = LuisIntentRecognition(self.api_keys)
        self.speech = "Open google"
        self.intent = "Open_Website"
        
    def test_user_intent(self):
        intents_json = self.luis.get_user_intent(self.speech)
        top_intent = intents_json["prediction"]["topIntent"]
        self.assertEqual(top_intent, self.intent)
        
if __name__ == '__main__':
    unittest.main()