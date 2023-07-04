import azure.cognitiveservices.speech as speechsdk

class AzureTextToSpeech:
	"""A class that utilizes Azure's Speech Service to verbalize the bot's response."""
	def __init__(self, speech_objects:dict):
		self.speech_synthesizer = speech_objects['speech_synthesizer']
		self.speech_config = speech_objects['speech_config']
		self.audio_config = speech_objects['audio_config']
  
	def text_to_speech(self, speech:str):
		"""Performs text-to-speech using Azure's Speech Service."""
		self.speech_synthesizer.speak_text(speech)

	def update_voice(self, voice_name:str):
		"""Updates the voice name used for Azure's Speech Service and reconfigures the speech synthesizer."""
		self.speech_config.speech_synthesis_voice_name = voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  