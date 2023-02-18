import config
import azure.cognitiveservices.speech as speechsdk
import json

class SpeechVerbalizer:
	"""
	A class that utilizes Azure's Cognitive Speech Service to verbalize the bot's response.

	Attributes:
	mute_status: mute status of the bot
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	audio_config (AudioOutputConfig): A configuration object that specifies the use of the default speaker
	speech_synthesizer (SpeechSynthesizer): A synthesizer object that uses the above configurations to generate the spoken words
	"""
	def __init__(self):
		"""
		Initializes a new SpeechVerbalizer object
		"""
		self.mute_status = None
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

	def verbalize_speech(self, speech: str, persona: str, gender: str, language: str):
		"""
		Verbalizes a given string with a specified gender and langauge of voice.
		:param speech (str): The speech to be verbalized.
		"""	
		# load the bot's current mute status
		self.mute_status = self.load_mute_status()  

		# check if speech is not empty
		if speech:
			# check bot's mute status
			if not self.mute_status: 
		
				# attempt to extract the bot's gender and language
				try: 
					with open('bot_properties.json', 'r') as f:   
						voice_names = json.load(f)
				except FileNotFoundError:
					print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
		
				# assigning appropriate bot voice 
				voice_name = voice_names[gender.lower()].get(language.lower())
				# check if voice with given parameters exists
				if voice_name:
					self.speech_config.speech_synthesis_voice_name = voice_name
				else:
					self.speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural' # used as backup 

				print('\nResponse:')
				print(f'{persona}: {speech}')
	
				self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
				self.speech_synthesizer.speak_text(speech)
			else:
				print('\n(muted) Response:')
				print(f'{persona}: {speech}')
	
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
	


