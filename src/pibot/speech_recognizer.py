
import azure.cognitiveservices.speech as speechsdk
from time import time
import sys

from settings.settings_manager import SettingsOrchestrator
from src.pibot.bot_commands.translate_speech import TranslateSpeech

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_config, speech_recognizer, translator_key):
		self.speech_recognizer = speech_recognizer
		self.speech_config = speech_config
		self.bot_settings = SettingsOrchestrator()
		self.translator = TranslateSpeech()
		self.translator_key = translator_key

	def listen(self):
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""

		# Reload the bot_settings.json file to check if the recognizer needs to be reconfigured 
		# This is needed when a property such as language is changed 
		self.bot_settings.reload_bot_settings()
		reconfigure = self.bot_settings.retrieve_bot_property('reconfigure')

		if reconfigure:
			self._reconfigure_recognizer()

		print("\nListening...")  

		recognition_attempt = 0
		begin_timer = time()
	  
		while True:
			try:
				# A 5-second attempt to recognize the user's speech input
				result = self.speech_recognizer.recognize_once_async().get() 
			except Exception as e:
				print(f"Error occurred during speech recognition: {e}")

			recognition_attempt += 1

			if result.reason == speechsdk.ResultReason.RecognizedSpeech:
				return self._handle_recognized_speech(result.text)
			elif result.reason == speechsdk.ResultReason.Canceled:
				self._handle_canceled_recognition(result)
			elif recognition_attempt == 6:
				self._handle_no_match(result)

			# Terminate the program if there is no user input for 5 minutes
			if time() - begin_timer >= 300:  
				print("The program has been terminated due to inactivity.")
				sys.exit()
	
	def _reconfigure_recognizer(self):
		# Get the new language setting
		current_language = self.bot_settings.retrieve_bot_property('language')

		# Recognizer needs language-country code
		language_country_code = self.bot_settings.get_language_country_code(current_language)

		self.speech_config.speech_recognition_language = language_country_code
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
  
	def _handle_recognized_speech(self, recognized_speech):
		# Get the current language setting
		current_language = self.bot_settings.retrieve_bot_property('language')
		print(f"\nInput:\nUser: {recognized_speech}")

		# If the language is not English, translate the recognized speech to English	
		# This is because the LUIS model is trained in English
		if current_language != 'english':
			translated_recognized_speech = self.translator.translate_speech(recognized_speech, current_language, 'english', self.translator_key)
			return {
				'original_speech': recognized_speech, 
				'translated_speech': translated_recognized_speech['response'].replace('.', '').strip()
			}
		return recognized_speech.replace('.', '').strip()

	def _handle_canceled_recognition(self, result):
		cancellation_details = result.cancellation_details
		print(f"Speech Recognition canceled: {cancellation_details.reason}")

		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print(f"Error Details: {cancellation_details.error_details}")
			print("Did you set the speech resource key and region values?")
				 
		
		


