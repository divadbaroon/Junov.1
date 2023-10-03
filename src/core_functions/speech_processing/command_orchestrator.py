from src.packages.virtual_assistant.commands.high_intent.translate_speech.translate_speech import TranslateSpeech
from src.packages.virtual_assistant.commands.low_intent.ask_gpt.ask_gpt import AskGPT
from importlib import import_module
from src.utilities.logs.log_performance import PerformanceLogger

logger = PerformanceLogger()

class CommandOrchestrator:
	"""
	A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
	This is done by retrieving the top intent  and its associated entity if applicable from the trained CLU model.
	If the top intent's score is less than 90% a response is instead created using OpenAI's GPT API.
	If the top intent's score is greater than 90% the associated entity is retrieved and the appropriate action is executed.
	"""
  
	def __init__(self, api_keys: dict, speech_verbalizer:object, intents_data:dict, setting_objects:dict):
		self.api_keys = api_keys
		self._retrieve_master_settings(setting_objects)
		self._load_in_commands(speech_verbalizer, intents_data, setting_objects)
		self.MINIMUM_INTENT_SCORE = .90
		self._intents_data = intents_data

	def process_command(self, speech:str) -> str:
		"""
		Provides the most apporiate response and action to the user's speech given the similarity rankings.
		"""
		# Retrieve the top intent and its associated entity if applicable from the trained CLU model
		if self.intents_data:
			response = self._execute_command(speech)
		else:
			response = self.command.ask_GPT(speech)
  
		return response

	@logger.log_operation
	def _retrieve_top_intent(self) -> str:
		"""
		Retrieves the top intent and its associated entity if applicable from data returned from the trained CLU model.
		"""
		# Extract top intent and top intent's score from intents_data
		top_intent = self.intents_data["result"]["prediction"]["topIntent"]
		# Now find the confidence score of this top intent
		for intent_data in self.intents_data["result"]["prediction"]["intents"]:
			if intent_data["category"] == top_intent:
				top_intent_score = intent_data["confidenceScore"]
    
				if top_intent_score < self.MINIMUM_INTENT_SCORE:
					top_intent = None
				return top_intent, top_intent_score

	def _execute_command(self, speech:str) -> None:
		"""
		Executes the appropriate action given the top intent and its associated entity if applicable.
		"""
		top_intent = self._retrieve_top_intent()
  
		if top_intent:
			if top_intent in self.commands:
				response = getattr(self.command, top_intent.lower())()
			else:
				response = "Sorry, I don't understand that command. Please try asking again."
		else:
			response = self.command.ask_GPT(speech)
		return response
  
	def _retrieve_master_settings(self, setting_objects:dict) -> None:
		"""
  		Retrieves the bot's role, language, and name from the bot settings file
    	"""
		profile_settings = setting_objects['profile_settings']
		self.role = profile_settings.retrieve_property('role')
		self.language = profile_settings.retrieve_property('current_language')
		self.bot_name = profile_settings.retrieve_property('name')
		self.package = profile_settings.retrieve_property('package')

	def _load_in_commands(self, speech_verbalizer:object, intents_data:dict, setting_objects:dict):
		"""
  		Loads in all currently supported bot commands supported by the bot's package.
    	"""
		if self.package:
			# initialize and load in all currently supported bot commands 
			self.CommandParser = getattr(import_module(f"src.packages.{self.package}.commands.command_parser"), "CommandParser")

			self.command = self.CommandParser(self.api_keys, speech_verbalizer, intents_data, setting_objects)
			self.commands = self.command.load_commands()
			# dict of similarity rankings returned by CLU
			self.intents_data = intents_data
		else:
			self.command = AskGPT(self.api_keys['OPENAI-API-KEY'], setting_objects)
			self.top_intent_score = None
			self.intents_data = None
   
		all_commands = []
		for command in self.commands['high_intent']:
			all_commands.append(command)
		for command in self.commands['low_intent']:
			all_commands.append(command)
		self.commands = all_commands

	@property
	def intents_data(self):
		return self._intents_data

	@intents_data.setter
	def intents_data(self, value):
		self._intents_data = value
		self.command.intents_data = value
	