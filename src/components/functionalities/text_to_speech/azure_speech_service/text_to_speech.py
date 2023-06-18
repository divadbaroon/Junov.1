import azure.cognitiveservices.speech as speechsdk

class AzureTextToSpeech:
	"""A class that utilizes Azure's Speech Service to verbalize the bot's response."""
	def __init__(self, api_keys:dict, speech_synthesizer:object, speech_config:object, audio_config:object):
		self.api_keys = api_keys
		self.speech_synthesizer = speech_synthesizer
		self.speech_config = speech_config
		self.audio_config = audio_config
  
	def text_to_speech(self, speech):
		"""Performs text-to-speech using Azure's Speech Service."""
		self.speech_synthesizer.speak_text(speech)

	def update_voice(self, voice_name):
		"""Updates the voice name used for Azure's Speech Service and reconfigures the speech synthesizer."""
		self.speech_config.speech_synthesis_voice_name = voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  