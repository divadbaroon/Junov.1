import requests
import uuid

from settings.settings_orchestrator import SettingsOrchestrator

class TranslateSpeech:
	"""
	A class that translates user given speech to a desired language.
		
	Atributes:
	region (str): region for Azure's Translator service
	translator_key (str): subscription key for Azure's Translator service
	bot_properties (BotProperties): BotProperties object
	"""
			
	def __init__(self, translator_key):
		self.region = 'eastus'
		self.translator_key = translator_key
		self.bot_settings = SettingsOrchestrator()
		self.endpoint = "https://api.cognitive.microsofttranslator.com/trasnlate"
			
	def translate_speech(self, speech_to_translate:str, language_from:str, language_to:str, one_shot_translation:bool=False):
		"""
		Translates a given string of text to a desired langauge.
		:param speech_to_translate: (str) the speech to be translated
		:param language: (str) the language for the speech to be translated into
		:return: (str) the translated speech
		"""
  
		language_to, language_from = self._clean_language(language_to, language_from)
   
		# Get the language codes for the language to be translated from and to
		language_from_code = self.bot_settings.retrieve_language_code(language_from.lower())
		language_to_code = self.bot_settings.retrieve_language_code(language_to.lower())
  
		# If the language is not supported, return an error message
		if language_from_code is None:
			return f'Sorry, {language_from} is not currently supported. Try asking again.'

		if language_to_code is None:
			return f'Sorry, {language_to} is not currently supported. Try asking again.'
  
		# prepare a request to Azure's Translator service
		params = {
			'api-version': '3.0',
			'from': language_from_code,
			'to': language_to_code
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
			request = requests.post(self.endpoint, params=params, headers=headers, json=body)
			response = request.json()

			# get the translated speech
			response = response[0]['translations'][0]['text']
		except Exception as e:
			print(f"An exception occurred: {type(e).__name__}")
			response = f'Sorry, there was an error while trying to translate: {speech_to_translate}. Try asking again.'
   
		if one_shot_translation:
			return {'action': 'one_shot_translation', 'new_language': language_to, 'original': speech_to_translate, 'response': response}
		else:
			return {'action': 'translation', 'new_language': language_to, 'original': speech_to_translate, 'response': response}

	def _clean_language(self, language_to:str, language_from:str):
		# Language sometimes ends in a question mark
		if language_to.endswith('?'):
			language_to = language_to.rstrip('?')

		elif language_from.endswith('?'):
			language_from = language_from.rstrip('?')

		return language_to, language_from