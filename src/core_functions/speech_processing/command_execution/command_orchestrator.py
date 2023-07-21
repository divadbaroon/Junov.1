from pathlib import Path
import json

# Import all commands
from src.components.commands.low_intent.ask_gpt.ask_gpt import AskGPT
from src.components.commands.high_intent.translate_speech.translate_speech import TranslateSpeech
from src.components.commands.high_intent.get_weather.get_weather import GetWeather
from src.components.commands.high_intent.web_searcher.web_searcher import WebSearcher
from src.components.commands.high_intent.bot_behavior.bot_behavior import BotBehavior
from src.components.commands.high_intent.set_timer.set_timer import StartTimer
from src.components.commands.high_intent.generate_password.password_generator import PasswordGenerator
from src.components.commands.high_intent.get_news.get_news import GetNews
#from src.components.commands.high_intent.play_music.play_music import PlaySong
from src.components.commands.high_intent.schedule_event.scheduler import Scheduler
from src.components.conversation_history.conversation_history_manager import ConversationHistoryManager

class CommandOrchestrator:
	"""Orchestrates the execution of all bot commands."""
 
	def __init__(self, api_keys:dict, speech_verbalizer:object, intents_data:dict, bot_settings:object, voice_settings:object, command_setttings:object):
		# retrieving the bot's role, language, and name
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		self.command_setttings = command_setttings
		self._retrieve_bot_settings()

		self.intents_data = intents_data
  
		self.speech_verbalizer = speech_verbalizer
  
		# Initialize all bot commands
		self._initilize_commands(api_keys)
  
	def _retrieve_bot_settings(self):
		# retrieving the bot's role and language
		self.role = self.bot_settings.retrieve_property('role')
		self.language = self.bot_settings.retrieve_property('language', 'current')
		self.bot_name = self.bot_settings.retrieve_property('name')
  
	def _initilize_commands(self, api_keys:dict):
		# Initialize all bot commands
		self.request_gpt = AskGPT(api_keys['OpenAI-API'], self.bot_settings, self.bot_name)
		self.request_translation = TranslateSpeech(api_keys['Translator-API'], self.bot_settings, self.voice_settings)
		self.request_weather = GetWeather(api_keys['Weather-API'])
		self.browser_request  = WebSearcher()
		self.bot_behavior = BotBehavior(self.speech_verbalizer, self.bot_settings, self.voice_settings)
		self.timer = StartTimer(self.speech_verbalizer)
		self.password_generator = PasswordGenerator()
		self.conversation_history = ConversationHistoryManager()
		self.request_news = GetNews(self.request_gpt, api_keys)
		#self.request_song = PlaySong(self.command_setttings, api_keys)
		self.schedule_event = Scheduler(self.bot_settings)
  
	def load_commands(self):
		# get the directory of the current Python script
		current_directory = Path(__file__).parent

		# construct the full path to the commands.json file
		commands_file_path = current_directory / 'supported_commands.json'

		# loads all currently supported bot commands
		with open(commands_file_path, 'r') as file:
			commands = json.load(file)
			
		return commands

	def ask_gpt(self, speech:str):
		response = self.request_gpt.ask_GPT(speech=speech) 
		self.gpt_response = True
		return response

	def translate_speech(self):
		speech_to_translate = self.intents_data["prediction"]["entities"]["translate_speech"][0]
		current_language = self.intents_data["prediction"]["entities"]["language"][0]
		new_language = self.language
		response = self.request_translation.translate_speech(speech_to_translate, current_language, new_language, one_shot_translation=True)
		return response

	def get_weather(self):
		location = self.intents_data["prediction"]["entities"].get("weather_location", [0])[0]
		response = self.request_weather.get_weather(location)
		return response

	def search_google(self):
		search_request = self.intents_data["prediction"]["entities"]["search_google"][0]
		response = self.browser_request.search_google(search_request)
		return response

	def open_website(self):
		website = self.intents_data["prediction"]["entities"]["open_website"][0]
		response = self.browser_request.open_website(website)
		return response

	def search_youtube(self):
		search_request = self.intents_data["prediction"]["entities"]["search_youtube"][0]
		response = self.browser_request.search_youtube(search_request)
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

	def start_timer(self):
		user_time = self.intents_data["prediction"]["entities"]["user_timer"][0]
		metric = self.intents_data["prediction"]["entities"]["metric"][0]
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
		self.bot_settings.save_property('status', True, 'exit')
		return response

	def get_news(self):
		response = self.request_news.get_news()
		return response

	def play_song(self):
		song_name = self.intents_data["prediction"]["entities"]["song_name"][0]
		response = self.request_song.play_song(song_name)
		return response

	def set_alarm(self):
		hour = self.intents_data["prediction"]["entities"].get("hour", [0])[0]
		minute = self.intents_data["prediction"]["entities"].get("minute", [0])[0]
		second = self.intents_data["prediction"]["entities"].get("second", [0])[0]
		am_or_pm = self.intents_data["prediction"]["entities"].get("am_or_pm", [0])[0]
		response = self.schedule_event.set_alarm(hour, minute, second, am_or_pm)
		return response

	def set_reminder(self):
		hour = self.intents_data["prediction"]["entities"].get("hour", [0])[0]
		minute = self.intents_data["prediction"]["entities"].get("minute", [0])[0]
		second = self.intents_data["prediction"]["entities"].get("second", [0])[0]
		am_or_pm = self.intents_data["prediction"]["entities"].get("am_or_pm", [0])[0]
		reminder = self.intents_data["prediction"]["entities"].get("reminder", [0])[0]
		response = self.schedule_event.set_reminder(hour, minute, second, am_or_pm, reminder)
		return response


