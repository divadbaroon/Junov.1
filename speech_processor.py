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
import azure.cognitiveservices.speech as speechsdk
from speech_verbalizer import SpeechVerbalizer
import threading

class SpeechProcessor:
	"""
	This class is composed of two classes: SpeechIntent and CommandParser.
	The SpeechIntent class retrieves the similarity rankings between the user's speech and the trained luis model.
	The CommandParser class provides the most apporiate response and action to the user's speech given the similarity rankings.
 
	Attributes:
	speech_intent (SpeechIntent): An object that retrieves the similarity rankings between the user's speech and the trained luis model
	command_parser (CommandParser): An object that provides the most apporiate response and action to the user's speech given the similarity rankings
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	"""
	def __init__(self):
		self.speech_intent = SpeechIntent()
		self.command_parser = CommandParser()
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
	
	def process_speech(self, speech:str, persona:str, gender:str, language:str): 
		"""
		Processes the user's input using Azure's LUIS Service and produces an appropriate response and action.
		"""
		# retrieves the similarity rankings between the user's speech and the trained luis model
		similarity_rankings = self.speech_intent.get_user_intent(speech)
		# provides the most apporiate response and action to the user's speech given the similarity rankings
		response = self.command_parser.parse_commands(similarity_rankings, speech, persona, gender, language)
		return response

