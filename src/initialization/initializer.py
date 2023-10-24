import azure.cognitiveservices.speech as speechsdk
from src.core_functions.speech_recognition.speech_recognizer import SpeechRecognition
from src.core_functions.speech_processing.speech_processor import SpeechProcessor
from src.core_functions.speech_verbalization.speech_verbalizer import SpeechVerbalizer
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.customization.voices.voice_settings_manager import VoiceSettingsManager
from src.utilities.settings.command_settings.command_settings_manager import BotCommandManager
from src.customization.profiles.profile_manager import ProfileManager
from configuration.manage_secrets import ConfigurationManager
from src.customization.sounds import play_sound

class BotInitializer:
	'''
	Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
	'''
	
	def __init__(self):
		"""
		Initializes Juno with the following proccesses:
		- Load in settings objects and save given params to bot settings
		- Retrieve dictionary of api keys
		- Initialize the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		- Play startup sound once initialization is complete.
		"""
  
		# load in bot, voice, command, and profile setting objects and store them in a dictionary for ease of use
		self.setting_objects = self._load_in_setting_objects()
  
		# retrieve api keys as a dictionary
		self.api_keys = ConfigurationManager().retrieve_api_keys()
  
		# Initializing the bot's audio configuration, speech configuration, speech recognizer, and speech synthesizer
		# The audio_config, speech_config, speech_recognizer, and speech_synthesizer are all being stored in a dictionary for ease of use  
		self.speech_objects = self._setup_speech_and_audio(self.api_keys['COGNITIVE-SERVICES-API-KEY'], self.api_keys['REGION'], self.setting_objects['profile_settings'].retrieve_property('language'))

		# initializing the bot's core functionalities: speech recognition, speech processing, and speech verbalization
		self._initialize_speech_functionalities()

		# plays startup sound
		if self.setting_objects['profile_settings'].retrieve_property('startup_sound'):
			play_sound.play_bot_sound('startup_sound')
  
	def _load_in_setting_objects(self) -> dict:
		"""
  		Initialize setting objects and store them in a dictionary for ease of use
    	"""
		settings = {}
		settings['master_settings'] = MasterSettingsManager()
		settings['voice_settings'] = VoiceSettingsManager()
		settings['command_settings'] = BotCommandManager()
		settings['profile_settings'] = ProfileManager()
		return settings 

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
  



