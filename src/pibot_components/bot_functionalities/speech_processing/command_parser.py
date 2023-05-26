from settings.settings_orchestrator import SettingsOrchestrator
from src.pibot_components.bot_commands.ask_gpt import AskGPT
from src.pibot_components.bot_commands.translate_speech import TranslateSpeech
from src.pibot_components.bot_commands.get_weather import GetWeather
from src.pibot_components.bot_commands.web_searcher import WebSearcher
from src.pibot_components.bot_commands.bot_behavior import BotBehavior
from src.pibot_components.bot_commands.timer import StartTimer
from src.pibot_components.bot_commands.password_generator import PasswordGenerator

class CommandParser:
	"""
	A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
	This is done by retrieving the top intent  and its associated entity if applicable from the returned json file from CLU.
	If the top intent's score is less than 70% a response is instead created using GPT-3.
	If the top intent's score is greater than 70% the associated entity is retrieved and the appropriate action is executed.
	"""
  
	def __init__(self, openai_key:str, translator_key:str, weather_key:str):
		self.bot_settings = SettingsOrchestrator()
		self.openai_key = openai_key
		self.translator_key = translator_key
		self.weather_key = weather_key
		self.persona = self.bot_settings.retrieve_bot_property('persona')
		self.language = self.bot_settings.retrieve_bot_property('language')
		self.gpt_response = False
		self.commands = {
			'Ask_GPT': self.ask_gpt,
			'Translate_Speech': self.translate_speech,
			'Get_Weather': self.get_weather,
			'Search_Google': self.search_google,
			'Open_Website': self.open_website,
			'Search_Youtube': self.search_youtube,
			'Change_Persona': self.change_persona,
			'Change_Gender': self.change_gender,
			'Change_Language': self.change_language,
			'Change_Voice': self.change_voice,
			'Randomize_Voice': self.randomize_voice,
			'Start_Timer': self.start_timer,
			'Generate_Password': self.generate_password,
			'Mute': self.mute,
			'Unmute': self.unmute,
			'Pause': self.pause,
			'Get_Conversation_History': self.get_conversation_history,
			'Clear': self.clear,
			'Quit': self.quit,
		}
   
	def ask_gpt(self, speech):
		# Loading conversation history to be used as context for GPT-3
		conversation_history = self.bot_settings.load_conversation_history()
		response = AskGPT(self.openai_key).ask_GPT(speech=speech, conversation_history=conversation_history, persona=self.persona, language=self.language) 
		self.gpt_response = True
		return response

	def translate_speech(self, speech=None, intents_json=None):
		speech_to_translate = intents_json["prediction"]["entities"]["translate_speech"][0]
		language_to = intents_json["prediction"]["entities"]["language"][0]
		language_from = self.language
		response = TranslateSpeech(self.translator_key).translate_speech(speech_to_translate, language_from, language_to, one_shot_translation=True)
		return response

	def get_weather(self, speech=None, intents_json=None):
		location = intents_json["prediction"]["entities"]["weather_location"][0]
		response = GetWeather(self.weather_key).get_weather(location)
		return response

	def search_google(self, speech=None, intents_json=None):
		search_request = intents_json["prediction"]["entities"]["search_google"][0]
		response = WebSearcher().search_google(search_request)
		return response

	def open_website(self, speech=None, intents_json=None):
		website = intents_json["prediction"]["entities"]["open_website"][0]
		response = WebSearcher().open_website(website)
		return response

	def search_youtube(self, speech=None, intents_json=None):
		search_request = intents_json["prediction"]["entities"]["search_youtube"][0]
		response = WebSearcher().search_youtube(search_request)
		return response

	def change_persona(self, speech=None, intents_json=None):
		new_persona = intents_json["prediction"]["entities"]["new_persona"][0]
		response = BotBehavior().change_persona(new_persona)
		return response

	def change_gender(self, speech=None, intents_json=None):
		new_gender = intents_json["prediction"]["entities"]["new_gender"][0]
		response = BotBehavior().change_gender(new_gender)
		return response

	def change_language(self, speech=None, intents_json=None):
		new_language = intents_json["prediction"]["entities"]["new_language"][0]
		response = BotBehavior().change_language(new_language)
		return response

	def change_voice(self, speech=None, intents_json=None):
		response = BotBehavior().change_voice()
		return response

	def randomize_voice(self, speech=None, intents_json=None):
		response = BotBehavior().randomize_voice()
		return response

	def start_timer(self, speech=None, intents_json=None):
		user_time = intents_json["prediction"]["entities"]["user_timer"][0]
		metric = intents_json["prediction"]["entities"]["metric"][0]
		response = StartTimer().start_timer(user_time, metric)
		return response

	def generate_password(self, speech=None, intents_json=None):
		response = PasswordGenerator().generate_password()
		return response

	def mute(self, speech=None, intents_json=None):
		response = BotBehavior().mute()
		return response

	def unmute(self, speech=None, intents_json=None):
		response = BotBehavior().unmute()
		return response

	def pause(self, speech=None, intents_json=None):
		response = BotBehavior().pause()
		return response

	def get_conversation_history(self, speech=None, intents_json=None):
		response = self.bot_settings.get_conversation_history(self.persona)
		return response

	def clear(self, speech=None, intents_json=None):
		response = self.bot_settings.clear_conversation_history()
		return response

	def quit(self, speech=None, intents_json=None):
		response = self.bot_settings.exit_and_clear_conversation_history()
		return response

	def parse_commands(self, speech:str, intents_json:dict):
		"""
		Provides the most apporiate response and action to the user's speech given the similarity rankings.
		:param speech: (str) speech input
		:param intents_json: (str) json file containing similarity rankings between the user's speech and the trained CLU model
		:return: (str) response to users speech and appropriate action to be taken
		"""

		if isinstance(speech, dict):
			speech = speech['original_speech']

		# Extract top intent and top intent's score from intents_json
		#top_intent = intents_json["prediction"]["topIntent"] 
		#top_intent_score = None
		#for intent in intents_json["prediction"]["intents"]:
			#if intent["category"] == top_intent:
				#top_intent_score = intent["confidenceScore"]
				#break

		# Extract top intent and top intent's score from intents_json
		top_intent = intents_json["prediction"]["topIntent"] 
		top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]

		if top_intent_score < .90:
			response = self.ask_gpt(speech)
		else:
			if top_intent in self.commands:
				response = self.commands[top_intent](speech, intents_json)
			else:
				response = "Sorry, I don't understand that command. Please try again."
		# ...
		# If GPT-3 was not used translate the response to the users language
		# This is since GPT-3 is capable of translating the response itself
		if not self.gpt_response and self.language != 'english' and top_intent != 'Translate_Speech':
			response = TranslateSpeech().translate_speech(speech_to_translate=response, language_from='english', language_to=self.language, translator_key=self.translator_key)

		# If the command is not to clear or quit, the conversation history is saved
		if top_intent_score < .70 and top_intent != 'Clear' and top_intent != 'Quit':
			self.bot_settings.save_conversation_history(speech, response, self.persona)
		# If the response is a dictionary only save the response
		elif isinstance(response, dict):
			self.bot_settings.save_conversation_history(speech, response['response'], self.persona)

		return response