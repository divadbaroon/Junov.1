import requests
import uuid

class TranslateSpeech:
	"""
	A class that translates user given speech to a desired language.
		
	Atributes:
	region (str): region for Azure's Translator service
	translator_key (str): subscription key for Azure's Translator service
	bot_properties (BotProperties): BotProperties object
	"""
			
	def __init__(self, translator_key, bot_settings:object):
		self.region = 'eastus'
		self.translator_key = translator_key
		self.bot_settings = bot_settings
		self.endpoint = "https://api.cognitive.microsofttranslator.com/translate"
			
	def translate_speech(self, speech_to_translate:str, current_language:str, new_language:str, one_shot_translation:bool=False):
		"""
		Translates a given string of text to a desired langauge.
		:param speech_to_translate: (str) the speech to be translated
		:param language: (str) the language for the speech to be translated into
		:return: (str) the translated speech
		"""
  
		if speech_to_translate == 'Exiting. Goodbye!':
			self.bot_settings.save_bot_property('exit_status', True)
   
		if one_shot_translation:
			self.bot_settings.save_bot_property('reset_language', True)

		# Clean the language input for any punctuation
		current_language, new_language = self._clean_language(current_language, new_language)
   
		# Get the language codes for the current and new languages
		current_language_code = self.bot_settings.retrieve_language_code(current_language.lower())
		new_language_code = self.bot_settings.retrieve_language_code(new_language.lower())
  
		# If the language is not supported, return an error message
		if current_language_code is None:
			return f'Sorry, {current_language} is not currently supported. Try asking again.'

		if new_language_code is None:
			return f'Sorry, {new_language} is not currently supported. Try asking again.'

		# Get the translated speech from Azure's Translator service
		response = self._send_request(current_language_code, new_language_code, speech_to_translate)
   
		return response

	def _clean_language(self, current_language:str, new_language:str):
		# Language sometimes ends in a question mark
		if current_language.endswith('?'):
			current_language = current_language.rstrip('?')

		elif new_language.endswith('?'):
			new_language = new_language.rstrip('?')

		return current_language, new_language

	def _send_request(self, current_language_code, new_language_code, speech_to_translate):
		"""Send a request to Azure's Translator service to translate a given string of text to a desired language."""
  
		# prepare a request to Azure's Translator service
		params = {
			'api-version': '3.0',
			'from': current_language_code,
			'to': new_language_code
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
   
		return response

