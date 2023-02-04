import config
import azure.cognitiveservices.speech as speechsdk
import json

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	persona (str): name of the person the bot will emobdy
	gender (str): gender of the bot
	langauge (str): language the bot will speak
	mute_status: mute status of the bot
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
	speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
	def __init__(self, persona='none', gender='female', language='default'):
		"""
		Initializes a new SpeechVerbalizer object
		:param persona: (str) name of the person that the bot will emobdy
		:param gender: (str) gender of the bot
		:param language: (str) language the bot will speak
		"""
		self.persona = persona
		self.gender = gender
		self.language = language
		self.mute_status = None
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

	def verbalize_speech(self, speech: str):
		"""
		Verbalizes a given string with a specified gender and langauge of voice.
		:param speech (str): The speech to be verbalized.
		"""	
		# load the bot's current mute status
		self.mute_status = self.load_mute_status()  
  
		# check bot's mute status
		if not self.mute_status: 
	  
			# attempt to extract the bot's gender and language
			try: 
				with open('bot_properties.json', 'r') as f:   
					voice_names = json.load(f)
			except FileNotFoundError:
				print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
	
			# assigning appropriate bot voice 
			voice_name = voice_names[self.gender.lower()].get(self.language.lower())
			# check if voice with given parameters exists
			if voice_name:
				self.speech_config.speech_synthesis_voice_name = voice_name
			else:
				self.speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural' # used as backup 

			#print('\nResponse:')
			print(f'{self.persona}: {speech}')
   
			self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
			self.speech_synthesizer.speak_text(speech)
		else:
			print('\n(muted) Response:')
			print(f'{self.persona}: {speech}')
	
	def load_mute_status(self):
		"""
		Loads the current mute status from "bot_properties.json"
		"""	
		try:
			with open("bot_properties.json") as f:
				data = json.load(f)
				self.mute_status = data.get("mute status")
				return self.mute_status
		except FileNotFoundError:
			print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
	
	def mute(self):
		"""
		Mutes the bot by setting mute status to true.
		"""	
		self.mute_status = True
		self.save_mute_status()
		
	def unmute(self):
		"""
		Unmutes the bot by setting mute status to false.
		"""
		self.mute_status = False
		self.save_mute_status()
	
	def save_mute_status(self):
		"""
		Saves the desired mute status to "bot_properties.json"
		"""
		try:
			with open("bot_properties.json", "r") as f:
				data = json.load(f)
			
			data["mute status"] = self.mute_status
			
			with open("bot_properties.json", "w") as f:
				json.dump(data, f, indent=4)
		except FileNotFoundError:
			print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
	


