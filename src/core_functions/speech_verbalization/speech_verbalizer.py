from .elevenlabs.elevenlabs_text_to_speech import ElevenlabsTextToSpeech
from .azure.azure_text_to_speech import AzureTextToSpeech
import sys

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	bot_properties (BotProperties): A BotProperties object that contains information about the bot's properties.
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
	speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
 
	def __init__(self, speech_objects:dict, api_keys:dict, bot_settings:object, voice_settings:object):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		if self.bot_settings.retrieve_property('voice', 'engine') == 'azure':
			self.text_to_speech_engine = AzureTextToSpeech(speech_objects, bot_settings, voice_settings)
		else:
			self.text_to_speech_engine = ElevenlabsTextToSpeech(api_keys, bot_settings)
  
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""""
  
		self._load_in_settings()

		# check if there is user input
		if speech:
			# check if the bot is muted
			if not self.mute_status:
				# check if voice need to be reconfigured
				if self.reconfigure_voice:
					self.text_to_speech_engine.update_voice()
					self.bot_settings.save_property('voice', False, 'reconfigure')
				
				print('\nResponse:')
				print(f'{self.bot_name.title()}: {speech}')

				# Verbalize the response
				self.text_to_speech_engine.text_to_speech(speech)
			else:
				print('\n(muted) Response:')
				print(f'{self.bot_name.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')

		# Checks whether the following params are true and executed the appropriate actions
		self._check_for_flags(self.reset_language, self.exit_status)
  
	def _load_in_settings(self):
		"""Loading in necessary data from 'bot_settings.json'"""
		self.bot_settings.reload_settings()
		self.mute_status = self.bot_settings.retrieve_property('status', 'mute')
		self.bot_name = self.bot_settings.retrieve_property('name')
		self.exit_status = self.bot_settings.retrieve_property('status', 'exit')
		self.reset_language = self.bot_settings.retrieve_property('language', 'reset')
		self.reconfigure_voice = self.bot_settings.retrieve_property('voice', 'reconfigure')
   
	def _check_for_flags(self, reset_language, exit_status):
		"""Checks whether the language needs to be reset or the program needs to exit"""
		if reset_language:
			self._reset_language()

		# Exit the program if the exit status is True
		if exit_status:
			self.bot_settings.save_property('status', False, 'exit')
			sys.exit()
   
	def _reset_language(self):
		"""Reset the language."""
		voice_engine = self.bot_settings.retrieve_property('voice', 'engine')

		if voice_engine != 'azure':
			previous_voice_name = self.bot_settings.retrieve_property('voice', 'previous_azure_voice_name')
			self.bot_settings.save_property('voice', previous_voice_name, 'current_azure_voice_name')
		else:
			previous_voice_name = self.bot_settings.retrieve_property('voice', 'previous_elevenlabs_voice_name')
			self.bot_settings.save_property('voice', previous_voice_name, 'current_elevenlabs_voice_name')

		previous_language = self.bot_settings.retrieve_property('language', 'previous')
		self.bot_settings.save_property('language', previous_language, 'current')
		# Updaing speech synthesizer with new voice name
		self.text_to_speech_engine.update_voice()
  
		self.bot_settings.save_property('language', False, 'reset')
  
	def _reset_gender(self):
		"""Reset the gender."""
		voice_engine = self.bot_settings.retrieve_property('voice', 'engine')

		if voice_engine != 'azure':
			previous_voice_name = self.bot_settings.retrieve_property('voice', 'previous_azure_voice_name')
			self.bot_settings.save_property('voice', previous_voice_name, 'current_azure_voice_name')
		else:
			previous_voice_name = self.bot_settings.retrieve_property('voice', 'previous_elevenlabs_voice_name')
			self.bot_settings.save_property('voice', previous_voice_name, 'current_elevenlabs_voice_name')

		previous_gender= self.bot_settings.retrieve_property('gender', 'previous')
		self.bot_settings.save_property('gender', previous_gender, 'current')
		# Updaing speech synthesizer with new voice name
		self.text_to_speech_engine.update_voice()
  
		self.bot_settings.save_property('gender', False, 'reset')

   