import config 
import openai 
import requests
import webbrowser
import json
import uuid
import urllib
import sys
import string
import pyperclip
from random import choice
from speech_verbalizer import SpeechVerbalizer
from bot_properties import BotProperties

class SpeechProcessor:
	"""
	A class that processes the user's input using a trained Luis model and produces an appropriate response and action.
	This class is comprised of two initial nested classes: SpeechIntent and CommandParser.
	The nested SpeechIntent class retrieves the similarity rankings between the user's speech and the trained luis model.
	The nested CommandParser class uses the data from the similarity rankings to provide the most apporiate response 
 	and action to the user's speech.
	The nested CommandParser class is composed of seven nested classes, each containing methods dedicated to executing
	commands that are specific to the user's intent.
	These clases nested under CommandParser include: ChatGPT, TranslateSpeech, GetWeather, WebSearcher, PasswordGenerator,
	BotBehavior, and ConversationHistoryManager
	"""

	def process_speech(self, speech:str): 
		"""
		Processes the user's input using Azure's LUIS Service and produces an appropriate response and action.
		"""
		# Retrieves a json file containing similarity rankings between the user's speech and the trained luis model
		intents_json = self.SpeechIntent().get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.CommandParser().parse_commands(intents_json, speech)
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
		
		def __init__(self):
			self.region = 'eastus'
			self.luis_app_id = config.retrieve_secret('Luis-APP-ID')
			self.luis_key = config.retrieve_secret('Luis-API')

		def get_user_intent(self, speech:str):
			"""
			Retrieves the similarity rankings between the user's speech and the trained luis model.
			"""
		
			endpoint_url = (f"https://{self.region}.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/{self.luis_app_id}"
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
		If the top intent's score is less than 70% a response is instead created using chatGPT.
		If the top intent's score is greater than 70% the associated entity is retrieved and the appropriate action is executed.
		"""

		def parse_commands(self, intents_json, speech):
			"""
			Provides the most apporiate response and action to the user's speech given the similarity rankings.
			"""
			# Extract top intent from similarity_rankings json file
			top_intent = intents_json["prediction"]["topIntent"] 
			top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]
		
			# If score does not meet minimum threshold a response is instead created using chatGPT
			if top_intent_score < .70:
				conversation_history = self.ConversationHistoryManager().load_conversation_history()
				response = self.ChatGPT().ask_chatgpt(speech, conversation_history) 
	
			# Find intent with the highest similarity score
			# and retrieve associated entity if applicable
			elif top_intent == 'Translate_Speech':
				speech_to_translate = intents_json["prediction"]["entities"]["translate_speech"][0]
				language = intents_json["prediction"]["entities"]["language"][0]
				response = self.TranslateSpeech().translate_speech(speech_to_translate, language)
	
			elif top_intent == 'Get_Weather':
				location = intents_json["prediction"]["entities"]["weather_location"][0]
				response = self.GetWeather().get_weather(location)
	
			elif top_intent == 'Search_Google':
				search_request = intents_json["prediction"]["entities"]["search_google"][0]
				response = self.WebSearcher().search_google(search_request)
	
			elif top_intent == 'Open_Website':
				website = intents_json["prediction"]["entities"]["open_website"][0]
				response = self.WebSearcher().open_website(website)
	
			elif top_intent == 'Search_Youtube':
				search_request = intents_json["prediction"]["entities"]["search_youtube"][0]
				response = self.WebSearcher().search_youtube(search_request)
    
			elif top_intent == 'Change_Persona':
				new_persona = intents_json["prediction"]["entities"]["new_persona"][0]
				response = self.BotBehavior().change_persona(new_persona)
    
			elif top_intent == 'Change_Gender':
				new_gender = intents_json["prediction"]["entities"]["new_gender"][0]
				response = self.BotBehavior().change_gender(new_gender)
    
			elif top_intent == 'Change_Language':
				new_language = intents_json["prediction"]["entities"]["new_language"][0]
				response = self.BotBehavior().change_language(new_language)

			elif top_intent == 'Generate_Password':
				response = self.PasswordGenerator().generate_password()
			elif top_intent == 'Mute':
				response = self.BotBehavior().toggle_mute()
			elif top_intent == 'Unmute':
				response = self.BotBehavior().untoggle_mute()
			elif top_intent == 'Pause':
				response = self.BotBehavior().pause()
			elif top_intent == 'Get_Conversation_History':
				response = self.ConversationHistoryManager().get_conversation_history()
			elif top_intent == 'Log_Conversation':
				response = self.ConversationHistoryManager().log_conversation()
			elif top_intent == 'Clear':
				response = self.ConversationHistoryManager().clear()
			elif top_intent == 'Quit':
				response = self.ConversationHistoryManager().exit_and_clear()
			else:
				response = "Sorry, I don't understand that command. Please try asking again."
			
			# Saving the new conversation to conversation_history.json 
			self.ConversationHistoryManager().save_conversation_history(speech, response)
	
			return response

		class ChatGPT:
			"""
			A class that creates a response using OpenAI's chatGPT.
			A personalize resposne is created depening on the user's specified persona and
			the past conversation history to provie context to the conversation.
		
			Atributes:
			language_model (str): language model used for chatGPT
			response_length (int): max response length of chatGPT's responses
			openai.api_key (str): subscription key for OpenAi's chatGPT
			"""
			
			def __init__(self):
				self.language_model = "text-davinci-003"
				self.response_length = 100
				openai.api_key = config.retrieve_secret('OpenAI-API')
				self.persona = BotProperties().get_property('persona')

			def ask_chatgpt(self, speech:str, conversation_history=None):
				"""
				Creates a response using OpenAI's chatGPT.
				"""

				formatted_conversation_history = ""
			
				# Formats conversation history to be used as prompt for chatgpt 
				if conversation_history:
					for conversation in conversation_history:
						formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
						for name, text in conversation.items():
							if name != 'User':
								formatted_conversation_history += f"Response: \n{name.title()}: {text}\n\n"

				# Creates prompt used for chatgpt
				if self.persona != 'chatbot' and formatted_conversation_history:
					prompt = (f"Provide the next response to the user given this conversation history {formatted_conversation_history}. I want you to respond to the user like you are {self.persona}: The user said: {speech}")
				elif self.persona == 'chatbot' and formatted_conversation_history:
					prompt = (f"Provide the next response to the user given this conversation history {formatted_conversation_history}. Provide a realistic chatbot like response to the user: The user said: {speech}")
				elif self.persona != 'chatbot' and not formatted_conversation_history:
					prompt = (f"I want you to respond to the user like you are {self.persona}. The user said: {speech}")
				else:
					prompt = (f"Provide a realistic chatbot like response to the user: The user said: {speech}")

				completion = openai.Completion.create(
				engine=self.language_model,
				prompt=prompt,
				max_tokens=self.response_length,
				n=1,
				stop=None,
				temperature=0.5)
				
				try:
					response = completion.choices[0].text
				except Exception as e:
					print(f"An error has occurred while sending a request to chatGPT. Error: {e}")
					response = 'Sorry, an error has occured. Please try asking again.'

				# Cleanup common mistakes that chatGPT returns
				response = response.replace('\n\n', ' ').replace(f'{self.persona}:', '').replace('Response:', '').lstrip()
				
				return response

		class TranslateSpeech:
			"""
			A class that translates speech to a desired language.
		
			Atributes:
			translator_key (str): subscription key for Azure's Translator service
			"""
			
			def __init__(self):
				self.region = 'eastus'
				self.translator_key = config.retrieve_secret('PiBot-Translator-API')
			
			def translate_speech(self, speech_to_translate:str, language:str):
				"""
				Translates a given string of text to a desired langauge
				:param speech_to_translate: (str) the speech to be translated
				:param language: (str) the language for the speech to be translated into
				:return: (str) speech translation
				"""
				endpoint = "https://api.cognitive.microsofttranslator.com/"
				path = '/translate'
				constructed_url = f'{endpoint}{path}'
				
				try:
					with open('bot_properties.json', 'r') as f:  
						languages = json.load(f)
				except FileNotFoundError:
					print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')

				# Language sometimes ends in a question mark
				if language.endswith('?'):
					language = language.rstrip('?')

				# Get language code from langauge
				language_code = languages['language_codes'].get(language) 
				params = {
					'api-version': '3.0',
					'from': 'en',
					'to': language_code
				}

				headers = {
					'Ocp-Apim-Subscription-Key': self.translator_key,
					'Ocp-Apim-Subscription-Region': self.region,
					'Content-type': 'application/json',
					'X-ClientTraceId': str(uuid.uuid4())
				}

				body = [{"text": speech_to_translate}]
		
				try:
					request = requests.post(constructed_url, params=params, headers=headers, json=body)
					response = request.json()
					response = response[0]['translations'][0]['text']
				except Exception as e:
					print(f"An error occurred while sending a request to microsoft translator. Error: {e}")
					response = f'Sorry, there was an error while trying translate {speech_to_translate}. Try asking again.'
		
				return response

		class GetWeather:
			"""
			A class that gets the weather for a given location.
		
			Atributes:
			weather_key (str): subscription key for OpenWeatherMap's weather api
			"""
			
			def __init__(self):
				self.weather_key = config.retrieve_secret('Weather-API')
			
			def get_weather(self, location:str):
				"""
				Gets the weather for a given location.
				"""
				
				# The location sometimes ends in a question mark
				if location.endswith('?'):
					location = location.rstrip('?')
			
				# Attempt to send request to openweathermap api
				try:
					response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_key}")
				except Exception as e:
					print(f"An error occurred while trying to send a request to openweathermap. Error: {e}")
					response = "Sorry, an error has occured. Please try asking again."
					return response

				# Check whether request was successful
				if response.status_code != 200:
					print(f"An error occurred while trying to send a request to openweathermap. Error: {response.status_code}")
					response = "Sorry, an error has occured. Please try asking again."
					return response
				# Returned json file with weather data
				data = response.json()

				temperature = data["main"]["temp"]

				# Convert temperature from kelvin to fahrenheit
				temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32

				response = f"The weather in {location} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
				
				return response

		class WebSearcher:
			"""
			A class that contains methods that opens a desired website, 
			performs a google search, or performs a youtube search.
			"""
				
			def open_website(self, website: str):
				"""
				Opens a user requested website
				:param website: (str) the website to open
				"""
				webbrowser.open(f"https://www.{website}.com")
		
				return f'Opening {website}'

			def search_google(self, search_request: str):
				"""
				Performs a google search for the given query
				:param search_request: (str) the google search request
				"""
				webbrowser.open(f"https://www.google.com/search?q={search_request}")
				
				return f'Searching google for {search_request}'
			
			def search_youtube(self, search_request: str):
				"""
				Performs a youtube search for the given query
				:param search_request: (str) the youtube search request
				"""
				# Encode the search request to be url friendly
				query = urllib.parse.quote(search_request)
				webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
				
				return f'Searching youtube for {search_request}'

		class PasswordGenerator:
			"""
			A class that generates a random password and copies it to the users clipboard.
			"""
			
			def generate_password(self, length=16):
				"""
				Generates a random password of a given length
				:param length: (int) the length of the password
				"""
				password = ''
				# Generate random password
				for _ in range(length):
					password += choice(string.ascii_letters + string.digits + string.punctuation)
				# Copy password
				pyperclip.copy(password)
				return 'A random password has been created and copied to your clipboard.'

		class BotBehavior:
			"""
			A class that contains methods that change the behavior of the bot.
		
			Atributes:
			speech_verbalizer: an object of the SpeechVerbalizer class
			"""
			
			def __init__(self):
				self.speech_verbalizer = SpeechVerbalizer()
				self.bot_properties = BotProperties()
			
			def toggle_mute(self):
				"""
				Mutes the bot
				"""
				self.bot_properties.save_property('mute_status', True)
				return 'I am now muted.'
		
			def untoggle_mute(self):
				"""
				Unmutes the bot
				"""
				self.bot_properties.save_property('mute_status', False)
				return 'I am now unmuted.'

			def pause(self):
				"""
				Pauses the bot
				The user must press the spacebar to unpause the bot
				"""
				self.speech_verbalizer.verbalize_speech(speech='I am now paused')
				user_input = ''
				while user_input != ' ':
					user_input = input('Press spacebar to unpause: ')
				return 'I am now unpaused.'

			def change_persona(self, new_persona:str):
				"""
				Changes the bot's persona
				"""
				self.bot_properties.save_property('persona', new_persona)
				return f'Ok, I have changed my persona to {new_persona}.'
			
			def change_gender(self, new_gender:str):
				"""
				Changes the bot's gender
				"""
				# Making sure user input is valid
				if new_gender not in ['male', 'female']:
					return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
				else:
					self.bot_properties.save_property('gender', new_gender)
		
					return f'Ok, I have changed my gender to {new_gender}.'
			
			def change_language(self, new_language:str):
				"""
				Changes the bot's language
				"""
				# Extracting all currently supported languages
				langauge_codes = self.bot_properties.get_property('language_codes')
				# Check if language is supported
				if new_language in langauge_codes.keys():
					self.bot_properties.save_property('language', new_language)
				else:
					return f"Sorry, {new_language} is not currently supported."
		
				return f'Ok, I have changed my language to {new_language}.'

		class ConversationHistoryManager:
			"""
			A class that manages the conversation history in the file "conversation_history.json".
		
			Atributes:
			speech_verbalizer: an object of the SpeechVerbalizer class
			"""
			
			def __init__(self):
				self.speech_verbalizer = SpeechVerbalizer()
				self.persona = BotProperties().get_property('persona')

			def load_conversation_history(self):
				"""
				Loads the conversation history from the conversation_history.json file
				"""
				try:
					with open('conversation_history.json', 'r') as f:
						data = json.load(f)
						conversation_history = data["conversation"]
				except FileNotFoundError:
					print('The file "conversation_history.json" is missing.\nMake sure all files are located within the same folder')
					conversation_history = []

				return conversation_history

			def get_conversation_history(self):
				"""
				Gets the conversation history from the conversation_history.json file
				"""
				# load conversation history from conversation_history.json file
				conversation_history = self.load_conversation_history()
				formatted_conversation_history = ""
			
				if conversation_history:
					for conversation in conversation_history:
						formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
						formatted_conversation_history += f"Response: \n{self.persona}: {conversation[self.persona]}\n\n"

				print(f'\nConversation History: \n{formatted_conversation_history}')
				return 'Ok, I have printed the conversation history to the console'

			def log_conversation(self): # WIP
				"""
				Log the most recent conversation
				"""
				conversation_history = self.load_conversation_history()
				most_recent_conversation = conversation_history[-1]
				data = {"logs": most_recent_conversation}
				return 'Sorry about that, I will send the conversation to my creator to imrpove my response.'
				
			def save_conversation_history(self, speech: str, response: str):
				"""
				Loads conversation history from json file
				:return: (list) conversation history
				"""
				conversation_history = self.load_conversation_history()
			
				new_conversation = {
				"User": speech,
				self.persona.title(): response
				}
				conversation_history.append(new_conversation)
				data = {"conversation": conversation_history}
				try:
					with open("conversation_history.json", "w", encoding="utf-8") as f:
						json.dump(data, f, ensure_ascii=False, indent=4)
				except FileNotFoundError:
					print('The file "conversation_history.json" is missing.Make sure all files are located within the same folder')

			def clear(self):
				"""
				Clears the conversation history
				"""
				# Reset the contents of the file
				with open("conversation_history.json", "w") as file:
					json.dump({"conversation": []}, file)
				return 'Ok, I have cleared the conversation history'
						
			def exit_and_clear(self):
				"""
				Cleans up by clearing the bot's conversation history 
				A response is then verbalized and the program is ended
				"""
				# Clear the conversation history	
				with open("conversation_history.json", "w") as file:
					json.dump({"conversation": []}, file)

				# verbalize a response before exiting the program
				self.speech_verbalizer.verbalize_speech(speech='Exiting. Goodbye!')
				sys.exit()
