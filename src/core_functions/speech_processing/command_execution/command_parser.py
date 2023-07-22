from src.components.commands.high_intent.translate_speech.translate_speech import TranslateSpeech
from .command_orchestrator import CommandOrchestrator

class CommandParser:
	"""
	A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
	This is done by retrieving the top intent  and its associated entity if applicable from the trained LUIS model.
	If the top intent's score is less than 90% a response is instead created using OpenAI's GPT API.
	If the top intent's score is greater than 90% the associated entity is retrieved and the appropriate action is executed.
	"""
  
	def __init__(self, api_keys: dict, speech_verbalizer:object, intents_data:dict, bot_settings:object, voice_settings:object, command_settings:object):
  
		self.api_keys = api_keys
	
		# Initialize all bot commands
		self.command = CommandOrchestrator(self.api_keys, speech_verbalizer, intents_data, bot_settings, voice_settings, command_settings)
  
		# load in the intents json produced by luis
		self.intents_data = intents_data
		
		# Minimum intent score for a command to be exucuted
		# If score is not met GPT-3.5-Turbo is used to create a response
		self.MINIMUM_INTENT_SCORE = .90
  
		# loads in all currently supported bot commands 
		self.commands = self.command.load_commands()

		# Set to True if GPT was used to create a response
		self.gpt_response = False

		# retrieving the bot's role, language, and name
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		self.command_settings = command_settings
		self._retrieve_bot_settings()

	def parse_commands(self, speech:str) -> str:
		"""
		Provides the most apporiate response and action to the user's speech given the similarity rankings.
		"""

		# Extract top intent and top intent's score from intents_data
		top_intent = self.intents_data["prediction"]["topIntent"]
		top_intent_score = self.intents_data["prediction"]["intents"][top_intent]["score"]

		# If the top intent's score is less than the minimum intent score, use GPT-3.5-Turbo to create a response
		if top_intent_score < self.MINIMUM_INTENT_SCORE:
			response = self.command.ask_gpt(speech)
		else:
			# Ensure the top intent is a supported command
			if top_intent in self.commands:
				response = getattr(self.command, top_intent.lower())()
			else:
				response = "Sorry, I don't understand that command. Please try asking again."

		# If GPT-3 was not used, translate the response to the users specified language
		# This is since GPT-3 is capable of translating the response itself
		if not self.gpt_response and self.language != 'english' and top_intent != 'Translate_Speech':
			response = TranslateSpeech(self.api_keys['TRANSLATOR-API-KEY'], self.bot_settings, self.voice_settings).translate_speech(response, 'english', self.language, True)
   
		return response

	@property
	def intents_data(self):
		return self._intents_data

	@intents_data.setter
	def intents_data(self, value):
		self._intents_data = value
		self.command.intents_data = value
	
	def _retrieve_bot_settings(self) -> None:
		"""Retrieves the bot's role, language, and name from the bot settings file"""
		self.role = self.bot_settings.retrieve_property('role')
		self.language = self.bot_settings.retrieve_property('language', 'current')
		self.bot_name = self.bot_settings.retrieve_property('name')