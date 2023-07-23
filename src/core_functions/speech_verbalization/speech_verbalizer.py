import sys
from .elevenlabs.elevenlabs_text_to_speech import ElevenlabsTextToSpeech
from .azure.azure_text_to_speech import AzureTextToSpeech

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.
	"""
 
	def __init__(self, speech_objects:dict, api_keys:dict, setting_objects:dict):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_settings = setting_objects['bot_settings']
		self.voice_settings = setting_objects['voice_settings']
		# check which speech engine is used
		if self.bot_settings.retrieve_property('voice', 'engine') == 'azure':
			self.text_to_speech_engine = AzureTextToSpeech(speech_objects, setting_objects)
		else:
			self.text_to_speech_engine = ElevenlabsTextToSpeech(api_keys, setting_objects)
  
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""
  
		# loading in necessary data from 'bot_settings.json'
		self._load_in_settings()

		# initiale flag to check whether the speech synthesizer needs to be reconfigured or the bot is muted
		if self._check_and_handle_preconditions(speech):
				
			print('\nResponse:')
			print(f'{self.bot_name.title()}: {speech}')

			# Verbalize the response
			self.text_to_speech_engine.text_to_speech(speech)

		# Checks whether the following params are true and executed the appropriate actions
		self._check_and_handle_postconditions(self.reset_language, self.exit_status)
  
	def _load_in_settings(self):
		"""
  		Loading in necessary data from 'bot_settings.json'
    	"""
		self.bot_settings.reload_settings()
		self.mute_status = self.bot_settings.retrieve_property('status', 'mute')
		self.bot_name = self.bot_settings.retrieve_property('name')
		self.exit_status = self.bot_settings.retrieve_property('status', 'exit')
		self.reset_language = self.bot_settings.retrieve_property('language', 'reset')
		self.reconfigure_voice = self.bot_settings.retrieve_property('voice', 'reconfigure')
  
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
			self.bot_settings.save_property('voice', False, 'reconfigure')
			return True
   
		return True
   
	def _check_and_handle_postconditions(self, reset_language, exit_status):
		"""Post verbalization flag check"""
		# check if language needs to be reset (this is done after one-shot speach translationions)
		if reset_language:
			self._reset_language()

		# Exit the program needs to be exited
		if exit_status:
			self.bot_settings.save_property('status', False, 'exit')
			sys.exit()
   
	def _reset_language(self):
		"""Reset the language, this is done after one-shot speach translationions"""
		# Reset the language to the previous language
		previous_language = self.bot_settings.retrieve_property('language', 'previous')
		self.bot_settings.save_property('language', previous_language, 'current')
		# Set reconfigure_voice to True to reconfigure the speech synthesizer
		self.bot_settings.save_property('voice', True, 'reconfigure')
		# Reset the reset language flag
		self.bot_settings.save_property('language', False, 'reset')
  

   