from code.components.commands.translate_speech.translate_speech import TranslateSpeech
from .command_orchestrator import CommandOrchestrator

class CommandParser:
	"""
	A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
	This is done by retrieving the top intent  and its associated entity if applicable from the returned json file from CLU.
	If the top intent's score is less than 70% a response is instead created using GPT-3.
	If the top intent's score is greater than 70% the associated entity is retrieved and the appropriate action is executed.
	"""
  
	def __init__(self, api_keys: dict, speech_verbalizer:object, intents_json:dict, bot_settings:object, voice_settings:object):
		
		# load in the intents json produced by luis
		self.intents_json = intents_json
  
		self.api_keys = api_keys
	
		# Initialize all bot commands
		self.command = CommandOrchestrator(self.api_keys, speech_verbalizer, intents_json, bot_settings, voice_settings)
		
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
		self._retrieve_bot_settings()
  
	def _retrieve_bot_settings(self):
		"""Retrieves the bot's role, language, and name from the bot settings file"""
		self.role = self.bot_settings.retrieve_property('role')
		self.language = self.bot_settings.retrieve_property('language')
		self.bot_name = self.bot_settings.retrieve_property('name')

	def parse_commands(self, speech:str):
		"""
		Provides the most apporiate response and action to the user's speech given the similarity rankings.
		:param speech: (str) speech input
		:param intents_json: (str) json file containing similarity rankings between the user's speech and the trained CLU model
		:return: (str) response to users speech and appropriate action to be taken
		"""

		# Extract top intent and top intent's score from intents_json
		top_intent = self.intents_json["prediction"]["topIntent"]
		top_intent_score = self.intents_json["prediction"]["intents"][top_intent]["score"]

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
			response = TranslateSpeech(translator_key=self.api_keys['translator_key']).translate_speech(speech_to_translate=response, current_language='english', new_language=self.language, one_shot_translation=True)
   
		return response