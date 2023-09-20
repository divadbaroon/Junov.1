from .intent_recognition import CLUIntentRecognition
from .command_orchestrator import CommandOrchestrator
 
class SpeechProcessor:
	"""
	A class that retrieves the user's intent using a trained CLU model and executes an appropriate response and action.
	"""
 
	def __init__(self, api_keys: dict, setting_objects:dict, speech_verbalizer:object):
		self._initialize_settings(setting_objects)
		self.get_intent = CLUIntentRecognition(api_keys, self.profile_settings, self.voice_settings)
		self.command_orchestrator = CommandOrchestrator(api_keys, speech_verbalizer, None, setting_objects)

	def process_speech(self, speech:str) -> str: 
		"""
		Processes the user's input using a trained CLU model (if a package is being used) and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken if applicable
		"""
		print('\nThinking...')
  
		# If a package is provided, retrieve the user's intent using the trained CLU model
		self._check_for_package(speech)
  
		# Process the user's speech and return the appropriate response and action
		return self.command_orchestrator.process_command(speech)

	def _check_for_package(self, speech) -> None:
		"""
		Handles the user's speech if a package is provided.
		"""
		if self.package_name: 
			# Returns a dictionary containing similarity rankings between the user's speech and the trained CLU model
			intents_data = self.get_intent.get_user_intent(speech)
			# Updates the intents_data property in the command_orchestrator object with the intents data retrieved from the CLU model
			self.command_orchestrator.intents_data = intents_data
	
	def _initialize_settings(self, setting_objects) -> None:
		"""
		Initialize setting objects.
		"""
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.package_name = self.profile_settings.retrieve_property('package')
