'''
Note:
The following files must all be located within the same folder for the bot to function.
< pibot.py, speech_recognizer.py, speech_processor.py, speech_verbalizer.py, sample_config.py,  
  bot_properties.py, bot_properties.json, conversation_history.json, startup_sound.wav(optional) >  
'''

import azure.cognitiveservices.speech as speechsdk
from playsound import playsound
import os

# Local module imports
from pibot.speech_recognizer import SpeechRecognition
from pibot.speech_processor import SpeechProcessor
from pibot.speech_verbalizer import SpeechVerbalizer
from configuration.bot_properties import BotProperties

class PiBot:
	'''
	PiBot is a class that provides a simple interface for creating a chatbot.
	It uses three classes for the speech recognition, speech processing, and speech verbalization.
 
	Attributes:
	persona (str): name of person the bot will emobdy
	gender (str): the gender of the bot
	langauge (str): the language the bot will speak
	speech_recognition: object of SpeechRecognition class
	speech_processor: object of SpeechProcessor class
	speech_verbalizer: object of SpeechVerbalizer class
	bot_properties: object of BotProperties class
	speech_config: object of SpeechConfig class
	audio_config: object of AudioOutputConfig class
	speech_synthesizer: object of SpeechSynthesizer class
	speech_recognizer: object of SpeechRecognizer class
	'''
	
	def __init__(self, pibot_api, luis_app_id, luis_key, openai_key, weather_key=None, translator_key=None, news_key=None):
		"""
		Initializes a new PiBot object 
		:param persona: (str) name of person the bot will emobdy
		:param gender: (str) the gender of the bot
		:param language: (str) the language the bot will speak
		Note: Plays startup sound once initialization of PiBot object is complete.
		"""

		# Retrieving the bot's language from bot_settings.json
		bot_properties = BotProperties()
		language = bot_properties.retrieve_property('language')
		# Recognizer needs the language's country code
		language_country_code = bot_properties.get_language_country_code(language)

		# Intializing the bot's audio configuration
		self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		# Initializing the bot's speech configuration
		self.speech_config = speechsdk.SpeechConfig(subscription = pibot_api, region = 'eastus')
		# Initializing the bot's speech recognizer 
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config, language=language_country_code)
		# Initializing the bot's speech synthesizer
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  
		# Retrieving the bot's secret values 
		self.luis_app_id = luis_app_id
		self.luis_key = luis_key
		self.openai_key = openai_key
		self.weather_key = weather_key
		self.translator_key = translator_key
		self.news_key = news_key
  
		# initializing the bot's speech functionalities
		self.speech_recognition = SpeechRecognition(self.speech_config, self.speech_recognizer, self.translator_key)
		self.speech_processor = SpeechProcessor(self.luis_app_id, self.luis_key, self.openai_key, self.translator_key, self.weather_key, self.news_key)
		self.speech_verbalizer  = SpeechVerbalizer(self.audio_config, self.speech_config, self.speech_synthesizer)

		# Construct the path to the configuration directory and the conversation_history.json file
		current_directory = os.path.dirname(os.path.abspath(__file__))
		sound_file_path = os.path.join(current_directory, os.pardir, os.pardir, 'assets', 'startup_sound.wav')
		# Normalize the path (remove any redundant components)
		sound_file_path = os.path.normpath(sound_file_path)

		# Plays startup sound if it exists
		if os.path.isfile(sound_file_path):
			playsound(sound_file_path)

	def listen(self) -> str:
		"""
		Listens for users speech input
		:return: (str) speech input
		"""
		return self.speech_recognition.listen()

	def process(self, speech: str) -> str:
		"""
		Processes and produces a response to users speech
		:param speech: (str) speech input
		:return: (str) response to users speech
		"""
		return self.speech_processor.process_speech(speech)
	
	def verbalize(self, response: str):
		"""
		Verbalizes a string
		:param response: (str) string to be verbalized
		"""
		self.speech_verbalizer.verbalize_speech(response)
	
	def run(self):
		"""
		Peforms all of bot's functionalities including:
		:.listen() # Listens for users speech
		:.process() # Processes and produces a response to users speech
		:.verbalize() # Verbalizes the response
		"""
		speech = self.speech_recognition.listen()
		response = self.speech_processor.process_speech(speech)
		self.speech_verbalizer.verbalize_speech(response)
			
