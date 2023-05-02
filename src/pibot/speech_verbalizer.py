
from configuration.bot_properties import BotProperties
import azure.cognitiveservices.speech as speechsdk
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
 
	def __init__(self, audio_config, speech_config, speech_synthesizer):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_properties = BotProperties()
		self.audio_config = audio_config
		self.speech_config = speech_config
		self.speech_synthesizer = speech_synthesizer
		self.reset_language = False
  
	def verbalize_speech(self, speech: str):
		"""Verbalize the bot's response using the speech synthesizer."""""

		self.bot_properties.reload_settings()
		mute_status = self.bot_properties.retrieve_property('mute_status')
		persona = self.bot_properties.retrieve_property('persona')

		if speech:

			if not mute_status:

				# If the bot is translating, changing the gender, or changing the language the speech will be a dictionary.
				# This is so that the config can be reinitalized with the new property.
				if isinstance(speech, dict):
					speech = self._handle_special_speech(speech)

					new_voice_name = self.bot_properties.retrieve_property('voice_name')
					if new_voice_name:
						self._update_voice(new_voice_name)

				print('\nResponse:')
				print(f'{persona.title()}: {speech}')

				self.speech_synthesizer.speak_text(speech)

				if self.reset_language:
					current_language = self.bot_properties.retrieve_property('language')
					self.bot_properties.save_property('language', current_language)

					voice_name = self.bot_properties.retrieve_property('voice_name')
					if voice_name:
						self._update_voice(voice_name)

					self.reset_language = False

				if speech == 'Exiting. Goodbye!':
					sys.exit()
			else:
				print('\n(muted) Response:')
				print(f'{persona.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')

	def _update_voice(self, voice_name):
		"""Update the speech config and synthesizer with a new voice."""
		self.speech_config.speech_synthesis_voice_name = voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

	def _handle_special_speech(self, speech):
		"""Handle special cases of speech, such as temporary language, gender, and language change."""
		key = next(iter(speech.keys()))

		if key == 'temporary_language':
			self.reset_language = True
			self.bot_properties.save_property('language', speech['temporary_language'])
			return speech['translated_speech']

		if key == 'gender':
			self.bot_properties.save_property('gender', speech['gender'])
			return speech['speech']

		if key == 'language':
			self.bot_properties.save_property('language', speech['language'])
			self.bot_properties.save_property('reconfigure', True)
			return speech['speech']

		return None

   