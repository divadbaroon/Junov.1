import azure.cognitiveservices.speech as speechsdk
from time import time
import sys

from src.components.commands.translate_speech.translate_speech import TranslateSpeech

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_recognizer, bot_settings, api_keys):
		self.speech_recognizer = speech_recognizer
		self.translator = TranslateSpeech(api_keys['translator_key'])
		self.bot_settings = bot_settings
		self.inavtivity_timeout = self.bot_settings.retrieve_bot_property('inactivity_timeout')

	def listen(self):
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""
  
		# Check if bot is in idle mode
		# In which listening will begin once the user presses enter
		self._check_for_idle_mode()

		# Start a timer to keep track of the user's inactivity
		begin_timer = time()
	  
		print("\nListening...")  
		while True:
			try:
				# A 5-second attempt to recognize the user's speech input
				result = self.speech_recognizer.recognize_once_async().get() 
			except Exception as e:
				print(f"Error occurred during speech recognition: {e}")

			if result.reason == speechsdk.ResultReason.RecognizedSpeech:
				return self._handle_recognized_speech(result.text)
			elif result.reason == speechsdk.ResultReason.Canceled:
				self._handle_canceled_recognition(result)

			# Terminate the program if there is no user input for a default of 5 minutes
			if time() - begin_timer >= self.inavtivity_timeout:  
				print("The program has been terminated due to inactivity.")
				sys.exit()
	
	def _reconfigure_recognizer(self) -> None:
		"""Reconfigures the speech recognizer with the new language setting"""
  
		# Get the new language setting
		current_language = self.bot_settings.retrieve_bot_property('language')

		# Recognizer needs language-country code
		language_country_code = self.bot_settings.get_language_country_code(current_language)

		self.speech_config.speech_recognition_language = language_country_code
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
  
	def _handle_recognized_speech(self, recognized_speech:str or dict) -> str or dict:
		"""Handles the recognized speech input"""
  
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

	def _handle_canceled_recognition(self, result:str) -> None:
		"""Handles the canceled speech recognition"""
  
		cancellation_details = result.cancellation_details
		print(f"Speech Recognition canceled: {cancellation_details.reason}")

		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print(f"Error Details: {cancellation_details.error_details}")
			print("Did you set the speech resource key and region values?")
		return None

	def _check_for_idle_mode(self) -> None:
		"""Checks if the bot is in idle mode"""
  
		# reload settings and retrieve idle status
		self.bot_settings.reload_bot_settings()
		self.idle_status = self.bot_settings.retrieve_bot_property('idle_status')
		# if idle status is true, start idle mode
		if self.idle_status:
			self._activate_idle_mode()
	
	def _activate_idle_mode(self) -> None:
		"""Puts the bot in idle mode"""
  
		start_listening = input('Press enter to start listening...')
		if start_listening == '':
			self.idle_status = self.bot_settings.save_bot_property('idle_status', False)
		else:
			self._activate_idle_mode()
	
				 
		
		