class SpeechIntent:
	"""
	A class that retrieves the similarity rankings between the user's speech and the trained luis model.
 
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
		# check if request was not successful
		if response.status_code != 200:
			raise ValueError(f"The request sent to the LUIS model was unsuccessful. Error: {response.status_code}")
		# returned json file of the similarity rankings between the user's speech and the trained luis model
		similarity_rankings = response.json()
  
		return similarity_rankings

class CommandParser:
	"""
	A class that provides the most apporiate response and action to the user's speech given the similarity rankings.
	"""

	def parse_commands(self, intents_json, speech, persona, gender, language):
		"""
		Provides the most apporiate response and action to the user's speech given the similarity rankings.
  		"""
	
		top_intent = intents_json["prediction"]["topIntent"] 
		top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]
	
		# if score does not meet minimum threshold a response is instead created using chatGPT
		if top_intent_score < .70:
			conversation_history = self.ConversationHistoryManager().load_conversation_history()
			response = self.ChatGPT().ask_chatgpt(speech, persona, conversation_history) 
   
		# find intent with the highest similarity score
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
			response = self.WebSearcher().search_google(search_request, persona, gender, language)
   
		elif top_intent == 'Open_Website':
			website = intents_json["prediction"]["entities"]["open_website"][0]
			response = self.WebSearcher().open_website(website, persona, gender, language)
   
		elif top_intent == 'Search_Youtube':
			search_request = intents_json["prediction"]["entities"]["search_youtube"][0]
			response = self.WebSearcher().search_youtube(search_request, persona, gender, language)

		elif top_intent == 'Generate_Password':
			response = self.PasswordGenerator().generate_password()
		elif top_intent == 'Mute':
			response = self.BotBehavior().toggle_mute()
		elif top_intent == 'Unmute':
			response = self.BotBehavior().untoggle_mute()
		elif top_intent == 'Pause':
			response = self.BotBehavior().pause(persona, gender, language)
		elif top_intent == 'Get_Conversation_History':
			response = self.ConversationHistoryManager().get_conversation_history(persona)
		elif top_intent == 'Clear':
			response = self.ConversationHistoryManager().clear()
		elif top_intent == 'Quit':
			response = self.ConversationHistoryManager().exit_and_clear(persona, gender, language)
		else:
			response = "Sorry, I don't understand that command. Please try asking again."
		
		# saving new conversation history to conversation_history.json
		self.ConversationHistoryManager().save_conversation_history(speech, response, persona)
   
		return response

	class ChatGPT:
		"""
		A class that creates a response using OpenAI's chatGPT.
	 
		Atributes:
		language_model (str): language model used for chatGPT
		response_length (int): max response length of chatGPT's responses
		openai.api_key (str): subscription key for OpenAi's chatGPT
		"""
		
		def __init__(self):
			self.language_model = "text-ada-001"
			self.response_length = 100
			openai.api_key = config.retrieve_secret('OpenAI-API')

		def ask_chatgpt(self, speech, persona, conversation_history=None):
			"""
			Creates a response using OpenAI's chatGPT.
			"""

			formatted_conversation_history = ""
		
			if conversation_history:
				for conversation in conversation_history:
					formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
					formatted_conversation_history += f"Response: \n{persona}: {conversation[persona]}\n\n"

			# creates prompt used for chatgpt
			if persona != 'bot' and formatted_conversation_history:
				prompt = (f"Provide the next response to the user given this conversation history {formatted_conversation_history}. I want you to respond to the user like you are {persona}: The user said: {speech}")
			elif persona == 'bot' and formatted_conversation_history:
				prompt = (f"Provide the next response to the user given this conversation history {formatted_conversation_history}. Provide a realistic chatbot like response to the user: The user said: {speech}")
			elif persona != 'bot' and not formatted_conversation_history:
				prompt = (f"I want you to respond to the user like you are {persona}. The user said: {speech}")
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
	
			response = response.replace('\n\n', ' ').replace(f'{persona}:', '').replace('Response:', '').lstrip()
			
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

			# language sometimes ends in a question mark
			if language.endswith('?'):
				language = language.rstrip('?')

			# get language code from langauge
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
			
			# the location sometimes ends in a question mark
			if location.endswith('?'):
				location = location.rstrip('?')
		
			# attempt to send request to openweathermap api
			try:
				response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_key}")
			except Exception as e:
				print(f"An error occurred while trying to send a request to openweathermap. Error: {e}")
				response = "Sorry, an error has occured. Please try asking again."
				return response

			# check whether request was successful
			if response.status_code != 200:
				print(f"An error occurred while trying to send a request to openweathermap. Error: {response.status_code}")
				response = "Sorry, an error has occured. Please try asking again."
				return response
			# returned json file with weather data
			data = response.json()

			temperature = data["main"]["temp"]

			# convert temperature from kelvin to fahrenheit
			temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32

			response = f"The weather in {location} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
			
			return response

	class WebSearcher:
		"""
		A class that opens a website or performs a google search.
		speech_verbalizer: an object of the SpeechVerbalizer class
		"""
  
		def __init__(self):
			self.speech_verbalizer = SpeechVerbalizer()
			
		def open_website(self, website: str, persona, gender, language):
			"""
			Opens a user requested website
			:param website: (str) the website to open
			"""
			# running both events simultaneously 
			# to avoid the speech verbalization from lagging behind
			def open_website():
				t1 = threading.Thread(target=self.speech_verbalizer.verbalize_speech, args=(f"Opening {website}", persona, gender, language))
				t2 = threading.Thread(target=webbrowser.open, args=(f"https://www.{website}.com",))
		
	
				t1.start()
				t2.start()

				t1.join()
				t2.join()
	
			# begin both threads
			threading.Thread(target=open_website).start()
			return

		def search_google(self, search_request: str, persona, gender, language):
			"""
			Performs a google search for the given query
			:param search_request: (str) the google search request
			"""
			# running both events simultaneously 
			# to avoid the speech verbalization from lagging behind
			def perform_search():
				t1 = threading.Thread(target=self.speech_verbalizer.verbalize_speech, args=(f"Searching google for {search_request}", persona, gender, language))
				t2 = threading.Thread(target=webbrowser.open, args=(f"https://www.google.com/search?q={search_request}",))
		
	
				t1.start()
				t2.start()

				t1.join()
				t2.join()

			# begin both threads
			threading.Thread(target=perform_search).start()
			return
		
		def search_youtube(self, search_request: str, persona, gender, language):
			"""
			Performs a youtube search for the given query
			:param search_request: (str) the youtube search request
			"""
			# encode the search request
			query = urllib.parse.quote(search_request)
			# running both events simultaneously 
			# to avoid the speech verbalization from lagging behind
			def perform_search():
				t1 = threading.Thread(target=self.speech_verbalizer.verbalize_speech, args=(f'Searching youtube for {search_request}', persona, gender, language))
				t2 = threading.Thread(target=webbrowser.open, args=(f'https://www.youtube.com/results?search_query={query}',))
		
	
				t1.start()
				t2.start()

				t1.join()
				t2.join()
	
				# begin both threads
			# call perform_search with search_request as an argument
			threading.Thread(target=perform_search, args=(search_request,)).start()
			return

	class PasswordGenerator:
		"""
		A class that generates a random password.
		"""
		
		def generate_password(self, length=12):
			"""
			Generates a random password of a given length
			:param length: (int) the length of the password
			"""
			password = ''
			# generate random password
			for _ in range(length):
				password += choice(string.ascii_letters + string.digits + string.punctuation)
			# copy password
			pyperclip.copy(password)
			return 'a random password has been copied to your clipboard'

	class BotBehavior:
		"""
		A class that contains methods that change the behavior of the bot.
	
		Atributes:
		speech_verbalizer: an object of the SpeechVerbalizer class
		"""
		
		def __init__(self):
			self.speech_verbalizer = SpeechVerbalizer()
		
		def toggle_mute(self):
			"""
			Mutes the bot
			"""
			self.speech_verbalizer.mute()
			return 'I am now muted'
	
		def untoggle_mute(self):
			"""
			Unmutes the bot
			"""
			self.speech_verbalizer.unmute()
			return 'I am now unmuted'

		def pause(self, persona, gender, language):
			"""
			Pauses the bot
			The user must press the spacebar to unpause the bot
			"""
			self.speech_verbalizer.verbalize_speech(speech='I am now paused', persona=persona, gender=gender, language=language)
			user_input = ''
			while user_input != ' ':
				user_input = input('Press spacebar to unpause: ')
			return 'I am now unpaused'

	class ConversationHistoryManager:
		"""
		A class that manages the conversation history in the file "conversation_history.json".
	
		Atributes:
		speech_verbalizer: an object of the SpeechVerbalizer class
		"""
		
		def __init__(self):
			self.speech_verbalizer = SpeechVerbalizer()

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

		def get_conversation_history(self, persona):
			"""
			Gets the conversation history from the conversation_history.json file
			"""
			# load conversation history from conversation_history.json file
			conversation_history = self.load_conversation_history()
			formatted_conversation_history = ""
		
			if conversation_history:
				for conversation in conversation_history:
					formatted_conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
					formatted_conversation_history += f"Response: \n{persona}: {conversation[persona]}\n\n"

			print(f'\nConversation History: \n{formatted_conversation_history}')
			return 'Ok, I have printed the conversation history to the console'

		def log_conversation(self, speech: str):
			"""
			Logs the conversation to the conversation_history.json file
			"""
			data = {"conversation": speech}
			try:
				with open("conversation_history.json", "w", encoding="utf-8") as f:
					json.dump(data, f, ensure_ascii=False, indent=4)
			except FileNotFoundError:
				print('The file "conversation_history.json" is missing. Make sure all files are located within the same folder')
			return 'Sorry about that, I will take note of that'
			
		def save_conversation_history(self, speech: str, response: str, persona: str):
			"""
			Loads conversation history from json file
			:return: (list) conversation history
			"""
			conversation_history = self.load_conversation_history()
		
			new_conversation = {
			"User": speech,
			persona: response
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
					
		def exit_and_clear(self, persona, gender, language):
			"""
			Cleans up by clearing the bot's conversation history 
			A response is then verbalized and the program is ended
			"""
			# Reset the contents of the file	
			with open("conversation_history.json", "w") as file:
				json.dump({"conversation": []}, file)

			# verbalize a response before exiting the program
			self.speech_verbalizer.verbalize_speech(speech='Exiting. Goodbye!', persona=persona, gender=gender, language=language)
			sys.exit()
