import azure.cognitiveservices.speech as speechsdk
from playsound import playsound
import os

# Local module imports
from settings.settings_orchestrator import SettingsOrchestrator
import configuration.secrets.config as config
from src.pibot_components.bot_functionalities.speech_to_text.speech_recognizer import SpeechRecognition
from src.pibot_components.bot_functionalities.speech_processing.speech_processor import SpeechProcessor
from src.pibot_components.bot_functionalities.text_to_speech.speech_verbalizer import SpeechVerbalizer

class BotInitializer:
	'''
	BotInitializer is a class that initializes a new PiBot object.
 
	Attributes:
	bot_settings: (SettingsOrchestrator) an instance of the SettingsOrchestrator class
	'''
	
	def __init__(self, persona, gender, language):
		"""
		Initializes a new PiBot object 
		:param persona: (str) name of person the bot will emobdy
		:param gender: (str) the gender of the bot
		:param language: (str) the language the bot will speak
		Note: Plays startup sound once initialization of PiBot object is complete.
		"""
		self.bot_settings = SettingsOrchestrator()
		# Save the following bot properties to bot_settings.json
		self._save_bot_properties(persona, gender, language)
  
		# Language country code is used for speech recognizer initialization
		language_country_code = self.bot_settings.get_language_country_code(language)
  
		# Retrieving the bot's secret values from Azure Key Vault
		self._load_api_keys()
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		self._setup_speech_and_audio(self.cognitive_services_api, self.region, language_country_code)

		# initializing the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		self._initialize_speech_functionalities()

		# plays the startup sound if it exists
		self._play_startup_sound_if_exists()
   
	def _save_bot_properties(self, persona, gender, language):
		"""Save the following bot properties to bot_settings.json"""
		self.bot_settings.save_bot_property('persona', persona)
		self.bot_settings.save_bot_property('gender', gender)
		self.bot_settings.save_bot_property('language', language)
   
	def _setup_speech_and_audio(self, cognitive_services_api, region, language_country_code):
		"""Initializes the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer"""
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_config = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config, language=language_country_code)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  
	def _load_api_keys(self):
		"""Retrieving the bot's secret values from Azure Key Vault"""
		self.region = 'eastus'
		self.cognitive_services_api = config.retrieve_secret('Cognitive-Services-API')
		self.luis_app_id = config.retrieve_secret('LUIS-App-ID')
		self.luis_key = config.retrieve_secret('LUIS-API')
		self.openai_key = config.retrieve_secret('OpenAI-API')
		self.weather_key = config.retrieve_secret('Weather-API')
		self.translator_key = config.retrieve_secret('Translator-API')
  
	def _initialize_speech_functionalities(self):
		"""initializing speech recognition, speech processing, and speech verbalization"""""
		self.speech_recognition = SpeechRecognition(self.speech_config, self.speech_recognizer, self.translator_key)
		self.speech_processor = SpeechProcessor(self.luis_app_id, self.luis_key, self.openai_key, self.translator_key, self.weather_key)
		self.speech_verbalizer  = SpeechVerbalizer(self.audio_config, self.speech_config, self.speech_synthesizer)
  
	def _play_startup_sound_if_exists(self):
		"""Plays startup sound if it exists"""
		# Construct the path to the configuration directory and the conversation_history.json file
		current_directory = os.path.dirname(os.path.abspath(__file__))
		sound_file_path = os.path.join(current_directory, os.pardir, os.pardir, 'assets', 'startup_sound.wav')
		# Normalize the path (remove any redundant components)
		sound_file_path = os.path.normpath(sound_file_path)

		# Plays startup sound if it exists
		if os.path.isfile(sound_file_path):
			playsound(sound_file_path)

