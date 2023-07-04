import azure.cognitiveservices.speech as speechsdk
from code.core_functions.speech_recognition.speech_recognizer import SpeechRecognition
from code.core_functions.speech_processing.speech_processor.speech_processor import SpeechProcessor
from code.core_functions.speech_verbalization.speech_verbalizer import SpeechVerbalizer
from code.components.settings.settings_manager import SettingsOrchestrator
from code.components.sounds import play_sound
from configuration.retrieve_secrets import load_api_keys

class BotInitializer:
	'''
	Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
	'''
	
	def __init__(self, role, gender, language):
		"""
		Initializes a new PiBot object 
		:param role: (str) name of person the bot will emobdy
		:param gender: (str) the gender of the bot
		:param language: (str) the language the bot will speak
		Note: Plays startup sound once initialization of PiBot object is complete.
		"""
  
		# check if given params are valid before saving them
		gender, language = self._check_gender_and_language(gender, language)
  
		# Save the following bot properties to bot_settings.json
		self.bot_settings = SettingsOrchestrator()
		self._save_bot_properties(role, gender, language)
  
		# Retrieving the bot's secret values as a dictionary
		self.api_keys = load_api_keys()

		# Language country code is used for speech recognizer initialization 
		language = self.bot_settings.retrieve_bot_property('language')
		language_country_code = self.bot_settings.get_language_country_code(language)
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		self._setup_speech_and_audio(self.api_keys['cognitive_services_api'], self.api_keys['region'], language_country_code)

		# initializing the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		self._initialize_speech_functionalities()

		# plays startup sound
		play_sound.play_bot_sound('startup_sound')
  
	def _check_gender_and_language(self, gender, language):
		"""Check if gender and langauge are valid"""
		gender, language = gender.lower(), language.lower()
  
		# Ensure gender and language provided are currently supported, if not set them to default values
		if gender not in ['male', 'female']:
			gender = 'female'
		if language not in ['arabic', 'english', 'spanish', 'french', 'mandarin', 
                      		'hindi', 'finnish', 'german', 'korean', 'russian']:
			language = 'english'
   
		return gender, language

	def _save_bot_properties(self, role, gender, language):
		"""Save the following bot properties to bot_settings.json"""
		self.bot_settings.save_bot_property('role', role)
		self.bot_settings.save_bot_property('gender', gender)
		self.bot_settings.save_bot_property('language', language)

	def _setup_speech_and_audio(self, cognitive_services_api, region, language_country_code):
		"""Initializes the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer"""
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_config = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config, language=language_country_code)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  
	def _initialize_speech_functionalities(self):
		"""initializing speech recognition, speech processing, and speech verbalization"""""
		self.speech_recognition = SpeechRecognition(self.speech_recognizer, self.speech_config, self.bot_settings, self.api_keys)
		self.speech_processor = SpeechProcessor(self.api_keys, self.bot_settings)
		self.speech_verbalizer  = SpeechVerbalizer(self.api_keys, self.bot_settings, self.speech_synthesizer, self.speech_config, self.audio_config)


