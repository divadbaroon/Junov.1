import azure.cognitiveservices.speech as speechsdk
from src.core_functions.speech_recognition.speech_recognizer import SpeechRecognition
from src.core_functions.speech_processing.speech_processor.speech_processor import SpeechProcessor
from src.core_functions.speech_verbalization.speech_verbalizer import SpeechVerbalizer
from src.components.settings.bot_settings.bot_settings_manager import BotSettingsManager
from src.components.settings.voice_settings.voice_settings_manager import VoiceSettingsManager
from src.components.sounds import play_sound
from configuration.retrieve_secrets import load_api_keys

class BotInitializer:
	'''
	Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
	'''
	
	def __init__(self, role:str, gender:str, language:str):
		"""
		Initializes a new PiBot object 
		:param role: (str) name of person the bot will emobdy
		:param gender: (str) the gender of the bot
		:param language: (str) the language the bot will speak
		Note: Plays startup sound once initialization of PiBot object is complete.
		"""
  
		# Load in settings objects
		self.bot_settings = BotSettingsManager()
		self.voice_settings = VoiceSettingsManager()
		self._save_bot_properties(role, gender, language)
  
		# check if given params are valid before saving them
		gender, language = self._check_gender_and_language(gender, language)
  
		# Retrieving the bot's secret values as a dictionary
		self.api_keys = load_api_keys()

		# Language country code is used for speech recognizer initialization 
		language = self.bot_settings.retrieve_property('language', 'current')
		language_country_code = self.voice_settings.retrieve_language_country_code(language)
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		# The audio_config, speech_config, speech_recognizer, and speech_synthesizer are all being stored in a dictionary for ease of use  
		self.speech_objects = self._setup_speech_and_audio(self.api_keys['cognitive_services_api'], self.api_keys['region'], language_country_code)

		# initializing the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		self._initialize_speech_functionalities()

		# plays startup sound
		play_sound.play_bot_sound('startup_sound')
  
	def _check_gender_and_language(self, gender:str, language:str) -> str:
		"""Check if gender and langauge are valid before saving them"""
		gender, language = gender.lower(), language.lower()
		# Ensure gender and language provided are currently supported, if not set them to default values
		if gender not in ['male', 'female']:
			gender = 'female'
		if language not in self.voice_settings.available_languages():
			language = 'english'
   
		return gender, language

	def _save_bot_properties(self, role:str, gender:str, language:str) -> None:
		"""Save the following bot properties to bot_settings.json"""
		self.bot_settings.save_property('role', role)
		self.bot_settings.save_property('gender', gender, 'current')
		self.bot_settings.save_property('language', language, 'current')

	def _setup_speech_and_audio(self, cognitive_services_api:str, region:str, language_country_code:str) -> dict:
		"""Initializes the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer"""
		speech_objects = {}
		speech_objects['audio_config'] = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		speech_objects['speech_config'] = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		speech_objects['speech_recognizer'] = speechsdk.SpeechRecognizer(speech_config=speech_objects['speech_config'], audio_config=speech_objects['audio_config'], language=language_country_code)
		speech_objects['speech_synthesizer'] = speechsdk.SpeechSynthesizer(speech_config=speech_objects['speech_config'], audio_config=speech_objects['audio_config'])
		return speech_objects
  
	def _initialize_speech_functionalities(self) -> None:
		"""initializing speech recognition, speech processing, and speech verbalization"""""
		self.speech_recognition = SpeechRecognition(self.speech_objects, self.api_keys, self.bot_settings, self.voice_settings)
		self.speech_processor = SpeechProcessor(self.api_keys, self.bot_settings, self.voice_settings)
		self.speech_verbalizer  = SpeechVerbalizer(self.speech_objects, self.api_keys, self.bot_settings, self.voice_settings)


