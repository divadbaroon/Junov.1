import azure.cognitiveservices.speech as speechsdk
from ..speech_recognizer import SpeechRecognition
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.utilities.settings.voice_settings.voice_settings_manager import VoiceSettingsManager
import configuration.secrets.key_vault as key_vault

class ManuallyTestSpeechRecognition():
	"""Performs a one shot manual test of the speech recognizer"""
 
	def __init__(self) -> None:
     
		self.master_settings = MasterSettingsManager()
		self.voice_settings = VoiceSettingsManager()
  
		# Language country code is used for speech recognizer initialization 
		language = self.master_settings.retrieve_property('language')
		language_country_code = self.voice_settings.retrieve_language_country_code(language)
  
		# API keys are retrieved from the config file with only necessary keys being retrieved
		self.api_keys = {'cognitive_services_api': key_vault.retrieve_secret('Cognitive-Services-API'), 'region': 'eastus', 'translator_key': key_vault.retrieve_secret('Translator-API')}
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		self._setup_speech_and_audio(self.api_keys['cognitive_services_api'], self.api_keys['region'], language_country_code)
  
		self.speech_recognition = SpeechRecognition(self.speech_recognizer, self.speech_config, self.master_settings, self.api_keys)
		
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