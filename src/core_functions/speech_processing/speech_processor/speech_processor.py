from ..intent_recognition.intent_recognition import LuisIntentRecognition
from ...speech_processing.command_execution.command_parser import CommandParser
 
class SpeechProcessor:
	"""
	A class that processes the user's input using a trained CLU model and produces an appropriate response and action.
	This class is comprised of two initial nested classes: SpeechIntent and CommandParser.
	The nested SpeechIntent class retrieves the similarity rankings between the user's speech and the trained CLU model in json format.
	The nested CommandParser class uses the data from the similarity rankings to provide the most apporiate response 
 	and action to the user's speech.
	The nested CommandParser class is composed of seven nested classes, each containing methods dedicated to executing
	commands that are specific to the user's intent.
	These clases nested under CommandParser include: AskGPT, TranslateSpeech, GetWeather, WebSearcher, PasswordGenerator,
	BotBehavior, and ConversationHistoryManager
	"""
 
	def __init__(self, api_keys: dict, bot_settings:object, voice_settings:object, command_settings:object, speech_verbalizer:object):
		self.api_keys = api_keys
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		self.command_settings = command_settings
		self.speech_verbalizer = speech_verbalizer
		# intents_data set to None since it will be updated in process_speech
		self.command_parser = CommandParser(self.api_keys, speech_verbalizer, None, self.bot_settings, self.voice_settings, self.command_settings)
		self.get_intent = LuisIntentRecognition(self.api_keys)

	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained CLU model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
		
		# Retrieves a dictionary containing similarity rankings between the user's speech and the trained CLU model
		intents_data = self.get_intent.get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		self.command_parser.intents_data = intents_data
		response = self.command_parser.parse_commands(speech)
		return response
