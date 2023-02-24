import config
import azure.cognitiveservices.speech as speechsdk
from bot_properties import BotProperties

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	bot_properties (BotProperties): A BotProperties object that contains information about the bot's properties.
	persona (str): The persona of the bot retrieved from bot_properties.json
    mute_status (bool): The mute status of the bot retrieved from bot_properties.json
    speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
    audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
    speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
 
	def __init__(self):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.bot_properties = BotProperties()
		self.persona = self.bot_properties.get_property('persona')
		self.mute_status = self.bot_properties.get_property('mute_status')
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

	def verbalize_speech(self, speech: str):
		"""
		Verbalizes a given string with a specified gender and langauge of voice.
		:param speech (str): The speech to be verbalized.
		"""	
  
		# Check if there is speech to verbalize
		if speech:
			# Check the bot's mute status
			if not self.mute_status: 
       
				# Retrieve the bot's voice name from bot_properties.json
				# depending on the bot's specified gender and language.
				voice_name = self.bot_properties.get_property('voice_name')

				# Check if voice with given parameters exists
				if voice_name:
					self.speech_config.speech_synthesis_voice_name = voice_name
				else:
					self.speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural' # used as a backup 

				print('\nResponse:')
				print(f'{self.persona.title()}: {speech}')
    
				# Verbalize the speech
				self.speech_synthesizer.speak_text(speech)
			else:
				print('\n(muted) Response:')
				print(f'{self.persona.title()}: {speech}')
		else:
			print('No speech has been provided to verbalize.')
	
	
   
	


