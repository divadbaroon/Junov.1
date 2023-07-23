from .intent_recognition.intent_recognition import LuisIntentRecognition
from importlib import import_module
 
class SpeechProcessor:
	"""
	A class that retrieves the user's intent using a trained LUIS model and executes an appropriate response and action.
	"""
 
	def __init__(self, api_keys: dict, setting_objects:dict, speech_verbalizer:object):
		# dynamically import the CommandOrchestrator depending on the package specified in 'bot_settings.json'
		self.package_name = setting_objects['bot_settings'].retrieve_property('package')
		self.CommandOrchestrator = getattr(import_module(f"src.core_functions.speech_processing.command_execution.packages.{self.package_name}.command_orchestrator"), "CommandOrchestrator")
		# initialize the LuisIntentRecognition and CommandOrchestrator objects
		self.get_intent = LuisIntentRecognition(api_keys)
		self.command_orchestrator = self.CommandOrchestrator(api_keys, speech_verbalizer, None, setting_objects)

	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained LUIS model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
		# Returns a dictionary containing similarity rankings between the user's speech and the trained LUIS model
		intents_data = self.get_intent.get_user_intent(speech)
		# Updates the intents_data property in the command_orchestrator object with the intents data retrieved from the LUIS model
		self.command_orchestrator.intents_data = intents_data
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.command_orchestrator.process_command(speech)
		return response
