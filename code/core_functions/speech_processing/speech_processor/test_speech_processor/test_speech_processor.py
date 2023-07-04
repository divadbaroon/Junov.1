import unittest
from unittest.mock import MagicMock
from code.core_functions.speech_processing.speech_processor.speech_processor import SpeechProcessor
import configuration.secrets.config as config

class TestSpeechProcessor(unittest.TestCase):

	def setUp(self):
		# Retrieving the bot's secret values from Azure Key Vault
		# Storing the bot's secret values in a hash map for ease of use
		self.api_keys = {}
		self._load_api_keys()
		self.bot_settings = MagicMock()
		self.speech_verbalizer = MagicMock()
		self.speech_processor = SpeechProcessor(self.api_keys, self.bot_settings)
  
	def _load_api_keys(self):
		"""Retrieving the bot's secret values from Azure Key Vault
  		   and storing the bot's secret values in a hash map for ease of use"""
		self.api_keys['region'] = 'eastus'
		self.api_keys['cognitive_services_api'] = config.retrieve_secret('Cognitive-Services-API')
		self.api_keys['luis_app_id'] = config.retrieve_secret('LUIS-App-ID')
		self.api_keys['luis_key'] = config.retrieve_secret('LUIS-API')
		self.api_keys['openai_key'] = config.retrieve_secret('OpenAI-API')
		self.api_keys['weather_key'] = config.retrieve_secret('Weather-API')
		self.api_keys['translator_key'] = config.retrieve_secret('Translator-API')
		self.api_keys['elevenlabs_api_key'] = config.retrieve_secret('Elevenlabs-API-Key')

	def test_process_speech(self):
		speech = "Open Google"
		expected_response = "Opening "
		self.speech_verbalizer.verbalize_speech.return_value = expected_response
		self.bot_settings.retrieve_bot_property.return_value = "open google"

		result = self.speech_processor.process_speech(speech, self.speech_verbalizer)

		self.assertEqual(result, expected_response)
		self.speech_verbalizer.verbalize_speech.assert_called_once_with(expected_response)
		self.bot_settings.retrieve_bot_property.assert_called_once_with("open google")

if __name__ == '__main__':
	unittest.main()
