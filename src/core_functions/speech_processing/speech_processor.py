from .intent_recognition.intent_recognition import LuisIntentRecognition
from .command_execution.command_orchestrator import CommandOrchestrator
 
class SpeechProcessor:
	"""
	A class that retrieves the user's intent using a trained LUIS model and executes an appropriate response and action.
	"""
 
	def __init__(self, api_keys: dict, setting_objects:dict, speech_verbalizer:object):
		# intents_data set to None since it will be updated in process_speech
		self.command_orchestrator = CommandOrchestrator(api_keys, speech_verbalizer, None, setting_objects)
		self.get_intent = LuisIntentRecognition(api_keys)

	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained CLU model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
		# Returns a dictionary containing similarity rankings between the user's speech and the trained LUIS model
		intents_data = self.get_intent.get_user_intent(speech)
		# Updates the intents_data property in the command_orchestrator object with the intents data retrieved from the LUIS model
		self.command_orchestrator.intents_data = intents_data
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.command_orchestrator.parse_commands(speech)
		return response
