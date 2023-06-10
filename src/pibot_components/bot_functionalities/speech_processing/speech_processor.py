from .intent_recognition import LuisIntentRecognition
from .command_parser import CommandParser
 
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
 
	def __init__(self, luis_app_id, luis_key, openai_key:str, translator_key:str, weather_key:str):
		self.luis_app_id = luis_app_id
		self.luis_key = luis_key
		self.openai_key = openai_key
		self.translator_key = translator_key
		self.weather_key = weather_key

	def process_speech(self, speech:str): 
		"""
		Processes the user's input using a trained CLU model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
  
		# Retrieves a json file containing similarity rankings between the user's speech and the trained CLU model
		intents_json = LuisIntentRecognition(self.luis_app_id, self.luis_key).get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = CommandParser(self.openai_key, self.translator_key, self.weather_key).parse_commands(speech, intents_json)
		return response
