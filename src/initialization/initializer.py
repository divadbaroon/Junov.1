import azure.cognitiveservices.speech as speechsdk
from src.core_functions.speech_recognition.speech_recognizer import SpeechRecognition
from src.core_functions.speech_processing.speech_processor import SpeechProcessor
from src.core_functions.speech_verbalization.speech_verbalizer import SpeechVerbalizer
from src.components.settings.bot_settings.bot_settings_manager import BotSettingsManager
from src.components.settings.voice_settings.voice_settings_manager import VoiceSettingsManager
from src.components.settings.command_settings.command_settings_manager import BotCommandManager
from src.components.sounds import play_sound
from configuration.manage_secrets import ConfigurationManager

class BotInitializer:
	'''
	Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
	'''
	
	def __init__(self, **kwargs):
		"""
		Initializes PiBot with the following proccesses:
		- Load in settings objects and save given params to bot settings
		- Retrieve dictionary of api keys
		- Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		- Play startup sound once initialization is complete.
		"""
		# load in bot, voice, and command setting objects and store them in a dictionary for ease of use
		self.setting_objects = self._load_in_setting_objects()
  
		# save properties to bot settings
		self._save_bot_properties(**kwargs)
  
		# retrieve api keys as a dictionary
		self.api_keys = ConfigurationManager().retrieve_api_keys()
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		# The audio_config, speech_config, speech_recognizer, and speech_synthesizer are all being stored in a dictionary for ease of use  
		self.speech_objects = self._setup_speech_and_audio(self.api_keys['COGNITIVE-SERVICES-API-KEY'], self.api_keys['REGION'], kwargs.get('language'))

		# initializing the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		self._initialize_speech_functionalities()

		# plays startup sound
		play_sound.play_bot_sound('startup_sound')
  
	def _load_in_setting_objects(self) -> dict:
		"""
  		Initialize setting objects and store them in a dictionary for ease of use
    	"""
		settings = {}
		settings['bot_settings'] = BotSettingsManager()
		settings['voice_settings'] = VoiceSettingsManager()
		settings['command_settings'] = BotCommandManager()
		return settings

	def _save_bot_properties(self, **kwargs) -> None:
		"""
  		Save the following bot properties to bot_settings.json
    	"""
		# check if given params are valid before saving them
		gender, language = self._check_gender_and_language(kwargs.get('gender'), kwargs.get('language'))
		bot_settings = self.setting_objects['bot_settings']
		command_settings = self.setting_objects['command_settings']
		if kwargs.get('name'):
			bot_settings.save_property('name', kwargs.get('name'))
		if kwargs.get('role'):
			bot_settings.save_property('role', kwargs.get('role'))
		if gender:
			bot_settings.save_property('gender', gender, 'current')
		if language:
			bot_settings.save_property('language', language, 'current')
		if kwargs.get('package'):
			bot_settings.save_property('package', kwargs.get('package'))
		if kwargs.get('prompt'):
			command_settings.save_property('ask_gpt', 'prompt', kwargs.get('prompt'))

	def _setup_speech_and_audio(self, cognitive_services_api:str, region:str, language:str) -> dict:
		"""
  		Initializes the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
    	"""
		speech_objects = {}
		speech_objects['audio_config'] = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		speech_objects['speech_config'] = speechsdk.SpeechConfig(subscription = cognitive_services_api, region = region)
		speech_objects['speech_recognizer'] = speechsdk.SpeechRecognizer(speech_config=speech_objects['speech_config'], audio_config=speech_objects['audio_config'], language=self.setting_objects['voice_settings'].retrieve_language_country_code(language))
		speech_objects['speech_synthesizer'] = speechsdk.SpeechSynthesizer(speech_config=speech_objects['speech_config'], audio_config=speech_objects['audio_config'])
		return speech_objects
  
	def _initialize_speech_functionalities(self) -> None:
		"""
  		initializing speech recognition, speech processing, and speech verbalization
    	"""
		self.speech_recognition = SpeechRecognition(self.speech_objects, self.api_keys, self.setting_objects)
		self.speech_verbalizer  = SpeechVerbalizer(self.speech_objects, self.api_keys, self.setting_objects)
		self.speech_processor = SpeechProcessor(self.api_keys, self.setting_objects, self.speech_verbalizer)
  
	def _check_gender_and_language(self, gender:str, language:str) -> str:
		"""
  		Check if gender and langauge are valid before saving them
    	"""
		if gender and gender.lower() not in ['male', 'female']:
			gender = 'female'
		if language and language.lower() not in self.setting_objects['voice_settings'].available_languages():
			language = 'english'
   
		return gender, language


