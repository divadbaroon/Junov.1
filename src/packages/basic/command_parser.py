import yaml
from src.packages.virtual_assistant.low_intent.ask_gpt.ask_gpt import AskGPT
from src.packages.virtual_assistant.high_intent.bot_behavior.bot_behavior import BotBehavior

class CommandParser:
	
	def __init__(self, api_keys:dict, speech_verbalizer:object, intents_data:dict, setting_objects:dict):
		self.speech_verbalizer = speech_verbalizer
		self.setting_objects = setting_objects
		self.intents_data = intents_data
		
		self._retrieve_master_settings()
		self._initialize_commands(api_keys)
  
	def load_commands(self):
		# path to 'supported_commands.yaml'
		commands_file_path = 'src/packages/basic/supported_commands.yaml'
  
		# loads all currently supported bot commands
		with open(commands_file_path, 'r') as f:
			commands = yaml.safe_load(f)
			
		return commands
	
	def _initialize_commands(self, api_keys:dict):
		self.request_gpt = AskGPT(api_keys['OPENAI-API-KEY'], self.setting_objects, self.bot_name)
		self.bot_behavior = BotBehavior(self.speech_verbalizer, self.setting_objects)
		
	def _retrieve_master_settings(self):
		# retrieving the bot's role and language
		profile_settings = self.setting_objects['profile_settings']
		self.role = profile_settings.retrieve_property('role')
		self.language = profile_settings.retrieve_property('language')
		self.bot_name = profile_settings.retrieve_property('name')
  
	def ask_gpt(self, speech:str):
		response = self.request_gpt.ask_GPT(speech=speech) 
		self.gpt_response = True
		return response
  
	def change_role(self):
		new_role = self.intents_data["prediction"]["entities"]["new_role"][0]
		response = self.bot_behavior.change_role(new_role)
		return response

	def change_gender(self):
		new_gender = self.intents_data["prediction"]["entities"]["new_gender"][0]
		response = self.bot_behavior.change_gender(new_gender)
		return response

	def change_language(self):
		new_language = self.intents_data["prediction"]["entities"]["new_language"][0]
		response = self.bot_behavior.change_language(new_language)
		return response

	def change_voice(self):
		response = self.bot_behavior.change_voice()
		return response

	def randomize_voice(self):
		response = self.bot_behavior.randomize_voice()
		return response

	def mute(self):
		response = self.bot_behavior.mute()
		return response

	def unmute(self):
		response = self.bot_behavior.unmute()
		return response

	def pause(self):
		response = self.bot_behavior.pause()
		return response

	# FIX
	def quit(self):
		#response = self.conversation_history.exit_and_clear_conversation_history()
		self.setting_objects['master_settings'].save_property('status', True, 'exit')
		#return response