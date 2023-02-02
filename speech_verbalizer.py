import config
import azure.cognitiveservices.speech as speechsdk
import json
import sys

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
				with open('bot_gender_and_languages.json', 'r') as f:   
					voice_names = json.load(f)
			except FileNotFoundError:
				print('The file "bot_gender_and_languages.json" is missing.\nMake sure all files are located within the same folder')
	
			# assigning appropriate bot voice 
			voice_name = voice_names[self.gender.lower()].get(self.language.lower())
			# check if voice with given parameters exists
			if voice_name:
				self.speech_config.speech_synthesis_voice_name = voice_name
			else:
				self.speech_config.speech_synthesis_voice_name = 'en-US-JennyNeural' # used as backup 

			print('\nResponse:')
			print(f'{self.persona}: {speech}')
   
			self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
			self.speech_synthesizer.speak_text(speech)
		else:
			print('\n(muted) Response:')
			print(f'{self.persona}: {speech}')

		# if user wants to end the session the file bot_conversation will be cleared
		# and the program will be stopped
		if speech == 'Exiting the program, goodbye...':
			self.exit_and_cleanup()
	
	def load_mute_status(self):
		"""
		Loads the current mute status from "mute_status.json"
		"""	
		try:
			with open("bot_mute_status.json") as f:
				self.mute_status = json.load(f)
				return self.mute_status
		except FileNotFoundError:
			print('The file "bot_mute_status.json" is missing.\nMake sure all files are located within the same folder')
	
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
		Saves the desired mute status to "mute_status.json"
		"""
		try:
			with open("bot_mute_status.json", "w") as f:
				json.dump(self.mute_status, f)
		except FileNotFoundError:
			print('The file "bot_mute_status.json" is missing.\nMake sure all files are located within the same folder')
	
	def exit_and_cleanup(self):
		"""
		Cleans up and ends program
		"""
		# Clearing the contents of the file	
		with open("bot_conversation.json", "w") as file:
			json.dump({"conversation": ""}, file)
		sys.exit()


