from .elevenlabs.text_to_speech import ElevenlabsTextToSpeech
from .azure_speech_service.text_to_speech import AzureTextToSpeech
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
 
	def __init__(self, api_keys, bot_settings, speech_synthesizer, speech_config, audio_config):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_settings = bot_settings
		if self.bot_settings.retrieve_bot_property('voice_engine') == 'azure':
			self.text_to_speech_engine = AzureTextToSpeech(api_keys, speech_synthesizer, speech_config, audio_config)
		else:
			self.text_to_speech_engine = ElevenlabsTextToSpeech(api_keys, bot_settings)
  
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""""

		self.bot_settings.reload_bot_settings()
		mute_status = self.bot_settings.retrieve_bot_property('mute_status')
		bot_name = self.bot_settings.retrieve_bot_property('name')
		exit_status = self.bot_settings.retrieve_bot_property('exit_status')
		reset_language = self.bot_settings.retrieve_bot_property('reset_language')

		# check if there is user input
		if speech:
			# check if the bot is muted
			if not mute_status:
				
				print('\nResponse:')
				print(f'{bot_name.title()}: {speech}')

				# Verbalize the response
				self.text_to_speech_engine.text_to_speech(speech)
    
				if reset_language:
					self._reset_language()

				# Exit the program if the exit status is True
				if exit_status:
					self.bot_settings.save_bot_property('mute_status', False)
					sys.exit()
			else:
				print('\n(muted) Response:')
				print(f'{bot_name.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')
   
	def _reset_language(self):
		"""Reset the language."""
		voice_engine = self.bot_settings.retrieve_bot_property('voice_engine')

		if voice_engine != 'azure':
			previous_voice_name = self.bot_settings.retrieve_bot_property('previous_azure_voice_name')
			self.bot_settings.save_bot_property('current_azure_voice_name', previous_voice_name)
		else:
			previous_voice_name = self.bot_settings.retrieve_bot_property('previous_elevenlabs_voice_name')
			self.bot_settings.save_bot_property('current_elevenlabs_voice_name', previous_voice_name)

		previous_language = self.bot_settings.retrieve_bot_property('previous_language')
		self.bot_settings.save_bot_property('language', previous_language)
		# Updaing speech synthesizer with new voice name
		self.text_to_speech_engine.update_voice(previous_voice_name)
  
	def _reset_gender(self):
		"""Reset the gender."""
		voice_engine = self.bot_settings.retrieve_bot_property('voice_engine')

		if voice_engine != 'azure':
			previous_voice_name = self.bot_settings.retrieve_bot_property('previous_azure_voice_name')
			self.bot_settings.save_bot_property('current_azure_voice_name', previous_voice_name)
		else:
			previous_voice_name = self.bot_settings.retrieve_bot_property('previous_elevenlabs_voice_name')
			self.bot_settings.save_bot_property('current_elevenlabs_voice_name', previous_voice_name)

		previous_gender= self.bot_settings.retrieve_bot_property('previous_gender')
		self.bot_settings.save_bot_property('gender', previous_gender)
		# Updaing speech synthesizer with new voice name
		self.text_to_speech_engine.update_voice(previous_voice_name)

   