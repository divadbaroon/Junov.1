import sys
from .elevenlabs.elevenlabs_text_to_speech import ElevenlabsTextToSpeech
from .azure.azure_text_to_speech import AzureTextToSpeech
from src.utilities.logs.log_performance import PerformanceLogger

logger = PerformanceLogger()

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.
	"""
 
	def __init__(self, profile_name:str, speech_objects:dict, api_keys:dict, setting_objects:dict):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.profile_name = profile_name
		self.master_settings = setting_objects['master_settings']
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		# check which speech engine is used
		if self.profile_settings.retrieve_property('voice_engine') == 'azure':
			self.text_to_speech_engine = AzureTextToSpeech(self.profile_name, speech_objects, setting_objects)
		else:
			self.text_to_speech_engine = ElevenlabsTextToSpeech(self.profile_name, api_keys, setting_objects)
   
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""
  
		# loading in necessary data from 'master_settings.json'
		self._load_in_settings()
  
		self.text_to_speech_engine.update_voice()

		# initiale flag to check whether the speech synthesizer needs to be reconfigured or the bot is muted
		if self._check_and_handle_preconditions(speech):
				
			print('\nResponse:')
			print(f'{self.bot_name.title()}: {speech}')

			# Verbalize the response
			self.text_to_speech_engine.text_to_speech(speech)

		# Checks whether the following params are true and executed the appropriate actions
		self._check_and_handle_postconditions(self.reset_language, self.exit_status)
  
		return speech
  
	def _load_in_settings(self):
		"""
  		Loading in necessary data from 'master_settings.json'
    	"""
		self.master_settings.reload_settings()
		self.bot_name = self.profile_settings.retrieve_property('name', profile_name=self.profile_name)
		self.mute_status = self.master_settings.retrieve_property('status', 'mute')
		self.exit_status = self.master_settings.retrieve_property('status', 'exit')
		self.reset_language = self.master_settings.retrieve_property('functions', 'reset_language')
		self.reconfigure_voice = self.master_settings.retrieve_property('functions', 'reconfigure_verbalizer')
  
	def _check_and_handle_preconditions(self, speech:str) -> bool:
		"""
		Initial flag check
		"""
		# check whether speech was given
		if not speech:
			print('No speech has been provided to verbalize.')
			return False
		
		# check if bot is muted
		if self.mute_status:
			print('\n(muted) Response:')
			print(f'{self.bot_name.title()}: {speech}')
			return False
   
		# check if voice need to be reconfigured
		if self.reconfigure_voice:
			self.text_to_speech_engine.update_voice()
			self.master_settings.save_property('functions', False, 'reconfigure_verbalizer')
			return True
   
		return True
   
	def _check_and_handle_postconditions(self, reset_language, exit_status):
		"""Post verbalization flag check"""
		# check if language needs to be reset (this is done after one-shot speach translationions)
		if reset_language:
			self.master_settings.save_property('functions', False, 'reset_language')

		# Exit the program needs to be exited
		if exit_status:
			self.master_settings.save_property('status', False, 'exit')
			sys.exit()
   
  

   