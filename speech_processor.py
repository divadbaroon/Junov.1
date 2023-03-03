import config 
import openai 
import requests
import json
import uuid
import webbrowser
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
	The nested SpeechIntent class retrieves the similarity rankings between the user's speech and the trained luis model in json format.
	The nested CommandParser class uses the data from the similarity rankings to provide the most apporiate response 
 	and action to the user's speech.
	The nested CommandParser class is composed of seven nested classes, each containing methods dedicated to executing
	commands that are specific to the user's intent.
	These clases nested under CommandParser include: AskGPT, TranslateSpeech, GetWeather, WebSearcher, PasswordGenerator,
	BotBehavior, and ConversationHistoryManager
	"""

	def process_speech(self, speech:str): 
		"""
		Processes the user's input using a trained LUIS model and produces an appropriate response and action.
		:param speech: (str) speech input
		:return: (str) response to users speech and appropriate action to be taken
		"""
  
		# Retrieves a json file containing similarity rankings between the user's speech and the trained luis model
		intents_json = self.SpeechIntent().get_user_intent(speech)
		# Provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.CommandParser().parse_commands(speech, intents_json)
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
			Retrieves the similarity rankings between the user's speech and the trained LUIS model.
			:param speech: (str) speech input
			:return: (str) json file containing similarity rankings between the user's speech and the trained luis model
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
		If the top intent's score is less than 70% a response is instead created using GPT-3.
		If the top intent's score is greater than 70% the associated entity is retrieved and the appropriate action is executed.
		"""

		def parse_commands(self, speech:str, intents_json:dict):
			"""
			Provides the most apporiate response and action to the user's speech given the similarity rankings.
			:param speech: (str) speech input
			:param intents_json: (str) json file containing similarity rankings between the user's speech and the trained luis model
			:return: (str) response to users speech and appropriate action to be taken
			"""
   
			# Extract top intent and top intent's score from intents_json
			top_intent = intents_json["prediction"]["topIntent"] 
			top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]
		
			# If score does not meet minimum threshold a response is instead created using GPT-3
			if top_intent_score < .70:
				# Loading conversation history to be used as context for GPT-3
				conversation_history = self.ConversationHistoryManager().load_conversation_history()
				response = self.AskGPT().ask_GPT(speech, conversation_history) 
	
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
	
			elif top_intent == 'Create_Image':
				image = intents_json["prediction"]["entities"]["image_to_create"][0]
				response = self.AskGPT().create_gpt_image(image)

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
			
			# Saving the newly created conversation to conversation_history.json 
			self.ConversationHistoryManager().save_conversation_history(speech, response)
	
			return response

		class AskGPT:
			"""
			A class that creates a response using OpenAI's GPT-3 API.
			A personalize response is created depening on the user's specified persona and
			the past conversation history to provie context to the conversation.
		
			Atributes:
			language_model (str): language model used for GPT-3 
			response_length (int): max response length of GPT-3's responses
			openai.api_key (str): subscription key for OpenAi's GPT-3
			persona (str): the bot's persona
			"""
			
			def __init__(self):
				self.language_model = "gpt-3.5-turbo"
				self.response_length = 100
				openai.api_key = config.retrieve_secret('OpenAI-API')
				self.persona = BotProperties().retrieve_property('persona')
				self.user_name = BotProperties().retrieve_property('user_name')
				self.verbalize_speech = SpeechVerbalizer()

			def ask_GPT(self, speech:str, conversation_history:list):
				"""
				Uses the user's speech, the bot's persona, and the conversation history 
				to create a response using OpenAI's GPT-3.5-turbo model API.
				:param speech: (str) speech input
				:param conversation_history: (list) the conversation history between the user and the bot
				"""
	
				formatted_conversation_history = ""
			
				# Formats conversation history to be used as prompt for GPT-3.5-turbo model 
				if conversation_history:
					for conversation in conversation_history:
						formatted_conversation_history += f"User said: {conversation['User']}\n"
						for name, text in conversation.items():
							if name != 'User':
								formatted_conversation_history += f"{name.title()} said: {text}\n"
	
				# Creates a prompt used for GPT-3.5-turbo model based on the user's persona and conversation history
				if self.persona != 'chatbot' and formatted_conversation_history:
					prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nI want you to provide the next response to the user. Respond like you are {self.persona}: The user said: {speech}. Keep it concise")
				elif self.persona == 'chatbot' and formatted_conversation_history:
					prompt = (f"\nProvide your response given this conversation history: \n{formatted_conversation_history}\nProvide a chatbot like response to the next user input and do not provide 'chatbot response' in the response: The user said: {speech}. Keep it concise")
				elif self.persona != 'chatbot' and not formatted_conversation_history:
					prompt = (f"\nI want you to respond to the user like you are {self.persona}. The user said: {speech}. Keep it concise")
				else:
					prompt = (f"\nProvide a chatbot like response to the user: The user said: {speech}. Keep it concise")
				
				# url to OpenAI's GPT-3 API
				url = "https://api.openai.com/v1/chat/completions"
	
				# Now using the GPT-3.5-turbo model
				payload = {
					"model": "gpt-3.5-turbo",
					"messages": [{"role": "assistant", "content": prompt}]
				}
				headers = {
					"Content-Type": "application/json",
					"Authorization": f"Bearer {config.retrieve_secret('OpenAI-API')}"
				}

				# Send the POST request to OpenAI's GPT-3 API
				request = requests.post(url, headers=headers, data=json.dumps(payload))
				if request.status_code == 200:
					content = request.json()
				else:
					# If the request fails, return a message to the user
					return "Sorry, I am currently experiencing technical difficulties. Please try again later."

				# Extract the 'content' value from the response
				# This is the response from the GPT-3.5-turbo model
				response = content['choices'][0]['message']['content']
	
				# clean up some errors chatgpt produces in its output
				response = response.replace(f'{self.persona} said:', ' ').replace(f'{self.persona}:', ' ').replace(f'response', ' ').strip()
	
				return response

			def create_gpt_image(self, image: str):
				"""
				Creates an image using OpenAI's GPT-3 API.
				"""
	
				# url to OpenAI's GPT-3 API
				url = "https://api.openai.com/v1/images/generations"
	
				# Now using the GPT-3.5-turbo model
				payload = {
					"prompt": image,
					"n": 1,
				}
				headers = {
					"Content-Type": "application/json",
					"Authorization": f"Bearer {config.retrieve_secret('OpenAI-API')}"
				}

				# Send the POST request to OpenAI's GPT-3 API
				response = requests.post(url, headers=headers, data=json.dumps(payload))
				
				if response.status_code == 200:
					response_json = json.loads(response.content)

					url = response_json['data'][0]['url']
					webbrowser.open(url)
					return f"Ok, I have created an image of {image}."
				else:
					# If the request fails, return a message to the user
					return "Sorry, I am currently experiencing technical difficulties. Please try again later."
		
		class TranslateSpeech:
			"""
			A class that translates user given speech to a desired language.
		
			Atributes:
			region (str): region for Azure's Translator service
			translator_key (str): subscription key for Azure's Translator service
			bot_properties (BotProperties): BotProperties object
			"""
			
			def __init__(self):
				self.region = 'eastus'
				self.translator_key = config.retrieve_secret('PiBot-Translator-API')
				self.bot_properties = BotProperties()
			
			def translate_speech(self, speech_to_translate:str, language:str):
				"""
				Translates a given string of text to a desired langauge.
				:param speech_to_translate: (str) the speech to be translated
				:param language: (str) the language for the speech to be translated into
				:return: (str) the translated speech
				"""
	
				endpoint = "https://api.cognitive.microsofttranslator.com/"
				path = '/translate'
				constructed_url = f'{endpoint}{path}'

				# Language sometimes ends in a question mark
				if language.endswith('?'):
					language = language.rstrip('?')

				# Extract languages and their codes from bot_properties.json
				language_codes = self.bot_properties.retrievet_property('language_codes')
				# Get the language code for the desired language
				for language_name, code in language_codes.items():
					if language.lower() == language_name:
						language_code = code
						break
  
				# prepare a request to Azure's Translator service
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

				# attempt to send a request to Azure's Translator service
				try:
					request = requests.post(constructed_url, params=params, headers=headers, json=body)
					response = request.json()
					# get the translated speech
					response = response[0]['translations'][0]['text']
				except Exception as e:
					print(f"An error occurred while sending a request to Azure. Error: {e}")
					response = f'Sorry, there was an error while trying to translate: {speech_to_translate}. Try asking again.'

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
				:param location: (str) the location to get the weather for
				:return: (str) the weather for the given location
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
				if response.status_code == 200:
		
					# Returned json file with weather data
					data = response.json()

					temperature = data["main"]["temp"]

					# Convert temperature from kelvin to fahrenheit
					temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32

					response = f"The weather in {location} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
				else:
		
					print(f"An error occurred while trying to send a request to openweathermap. Error: {response.status_code}")
					response = "Sorry, an error has occured. Please try asking again."
				
				return response

		class WebSearcher:
			"""
			A class that contains methods for opening a desired website, 
			performing a google search, and performing a youtube search.
			"""
				
			def open_website(self, website: str):
				"""
				Opens the specified website in a new browser window.
				:param website: (str) the website to open
				"""
				webbrowser.open(f"https://www.{website}.com")
		
				return f'Opening {website}.com'

			def search_google(self, search_request: str):
				"""
				Performs a google search for a given query
				:param search_request: (str) the google search request
				"""
				webbrowser.open(f"https://www.google.com/search?q={search_request}")
				
				return f'Searching google for {search_request}'
			
			def search_youtube(self, search_request: str):
				"""
				Performs a youtube search for a given query
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
			
			def generate_password(self, length: int = 16):
				"""
				Generates a random password of the specified length and copies it to the users clipboard.
				:param length: (int) the length of the password
				:return: (str) a message that a password has been generated and copied to the clipboard
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
			A class that contains methods to change the behavior of the chatbot.
		
			Atributes:
			speech_verbalizer: an object of the SpeechVerbalizer class
			bot_properties: an object of the BotProperties class
			"""
			
			def __init__(self):
				"""
				Initializes an object of BotBehavior class.
	   			"""
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
				:param new_persona: (str) the new persona to change to
				"""

				self.bot_properties.save_property('persona', new_persona)
				return f'Ok, I have changed my persona to {new_persona}.'

			def change_gender(self, new_gender:str):
				"""
				Changes the bot's gender
				:param new_gender: (str) the new gender to change to
				"""
				if new_gender in ['male', 'female']:
					self.bot_properties.save_property('gender', new_gender)
					return f'Ok, I have changed my gender to {new_gender}.'
				else:
					return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
			
			def change_language(self, new_language:str):
				"""
				Changes the bot's language
				:param new_language: (str) the new language to change to
				"""
				# Extracting all currently supported languages
				langauges = self.bot_properties.retrieve_property('languages')
				# Check if language is supported
				if new_language.lower() in langauges:
					self.bot_properties.save_property('language', new_language)
					return f'Ok, I have changed my language to {new_language}.'
				else:
					return f'Sorry, {new_language} is not currently supported.'

		class ConversationHistoryManager:
			"""
			A class that manages the conversation history in the file "conversation_history.json".
		
			Atributes:
			speech_verbalizer: an object of the SpeechVerbalizer class
			"""
			
			def __init__(self):
				"""
				Initializes a new ConversationHistoryManager object.
				"""
				self.speech_verbalizer = SpeechVerbalizer()
				self.persona = BotProperties().retrieve_property('persona')

			def load_conversation_history(self):
				"""
				Loads the conversation history from the conversation_history.json file
				:return: (list) the conversation history
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
				and prints it to the console
				:return: (str) the conversation history
				"""
				# load conversation history from conversation_history.json file
				conversation_history = self.load_conversation_history()
				formatted_conversation_history = ""

				# Reformat conversation history to make it more readable
				if conversation_history:
					for conversation in conversation_history:
						formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
						formatted_conversation_history += f"Response: \n{self.persona}: {conversation[self.persona]}\n\n"

				print(f'\nConversation History: \n{formatted_conversation_history}')
				return 'Ok, I have printed the conversation history to the console'
				
			def save_conversation_history(self, speech: str, response: str):
				"""
				Saves the new conversation along with the rest of the conversation
				history to conversation_history.json file
				:param speech: (str) the user's speech
				:param response: (str) the bot's response
				"""
				# load conversation history from conversation_history.json file
				conversation_history = self.load_conversation_history()

				# Add new conversation to the conversation history
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
				# Reset the contents of conversation_history.json
				with open("conversation_history.json", "w") as file:
					json.dump({"conversation": []}, file)
				return 'Ok, I have cleared the conversation history'
						
			def exit_and_clear(self):
				"""
				Cleans up by clearing the bot's conversation history. 
				A response is then verbalized and the program is ended
				"""
				# Reset the contents of conversation_history.json	
				with open("conversation_history.json", "w") as file:
					json.dump({"conversation": []}, file)

				# verbalize a response before exiting the program
				self.speech_verbalizer.verbalize_speech(speech='Exiting. Goodbye!')
				sys.exit()
