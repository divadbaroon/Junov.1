import azure.cognitiveservices.speech as speechsdk
from time import time
import sys

from src.components.commands.translate_speech.translate_speech import TranslateSpeech

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_objects:dict, api_keys:dict, bot_settings:object, voice_settings:object):
		self.speech_recognizer = speech_objects['speech_recognizer']
		self.spech_config = speech_objects['audio_config']
		self.api_keys = api_keys
		self.bot_settings = bot_settings
		self.voice_settings = voice_settings
		self.inavtivity_timeout = self.bot_settings.retrieve_property('timeout', 'inactivity')
		self.translator = TranslateSpeech(api_keys['translator_key'], bot_settings, voice_settings)
  
	def listen(self) -> str:
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""
		# Start a timer to keep track of the user's inactivity
		begin_timer = time()
	  
		print("\nListening...")  
		while True:
			# A 5-second attempt to recognize the user's speech input
			result = self._attempt_speech_recognition()

			# If speech is recognized, return it
			if result.reason == speechsdk.ResultReason.RecognizedSpeech:
				return self._handle_recognized_speech(result.text)
			elif result.reason == speechsdk.ResultReason.Canceled:
				self._handle_canceled_recognition(result)

			# Terminate the program if there is no user input for a default of 5 minutes
			if time() - begin_timer >= self.inavtivity_timeout:  
				print("The program has been terminated due to inactivity.")
				sys.exit()
	
	def _attempt_speech_recognition(self) -> str:
		"""
		A 5-second attempt to recognize the user's speech input
  		"""
		try:
			result = self.speech_recognizer.recognize_once_async().get() 
		except Exception as e:
			print(f"Error occurred during speech recognition: {e}")
   
		return result
	
	def _reconfigure_recognizer(self) -> None:
		"""Reconfigures the speech recognizer with the new language setting"""
  
		# Get the new language setting
		current_language = self.bot_settings.retrieve_property('language', 'current')

		# Recognizer needs language-country code
		language_country_code = self.voice_settings.retrieve_language_country_code(current_language)

		self.speech_config.speech_recognition_language = language_country_code
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
  
	def _handle_recognized_speech(self, recognized_speech:str) -> str:
		"""Handles the recognized speech input"""
  
		# Get the current language setting
		current_language = self.bot_settings.retrieve_property('language', 'current')
		print(f"\nInput:\nUser: {recognized_speech}")

		# If the language is not English, translate the recognized speech to English	
		# This is because the LUIS model is trained in English
		if current_language != 'english':
			return self.translator.translate_speech(speech_to_translate=recognized_speech, current_language=current_language, new_language='english')

		return recognized_speech.replace('.', '').strip()

	def _handle_canceled_recognition(self, result:str) -> None:
		"""Handles the canceled speech recognition"""
  
		cancellation_details = result.cancellation_details
		print(f"Speech Recognition canceled: {cancellation_details.reason}")

		if cancellation_details.reason == speechsdk.CancellationReason.Error:
			print(f"Error Details: {cancellation_details.error_details}")
			print("Did you set the speech resource key and region values?")
		return None
				 
		
		


