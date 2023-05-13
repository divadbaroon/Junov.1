
import requests
import uuid

import sys
import os

# Get the current script's directory and its parent directory
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
grandparent_directory = os.path.dirname(parent_directory)
greatgrandparent_directory = os.path.dirname(grandparent_directory)

# Add the parent directory to sys.path
if greatgrandparent_directory not in sys.path:
    sys.path.append(greatgrandparent_directory)

from configuration.general_settings.bot_properties import BotProperties

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
		self.bot_properties = BotProperties()
			
	def translate_speech(self, speech_to_translate:str, language_from:str, language_to:str, translator_key:str, one_shot_translation:bool=False):
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
		if language_to.endswith('?'):
			language_to = language_to.rstrip('?')
		elif language_from.endswith('?'):
			language_from = language_from.rstrip('?')
   
		# Extract languages and their codes from bot_properties.json
		language_codes = self.bot_properties.retrieve_property('language_codes')
		# Get the language code for the desired language
		for language_name, code in language_codes.items():
			if language_to.lower() == language_name:
				language_to_code = code
			elif language_from.lower() == language_name:
				language_from_code = code
			else:
				response = f'Sorry, {language_to} is not a supported language. Please try asking again.'
  
		# prepare a request to Azure's Translator service
		params = {
			'api-version': '3.0',
			'from': language_from_code,
			'to': language_to_code
		}

		headers = {
			'Ocp-Apim-Subscription-Key': translator_key,
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
			print(f"An exception occurred: {type(e).__name__}")
			print(f"Error message: {str(e)}")
			print(f"Line number: {sys.exc_info()[-1].tb_lineno}")
			response = f'Sorry, there was an error while trying to translate: {speech_to_translate}. Try asking again.'
   
		if one_shot_translation:
			return {'one_shot_translation': language_to, 'original': speech_to_translate, 'response': response}
		else:
			return {'new_language': language_to, 'original': speech_to_translate, 'response': response}