import azure.cognitiveservices.speech as speechsdk
from ..speech_recognizer import SpeechRecognition
from settings.settings_manager import SettingsOrchestrator
import configuration.secrets.config as config

class ManuallyTestSpeechRecognition():
	"""Performs a one shot manual test of the speech recognizer"""
 
	def __init__(self) -> None:
     
		self.bot_settings = SettingsOrchestrator()
  
		# Language country code is used for speech recognizer initialization 
		language = self.bot_settings.retrieve_bot_property('language')
		language_country_code = self.bot_settings.get_language_country_code(language)
  
		# API keys are retrieved from the config file with only necessary keys being retrieved
		self.api_keys = {'cognitive_services_api': config.retrieve_secret('Cognitive-Services-API'), 'region': 'eastus', 'translator_key': config.retrieve_secret('Translator-API')}
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		self._setup_speech_and_audio(self.api_keys['cognitive_services_api'], self.api_keys['region'], language_country_code)
  
		self.speech_recognition = SpeechRecognition(self.speech_recognizer, self.speech_config, self.bot_settings, self.api_keys)
		
	def _setup_speech_and_audio(self, cognitive_services_api, region, language_country_code):
		"""Initializes the bot's audio configuration, speech configuration, and speech recognizer"""
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_config = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config, language=language_country_code)
		
	def test_speech_recogniton(self):
		self.speech_recognition.listen()
		
if __name__ == '__main__':
	test = ManuallyTestSpeechRecognition()
	test.test_speech_recogniton()