import config 
import openai 
import requests
import webbrowser 
import json
from speech_verbalizer import SpeechVerbalizer
import uuid
import azure.cognitiveservices.speech as speechsdk
import urllib

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
		self.language_model = "text-davinci-002"
		self.response_length = 100
		self.region = 'eastus'
		openai.api_key = config.retrieve_secret('OpenAI-API')
		self.weather_key = config.retrieve_secret('Weather-API')
		self.luis_app_id = config.retrieve_secret('Luis-APP-ID')
		self.luis_key = config.retrieve_secret('Luis-API')
		self.translator_key = config.retrieve_secret('PiBot-Translator-API')
		self.speech_verbalizer  = SpeechVerbalizer()
		self.speech_config = speechsdk.SpeechConfig(subscription = config.retrieve_secret('PiBot-API'), region = 'eastus')
	
	def process_speech(self, speech: str, persona: str) -> str: 
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
		if top_intent_score < .5:
			response = self.ask_chatgpt(speech, persona) 
		# now checking for intent with the highest similarity score
		elif top_intent == 'Translate_Speech':
			response = self.translate_speech(speech)
		elif top_intent == 'Get_Weather':
			response = self.get_weather(speech)
		elif top_intent == 'Mute_Bot':
			response = self.toggle_mute()
		elif top_intent == 'Unmute_Bot':
			response = self.untoggle_mute()
		elif top_intent == 'Search_Google':
			response = self.search_google(speech)
		elif top_intent == 'Open_Website':
			response = self.open_website(speech)
		elif top_intent == 'Search_Youtube':
			response = self.search_youtube(speech)
		elif top_intent == 'Quit':
			response = 'Exiting the program, goodbye...'
		else:
			response = "Sorry, I don't understand that command. Please try asking again."
   
		return response

	def ask_chatgpt(self, speech: str, persona: str):
		"""
		Sends a request to chatgpt using users speech
		:param speech: (str) speech input
		:return: (str) chatgpt response
  		"""
    
		try:
			with open('bot_conversation.json', 'r') as f:  
				data = json.load(f)
				conversations = data["conversation"]
		except FileNotFoundError:
			print('The file "bot_conversation.json" is missing.\nMake sure all files are located within the same folder')

		# creates prompt used for chatgpt
		if persona != 'bot' and conversations:
			prompt = (f"Respond to me like you are {persona} talking to me in person. Given this conversation history {conversations}: {speech}\n")
		elif persona != 'bot' and not conversations:
			prompt = (f"Respond to me like you are {persona} talking to me in person: {speech}\n")
		elif persona == 'bot' and conversations:
			prompt = (f"Give me a response given this conversation history {conversations}: {speech}\n")
		else:
			prompt = speech

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

		new_conversation = f'I said: {speech} + {persona} said: {response}'
		data["conversation"] = new_conversation
		print(data)
		try:
			with open("bot_conversation.json", "w") as f:
				json.dump(data, f)
		except FileNotFoundError:
			print('The file "bot_conversation.json" is missing.\nMake sure all files are located within the same folder')
		
		# occasionally the response ends in an incomplete sentence
		# thus any extra words after the last period are removed
		return response.rsplit('.', 1)[0] + '.'
	
	def get_weather(self, speech: str  ):
		"""
		Returns weather information for a particular location
		:param speech: (str) speech input
		:return: (str) weather information
  		"""
		# clean up user input
		locaton = speech.split("in ")[-1].replace('?', '').strip() 

		# attempt to send request to openweathermap api
		try:
			response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={locaton}&appid={self.weather_key}")
		except Exception as e:
			print(f"An error occurred while trying to send a request to openweathermap. Error: {e}")
			response = "Sorry, an error has occured. Please try asking again."
			return response

		# check whether request was successful
		if response.status_code != 200:
			raise ValueError(f"The request sent to the chatGPT was unsuccessful. Error: {response.status_code}")
		# returned json file with weather data
		data = response.json()

		temperature = data["main"]["temp"]

		# convert temperature from kelvin to fahrenheit
		temperature_celsius = temperature - 273.15
		temperature_fahrenheit = temperature_celsius * 9/5 + 32

		response = f"The weather in {locaton} is {round(temperature_fahrenheit)} degrees Fahrenheit"		
		
		return response

	def translate_speech(self, speech: str): 
		"""
		Translates a given string of text to a desired langauge
		:param speech: (str) speech input
		:return: (str) speech translation
  		"""
		endpoint = "https://api.cognitive.microsofttranslator.com/"
		path = '/translate'
		constructed_url = f'{endpoint}{path}'

		# retrieve desired language from user input
		language = speech.split('into')[-1].replace('?', '').strip()
  
		try:
			with open('bot_gender_and_languages.json', 'r') as f:  
				languages = json.load(f)
		except FileNotFoundError:
			print('The file "gender_and_languages.json" is missing.\nMake sure all files are located within the same folder')

		# get language code
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

		# clean up user input
		speech = speech.split('translate')[1].split('into')[0].strip()
		body = [{"text": speech}]
  
		try:
			request = requests.post(constructed_url, params=params, headers=headers, json=body)
			response = request.json()
			response = response[0]['translations'][0]['text']
		except Exception as e:
			print(f"An error occurred while sending a request to microsoft translator. Error: {e}")
			response = f'Sorry, there was an error while trying translate {speech}. Try asking again.'
  
		return response
  
	def open_website(self, speech: str):
		"""
		Opens a user requested website
		:param query: (str) the search query
  		"""
		# clean up user input
		website = speech.split('open')[1].replace('.com', '').strip()

		# attempt to open website
		try:
			webbrowser.open(f"https://www.{website}.com") 
			response = f"Opening {website}"
		except Exception as e:
			print(f'Could not open {website}. Error {e}')
			response = f'Sorry, there was an error while trying to open {website}'
		
		return response

	def search_google(self, speech: str):
		"""
		Performs a google search for the given query
		:param query: (str) the search query
		"""
		if speech.startswith('google'):
			search_request = speech.replace("google", '')
		elif speech.startswith('search'):
			search_request = speech.replace("search", '')
		elif speech.startswith('look up'):
			search_request = speech.replace("look up", '')

		# clean up input
		search_request = search_request.replace(".", '').strip() 

		try:
			# attempt to open the google search page with the query
			webbrowser.open(f"https://www.google.com/search?q={search_request}")
			response = "Searching " + search_request
		except Exception as e:
			print(f'Could not complete search for {search_request}. Error: {e}')
			response = 'Sorry, there was an error while trying to complete the search'
	
		return response
	
	def search_youtube(self, speech):
		"""
		Performs a youtube search for the given query
		:param query: (str) the search query
		"""
		# clean up input
		search_request = speech.split('youtube')[1].strip()
		query = urllib.parse.quote(search_request)
		webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
		return(f'Searching youtube for {search_request}')
	
	def toggle_mute(self):
		"""
		Mutes the bot
		"""
		self.speech_verbalizer.mute()
		return('I am now muted.')

	def untoggle_mute(self):
		"""
		Unmutes the bot
		"""
		self.speech_verbalizer.unmute()
		return('I am now unmuted.')