
import os
import sys

# Get the current script's directory and its parent directory
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

# Add the parent directory to sys.path
if parent_directory not in sys.path:
	sys.path.append(parent_directory)

import azure.cognitiveservices.speech as speechsdk
from time import time
from configuration.bot_properties import BotProperties

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_config, speech_recognizer):
		self.speech_recognizer = speech_recognizer
		self.speech_config = speech_config
		self.bot_properties = BotProperties()

	def listen(self):
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""

		# Check if the bot_settings.json file has been modified and needs to be reloaded
		# This is done when a property such as the language is changed 
		# In which the recognizer needs to be reconfigured to recognize the new language
		self.bot_properties.reload_settings()
		reconfigure = self.bot_properties.retrieve_property('reconfigure')
		
		if reconfigure:
		
			# Get the new language setting
			language_setting = self.bot_properties.retrieve_property('language')

			# Recognizer needs language-country code
			language_country_code = self.bot_properties.get_language_country_code(language_setting)
			print(language_country_code)
			self.speech_config.speech_recognition_language = language_country_code
			self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)

			# Set reconfigure to False so that the bot_settings.json file is not reloaded again
			self.bot_properties.save_property('reconfigure', False)
		
		print("\nListening...")  
		
		# It appears the current implementation of .recognize_once_async() can only attempt to listen for input for 5 seconds
		# To accommodate for this limitation, recognition_attempt allows for 6 attempts at 5 seconds each, for a total of 30 seconds
		# This allows for a longer window of speech recognition while also avoiding repetitive prompts to the user
		# This approach may not be ideal and a better solution is currently being sought
		recognition_attempt = 0
		
		# Time in seconds until the program ends if no speech is detected (5 minutes by default)
		# This is to prevent unintentional continuous listening to the user
		time_until_exit = 300
		
		# Starting timer
		begin_timer = time()  

		# Continuously listen for speech
		while True:
			try:
				# A 5 second attempt to recognize the user's speech input
				result = self.speech_recognizer.recognize_once_async().get() 
			except Exception as e:
				print(f"Error occurred during speech recognition: {e}")
			
			recognition_attempt += 1
			
			# If speech was recognized, print it and return it
			if result.reason == speechsdk.ResultReason.RecognizedSpeech:
				recognized_speech = result.text
				print(f"\nInput:\nUser: {recognized_speech}")
				return recognized_speech.replace('.', '').strip()
			
			# If the recognition was cancelled, check if it was due to an error
			elif result.reason == speechsdk.ResultReason.Canceled:
				cancellation_details = result.cancellation_details
				print(f"Speech Recognition canceled: {cancellation_details.reason}")
				
				if cancellation_details.reason == speechsdk.CancellationReason.Error:
					print(f"Error Detais: {cancellation_details.error_details}")
					print("Did you set the speech resource key and region values?")
			
			# If no speech was recognized after 30 seconds (6 attempts at 5 seconds each), notify the user that no speech was detected
			elif recognition_attempt == 6:
				if result.reason == speechsdk.ResultReason.NoMatch:
					print(f'No speech could be recognized: {result.no_match_details}')
				recognition_attempt = 0

			# Ending timer
			end_timer = time()
			elapsed_time = end_timer - begin_timer
			
			# Terminate the program if no speech is detected after 5 minutes
			if elapsed_time >= time_until_exit:
				print("The program has been terminated due to inactivity.")
				sys.exit()
				 
		
		


