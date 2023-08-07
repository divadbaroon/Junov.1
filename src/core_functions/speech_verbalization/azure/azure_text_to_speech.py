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
  
	def text_to_speech(self, speech:str):
		"""Performs text-to-speech using Azure's Speech Service."""
		self.speech_synthesizer.speak_text(speech)

	def update_voice(self):
		"""Updates the voice name used for Azure's Speech Service and reconfigures the speech synthesizer."""
		voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
		azure_voice_name = self.voice_settings.retrieve_azure_voice_name(voice_name.title())
		self.speech_config.speech_synthesis_voice_name = azure_voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  