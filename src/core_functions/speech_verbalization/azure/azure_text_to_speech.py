import azure.cognitiveservices.speech as speechsdk

class AzureTextToSpeech:
	"""A class that utilizes Azure's Speech Service to verbalize the bot's response."""
	def __init__(self, profile_name:str, speech_objects:dict, setting_objects:dict):
		self.profile_name = profile_name
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.speech_synthesizer = speech_objects['speech_synthesizer']
		self.speech_config = speech_objects['speech_config']
		self.audio_config = speech_objects['audio_config']
  
	def text_to_speech(self, speech:str, language_country_code:str):
		"""Performs text-to-speech using Azure's Speech Service."""

		# prepare ssml file to be used for azure text to speech
		ssml = self._prepare_ssml(speech, language_country_code)
		# perform text to speech
		self.speech_synthesizer.speak_ssml(ssml)
  
	def _prepare_smml(self, speech:str, language_country_code:str):
		"""
		Prepare ssml file to be used for azure text to speech
		"""
		return f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">' \
			   f'<voice name="{self.speech_config.speech_synthesis_voice_name}">' \
			   f'<prosody rate="1.0">' \
			   f'<mstts:express-as style="assistant" styledegree="1">' \
			   f'<lang xml:lang="{language_country_code}">' \
			   f'{speech}' \
			   f'</lang>' \
			   f'</mstts:express-as>' \
			   f'</prosody>' \
			   f'</voice>' \
			   f'</speak>'

	def update_voice(self):
		"""
		Updates the voice name used for Azure's Speech Service and reconfigures the speech synthesizer.
  		"""
		voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
		azure_voice_name = self.voice_settings.retrieve_azure_voice_name(voice_name.title())
		self.speech_config.speech_synthesis_voice_name = azure_voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  