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
 
	def __init__(self, api_keys: dict, bot_settings:object, voice_settings:object, command_settings:object):
		self.api_keys = api_keys
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		self.command_settings = command_settings

	def process_speech(self, speech:str, speech_verbalizer:object): 
		"""
		Processes the user's input using a trained CLU model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
		
		# Retrieves a json file containing similarity rankings between the user's speech and the trained CLU model
		intents_json = LuisIntentRecognition(self.api_keys).get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = CommandParser(self.api_keys, speech_verbalizer, intents_json, self.bot_settings, self.voice_settings, self.command_settings).parse_commands(speech)
		return response
