from .intent_recognition.intent_recognition import LuisIntentRecognition
from .command_execution.command_orchestrator import CommandOrchestrator
 
class SpeechProcessor:
	"""
	A class that retrieves the user's intent using a trained LUIS model and executes an appropriate response and action.
	"""
 
	def __init__(self, api_keys: dict, setting_objects:dict, speech_verbalizer:object):
		self.package_name = setting_objects['profile_settings'].retrieve_property('package')
		self.get_intent = LuisIntentRecognition(api_keys)
		self.command_orchestrator = CommandOrchestrator(api_keys, speech_verbalizer, None, setting_objects)

	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained LUIS model (if a package is being used) and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
  
		print('\nThinking...')
		# If a package is provided, retrieve the user's intent using the trained LUIS model
		if self.package_name: 
			# Returns a dictionary containing similarity rankings between the user's speech and the trained LUIS model
			intents_data = self.get_intent.get_user_intent(speech)
			# Updates the intents_data property in the command_orchestrator object with the intents data retrieved from the LUIS model
			self.command_orchestrator.intents_data = intents_data
   
		# Provides the most apporiate response and action to the user's speech
		return self.command_orchestrator.process_command(speech)
