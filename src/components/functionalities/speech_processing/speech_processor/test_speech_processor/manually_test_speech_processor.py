import azure.cognitiveservices.speech as speechsdk
from ..speech_processor import SpeechProcessor
from src.components.functionalities.speech_verbalization.speech_verbalizer import SpeechVerbalizer
from settings.settings_manager import SettingsOrchestrator
import configuration.secrets.config as config

class ManuallyTestSpeechProcessor():
	"""Performs a one shot test of the SpeechProcessor class"""
 
	def __init__(self) -> None:
     
		self.bot_settings = SettingsOrchestrator()
  
		# Language country code is used for speech recognizer initialization 
		language = self.bot_settings.retrieve_bot_property('language')
		language_country_code = self.bot_settings.get_language_country_code(language)
  
		# Retrieving the bot's secret values from Azure Key Vault
		self.api_keys = {}
		self._load_api_keys() 
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		self._setup_speech_and_audio(self.api_keys['cognitive_services_api'], self.api_keys['region'], language_country_code)
  
		self.speech_verbalizer  = SpeechVerbalizer(self.api_keys, self.bot_settings, self.speech_synthesizer, self.speech_config, self.audio_config)
        
		self.speech_processor = SpeechProcessor(self.api_keys, self.bot_settings)
  
	def _setup_speech_and_audio(self, cognitive_services_api, region, language_country_code):
		"""Initializes the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer"""
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_config = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config, language=language_country_code)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  
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
		
	def test_speech_processor(self, speech):
		response = self.speech_processor.process_speech(speech, self.speech_verbalizer)
		print(response)
		
if __name__ == '__main__':
	test = ManuallyTestSpeechProcessor()
	test.test_speech_processor("Open google")