from src.components.commands.ask_gpt.ask_gpt import AskGPT
from src.components.commands.translate_speech.translate_speech import TranslateSpeech
from src.components.commands.get_weather.get_weather import GetWeather
from src.components.commands.web_searcher.web_searcher import WebSearcher
from src.components.commands.behavior.behavior import BotBehavior
from src.components.commands.timer.timer import StartTimer
from src.components.commands.password_generator.password_generator import PasswordGenerator
from settings.conversation_history.conversation_history_manager import ConversationHistoryManager
from pathlib import Path
import json

class Commands:
	
	def __init__(self, api_keys:dict, speech_verbalizer:object, intents_json:dict, bot_settings:object) -> None:
		
		# retrieving the bot's role, language, and name
		self.bot_settings = bot_settings
		self._retrieve_bot_settings()
     
		# Initialize all bot commands
		self.request_gpt = AskGPT(api_keys['openai_key'], self.bot_settings, self.bot_name)
		self.request_translation = TranslateSpeech(api_keys['translator_key'])
		self.request_weather = GetWeather(api_keys['weather_key'])
		self.browser_request  = WebSearcher()
		self.bot_behavior = BotBehavior(speech_verbalizer)
		self.timer = StartTimer(speech_verbalizer)
		self.password_generator = PasswordGenerator()
		self.conversation_history = ConversationHistoryManager()
  
		self.intents_json = intents_json
  
		self.speech_verbalizer = speech_verbalizer
  
	def _retrieve_bot_settings(self):
		# retrieving the bot's role and language
		self.role = self.bot_settings.retrieve_bot_property('role')
		self.language = self.bot_settings.retrieve_bot_property('language')
		self.bot_name = self.bot_settings.retrieve_bot_property('name')
  
	def load_commands(self):
		# get the directory of the current Python script
		current_directory = Path(__file__).parent

		# construct the full path to the commands.json file
		commands_file_path = current_directory / 'commands.json'

		# loads all currently supported bot commands
		with open(commands_file_path, 'r') as file:
			commands = json.load(file)
			
		return commands

	def ask_gpt(self, speech):
		response = self.request_gpt.ask_GPT(speech=speech, bot_name=self.bot_name) 
		self.gpt_response = True
		return response

	def translate_speech(self):
		speech_to_translate = self.intents_json["prediction"]["entities"]["translate_speech"][0]
		language_to = self.intents_json["prediction"]["entities"]["language"][0]
		language_from = self.language
		response = self.request_translation.translate_speech(speech_to_translate, language_from, language_to, one_shot_translation=True)
		return response

	def get_weather(self):
		location = self.intents_json["prediction"]["entities"]["weather_location"][0]
		response = self.request_weather.get_weather(location)
		return response

	def search_google(self):
		search_request = self.intents_json["prediction"]["entities"]["search_google"][0]
		response = self.browser_request.search_google(search_request)
		return response

	def open_website(self):
		website = self.intents_json["prediction"]["entities"]["open_website"][0]
		response = self.browser_request.open_website(website)
		return response

	def search_youtube(self):
		search_request = self.intents_json["prediction"]["entities"]["search_youtube"][0]
		response = self.browser_request.search_youtube(search_request)
		return response

	def change_role(self):
		new_role = self.intents_json["prediction"]["entities"]["new_role"][0]
		response = self.bot_behavior.change_role(new_role)
		return response

	def change_gender(self):
		new_gender = self.intents_json["prediction"]["entities"]["new_gender"][0]
		response = self.bot_behavior.change_gender(new_gender)
		return response

	def change_language(self):
		new_language = self.intents_json["prediction"]["entities"]["new_language"][0]
		response = self.bot_behavior.change_language(new_language)
		return response

	def change_voice(self):
		response = self.bot_behavior.change_voice()
		return response

	def randomize_voice(self):
		response = self.bot_behavior.randomize_voice()
		return response

	def start_timer(self):
		user_time = self.intents_json["prediction"]["entities"]["user_timer"][0]
		metric = self.intents_json["prediction"]["entities"]["metric"][0]
		response = self.timer.start_timer(user_time, metric)
		return response

	def generate_password(self):
		response = self.password_generator.generate_password()
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

	def get_conversation_history(self):
		response = self.conversation_history.get_conversation_history(self.role)
		return response

	def clear(self):
		response = self.conversation_history.clear_conversation_history()
		return response

	def quit(self):
		response = self.conversation_history.exit_and_clear_conversation_history()
		self.bot_settings.save_bot_property('exit_status', True)
		return response
