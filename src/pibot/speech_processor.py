
import requests
from pibot.bot_commands.ask_gpt import AskGPT
from pibot.bot_commands.translate_speech import TranslateSpeech
from pibot.bot_commands.conversation_manager import ConversationHistoryManager
from configuration.bot_properties import BotProperties
 
class SpeechProcessor:
	"""
	A class that processes the user's input using a trained Luis model and produces an appropriate response and action.
	This class is comprised of two initial nested classes: SpeechIntent and CommandParser.
	The nested SpeechIntent class retrieves the similarity rankings between the user's speech and the trained luis model in json format.
	The nested CommandParser class uses the data from the similarity rankings to provide the most apporiate response 
 	and action to the user's speech.
	The nested CommandParser class is composed of seven nested classes, each containing methods dedicated to executing
	commands that are specific to the user's intent.
	These clases nested under CommandParser include: AskGPT, TranslateSpeech, GetWeather, WebSearcher, PasswordGenerator,
	BotBehavior, and ConversationHistoryManager
	"""
 
	def __init__(self, luis_app_id:str, luis_key:str, openai_key:str, translator_key:str, weather_key:str, news_key:str):
		self.luis_app_id = luis_app_id
		self.luis_key = luis_key
		self.openai_key = openai_key
		self.translator_key = translator_key
		self.weather_key = weather_key
		self.news_key = news_key

	def process_speech(self, speech:str): 
		"""
		Processes the user's input using a trained LUIS model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
  
		# Retrieves a json file containing similarity rankings between the user's speech and the trained luis model
		intents_json = self.SpeechIntent(self.luis_app_id, self.luis_key).get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.CommandParser(self.openai_key, self.translator_key, self.weather_key, self.news_key).parse_commands(speech, intents_json)
		return response

	class SpeechIntent:
		"""
		A class that retrieves the similarity rankings between the user's speech and the trained luis model
		as a json file.
	
		Attributes:
		region (str): region used for Azure resources
		luis_app_id (str): application id for Azure's LUIS service
		luis_key (str): subscription key for Azure's LUIS service
		"""
  
		def __init__(self, luis_app_id:str, luis_key:str):
			self.luis_app_id = luis_app_id
			self.luis_key = luis_key

		def get_user_intent(self, speech:str):
			"""
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (str) json file containing similarity rankings between the user's speech and the trained luis model
			"""
   
			if isinstance(speech, dict):
				speech = speech['translated_speech']
		
			endpoint_url = (f"https://eastus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/{self.luis_app_id}"
							f"/slots/production/predict?verbose=true&show-all-intents=true&log=true"
							f"&subscription-key={self.luis_key}"
							f"&query={speech}")

			response = requests.get(endpoint_url)
			# Check whether request was successful
			if response.status_code == 200:
				# Returned json file of the similarity rankings between the user's speech and the trained luis model
				intents_json = response.json()
			else:
				raise ValueError(f"The request sent to the LUIS model was unsuccessful. Error: {response.status_code}")
			
			return intents_json

	class CommandParser:
		"""
		A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
		This is done by retrieving the top intent  and its associated entity if applicable from the returned json file from Luis.
		If the top intent's score is less than 70% a response is instead created using GPT-3.
		If the top intent's score is greater than 70% the associated entity is retrieved and the appropriate action is executed.
		"""
  
		def __init__(self, openai_key:str, translator_key:str, weather_key:str, news_key:str):
			self.bot_properties = BotProperties()
			self.persona = self.bot_properties.retrieve_property('persona')
			self.language = self.bot_properties.retrieve_property('language')
			self.openai_key = openai_key
			self.translator_key = translator_key
			self.weather_key = weather_key
			self.news_key = news_key
			self.gpt_response = False

		def parse_commands(self, speech:str, intents_json:dict):
			"""
			Provides the most apporiate response and action to the user's speech given the similarity rankings.
			:param speech: (str) speech input
			:param intents_json: (str) json file containing similarity rankings between the user's speech and the trained luis model
			:return: (str) response to users speech and appropriate action to be taken
			"""
   
			if isinstance(speech, dict):
				speech = speech['original_speech']

			# Extract top intent and top intent's score from intents_json
			top_intent = intents_json["prediction"]["topIntent"] 
			top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]
   
			# If score does not meet minimum threshold a response is instead created using GPT-3
			if top_intent_score < .70:
	
				# Loading conversation history to be used as context for GPT-3
				conversation_history = ConversationHistoryManager().load_conversation_history()
				response = AskGPT().ask_GPT(speech=speech, conversation_history=conversation_history, openai_key=self.openai_key, persona=self.persona, language=self.language) 
				self.gpt_response = True
	
			# Find intent with the highest similarity score
			# and retrieve associated entity if applicable
			elif top_intent == 'Translate_Speech':
				speech_to_translate = intents_json["prediction"]["entities"]["translate_speech"][0]
				language_to = intents_json["prediction"]["entities"]["language"][0]
				language_from = self.language
				response = TranslateSpeech().translate_speech(speech_to_translate, language_from, language_to, self.translator_key, one_shot_translation=True)
	
			elif top_intent == 'Get_Weather':
				location = intents_json["prediction"]["entities"]["weather_location"][0]
				from pibot.bot_commands.get_weather import GetWeather
				response = GetWeather().get_weather(location, self.weather_key)
	
			elif top_intent == 'Search_Google':
				search_request = intents_json["prediction"]["entities"]["search_google"][0]
				from pibot.bot_commands.web_searcher import WebSearcher
				response = WebSearcher().search_google(search_request)
	
			elif top_intent == 'Open_Website':
				website = intents_json["prediction"]["entities"]["open_website"][0]
				from pibot.bot_commands.web_searcher import WebSearcher
				response = WebSearcher().open_website(website)
	
			elif top_intent == 'Search_Youtube':
				search_request = intents_json["prediction"]["entities"]["search_youtube"][0]
				from pibot.bot_commands.web_searcher import WebSearcher
				response = WebSearcher().search_youtube(search_request)
	
			elif top_intent == 'Change_Persona':
				new_persona = intents_json["prediction"]["entities"]["new_persona"][0]
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().change_persona(new_persona)
	
			elif top_intent == 'Change_Gender':
				new_gender = intents_json["prediction"]["entities"]["new_gender"][0]
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().change_gender(new_gender)
	
			elif top_intent == 'Change_Language':
				new_language = intents_json["prediction"]["entities"]["new_language"][0]
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().change_language(new_language)
    
			elif top_intent == 'Change_Voice':
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().change_voice()
    
			elif top_intent == 'Randomize_Voice':
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().randomize_voice()
	
			elif top_intent == 'Create_Image':
				image = intents_json["prediction"]["entities"]["image_to_create"][0]
				response = AskGPT().create_gpt_image(image, self.openai_key)
    
			elif top_intent == 'Start_Timer':
				user_time = intents_json["prediction"]["entities"]["user_timer"][0]
				metric = intents_json["prediction"]["entities"]["metric"][0]
				from pibot.bot_commands.timer import StartTimer
				response = StartTimer().start_timer(user_time, metric)

			elif top_intent == 'Generate_Password':
				from pibot.bot_commands.password_generator import PasswordGenerator
				response = PasswordGenerator().generate_password()
			elif top_intent == 'Mute':
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().toggle_mute()
			elif top_intent == 'Unmute':
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().untoggle_mute()
			elif top_intent == 'Pause':
				from pibot.bot_commands.bot_behavior import BotBehavior
				response = BotBehavior().pause()
			elif top_intent == 'Get_Conversation_History':
				response = ConversationHistoryManager().get_conversation_history(self.persona)
			elif top_intent == 'Clear':
				response = ConversationHistoryManager().clear_conversation_history()
			elif top_intent == 'Quit':
				response = ConversationHistoryManager().exit_and_clear()
			else:                                                                                                                                                     
				response = "Sorry, I don't understand that command. Please try asking again."

			# If GPT-3 was not used translate the response to the users language
			# This is since GPT-3 is capable of translating the response itself
			if not self.gpt_response and self.language != 'english' and top_intent != 'Translate_Speech':
				response = TranslateSpeech().translate_speech(speech_to_translate=response, language_from='english', language_to=self.language, translator_key=self.translator_key)
    
			# If the command is not to clear or quit the conversation history is saved
			if top_intent_score < .70 and top_intent != 'Clear' and top_intent != 'Quit':
				ConversationHistoryManager().save_conversation_history(speech, response, self.persona)
			# If the response is a dictionary only save the response
			elif isinstance(response, dict):
				ConversationHistoryManager().save_conversation_history(speech, response['response'], self.persona)

			return response