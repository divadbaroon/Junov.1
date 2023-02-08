import config 
import openai 
import requests
import webbrowser 
import json
from speech_verbalizer import SpeechVerbalizer
import uuid
import azure.cognitiveservices.speech as speechsdk
import urllib
import sys

class SpeechProcessor:
	"""
	A class that processes the user's input using Azure's LUIS Service.
	If minimal similarities are found between the user's speech and the trained Azure LUIS model a 
	response is created using OpenAI's chatGPT.
 
	Attributes:
	language_model (str): language model used for chatGPT
	response_length (int): max response length of chatGPT's responses
	region (str): region used for Azure resources
	openai.api_key (str): subscription key for OpenAi's chatGPT
	weather_key (str): subscription key for OpenWeatherMap 
    luis_app_id (str): application id for Azure's LUIS service
	luis_key (str): subscription key for Azure's LUIS service
	translator_key (str): subscription key for Azure's Translator service
	speech_verbalizer (object of SpeechVerbalizer class)
	speech_config (SpeechConfig): A configuration object that takes a subscription key and a region as arguments
	"""
	def __init__(self):
		"""
		Initializes a new SpeechProcessor object
		"""
		self.language_model = "text-davinci-003"
		self.response_length = 100
		self.region = 'eastus'
		openai.api_key = config.retrieve_secret('OpenAI-API')
		self.weather_key = config.retrieve_secret('Weather-API')
		self.luis_app_id = config.retrieve_secret('Luis-APP-ID')
		self.luis_key = config.retrieve_secret('Luis-API')
		self.translator_key = config.retrieve_secret('PiBot-Translator-API')
		self.speech_verbalizer  = SpeechVerbalizer()
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
	
	def process_speech(self, speech: str, persona: str, gender: str, language: str) -> str: 
		"""
		Checks for user's intent by sending a request to LUIS api and checking for similarites between the user's speech
		and the trained langauge model.
		:param speech: (str) speech input
		:param persona: (str) bot persona
		:return: (str) bot's response 
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
		intents_json = response.json()
  
		top_intent = intents_json["prediction"]["topIntent"] 
		top_intent_score = intents_json["prediction"]["intents"][top_intent]["score"]
  
		# if score does not meet minimum threshold a response is instead created using chatGPT
		if top_intent_score < .70:
			response = self.ask_chatgpt(speech, persona) 
   
		# find intent with the highest similarity score
		# and retrieve associated entity if applicable
		elif top_intent == 'Translate_Speech':
			speech_to_translate = intents_json["prediction"]["entities"]["translate_speech"][0]
			language = intents_json["prediction"]["entities"]["language"][0]
			response = self.translate_speech(speech_to_translate, language)
   
		elif top_intent == 'Get_Weather':
			location = intents_json["prediction"]["entities"]["weather_location"][0]
			response = self.get_weather(location)
   
		elif top_intent == 'Search_Google':
			search_request = intents_json["prediction"]["entities"]["search_google"][0]
			response = self.search_google(search_request)
   
		elif top_intent == 'Open_Website':
			website = intents_json["prediction"]["entities"]["open_website"][0]
			response = self.open_website(website)
   
		elif top_intent == 'Search_Youtube':
			search_request = intents_json["prediction"]["entities"]["search_youtube"][0]
			response = self.search_youtube(search_request)

		elif top_intent == 'Mute':
			response = self.toggle_mute(persona, gender, language)
		elif top_intent == 'Unmute':
			response = self.untoggle_mute(persona, gender, language)
		elif top_intent == 'Quit':
			response = self.exit_and_cleanup(persona, gender, language)
		else:
			response = "Sorry, I don't understand that command. Please try asking again."
   
		return response

	def ask_chatgpt(self, speech: str, persona: str):
		"""
		Sends a request to chatgpt using users speech
		:param speech: (str) speech input
		:return: (str) chatgpt response
  		"""
		# get conversation history
		try:
			with open('C:/Users/David/OneDrive/Desktop/PiBot/conversation_history.json', 'r') as f:  
				data = json.load(f)
				conversations = data["conversation"]
		except FileNotFoundError:
			print('The file "conversation_history.json" is missing.\nMake sure all files are located within the same folder')

		conversation_history = ""
	
		if conversations:
			for conversation in conversations:
				conversation_history += f"Input: \nUser: {conversation['User']}\n\n"
				conversation_history += f"Response: \n{persona}: {conversation[persona]}\n\n"

		# creates prompt used for chatgpt
		if persona != 'bot' and conversation_history:
			prompt = (f"Provide the next response to the user given this conversation history {conversation_history}. I want you to respond to the user like you are {persona}: The user said: {speech}")
		elif persona == 'bot' and conversation_history:
			prompt = (f"Provide the next response to the user given this conversation history {conversation_history}. Provide a realistic chatbot like response to the user: The user said: {speech}")
		elif persona != 'bot' and not conversation_history:
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

		new_conversation = {
			"User": speech,
			persona: response
		}
		conversations.append(new_conversation)
		data["conversation"] = conversations
		try:
			with open("conversation_history.json", "w") as f:
				json.dump(data, f, indent=4)
		except FileNotFoundError:
			print('The file "conversation_history.json" is missing.\nMake sure all files are located within the same folder')
		
		return response
	
	def get_weather(self, location: str  ):
		"""
		Returns weather information for a particular location
		:param location: (str) location for weather retrieval
		:return: (str) weather information
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
			raise ValueError(f"The request sent to OpenWeatherMap was unsuccessful. Error: {response.status_code}")
		# returned json file with weather data
		data = response.json()

		temperature = data["main"]["temp"]

		# convert temperature from kelvin to fahrenheit
		temperature_fahrenheit = (temperature - 273.15) * 9/5 + 32

		response = f"The weather in {location} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
		
		return response

	def translate_speech(self, speech_to_translate: str, language: str): 
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
  
	def open_website(self, website: str):
		"""
		Opens a user requested website
		:param website: (str) the website to open
  		"""
		# attempt to open website
		try:
			webbrowser.open(f"https://www.{website}.com") 
			response = f"Opening {website}"
		except Exception as e:
			print(f'Could not open {website}. Error {e}')
			response = f'Sorry, there was an error while trying to open {website}'
		
		return response

	def search_google(self, search_request: str):
		"""
		Performs a google search for the given query
		:param search_request: (str) the google search request
		"""
		try:
			# attempt to open the google search page with the query
			webbrowser.open(f"https://www.google.com/search?q={search_request}")
			response = "Searching google for" + search_request
		except Exception as e:
			print(f'Could not complete search for {search_request}. Error: {e}')
			response = 'Sorry, there was an error while trying to complete the search'
	
		return response
	
	def search_youtube(self, search_request: str):
		"""
		Performs a youtube search for the given query
		:param search_request: (str) the youtube search request
		"""
		query = urllib.parse.quote(search_request)
		webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
		return(f'Searching youtube for {search_request}')
	
	def toggle_mute(self, persona, gender, language):
		"""
		Mutes the bot
		"""
		self.speech_verbalizer.mute()
		self.speech_verbalizer.verbalize_speech(speech='I am now muted', persona=persona, gender=gender, language=language)

	def untoggle_mute(self, persona, gender, language):
		"""
		Unmutes the bot
		"""
		self.speech_verbalizer.unmute()
		self.speech_verbalizer.verbalize_speech(speech='I am now unmuted', persona=persona, gender=gender, language=language)

	def exit_and_cleanup(self, persona, gender, language):
		"""
		Cleans up by clearing the bot's conversation history 
  		A response is then verbalized and the program is ended
		"""
		# Reset the contents of the file	
		with open("conversation_history.json", "w") as file:
			json.dump({"conversation": []}, file)

		# verbalize a response before exiting the program
		self.speech_verbalizer.verbalize_speech(speech='Exiting the program. Goodbye...', persona=persona, gender=gender, language=language)
		sys.exit()
