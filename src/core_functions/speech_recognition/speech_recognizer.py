import sys
from time import time
from .azure.azure_speech_recognition import AzureSpeechRecognition
from src.utils.logs.log_performance import PerformanceLogger

logger = PerformanceLogger()

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_objects:dict, api_keys:dict, setting_objects:dict):
		self.master_settings = setting_objects['master_settings']
		self.profile_settings = setting_objects['profile_settings']
		self.inavtivity_timeout = self.master_settings.retrieve_property('timeout', 'inactivity')
		self.speech_recognition_engine = self.profile_settings.retrieve_property('voice_engine')
  
		if self.speech_recognition_engine == 'azure':
			self.speech_recognition_engine = AzureSpeechRecognition(speech_objects, api_keys, setting_objects)
  
	def listen(self) -> str:
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""
  
		# loading in necessary data from 'master_settings.json'
		self._load_in_settings()
  
		# initiale flag to check whether the speech recognizer needs to be reconfigured
		self._check_and_handle_preconditions()
  
		# Start timer to keep track of the user's inactivity
		begin_timer = time()
	  
		print('\nListening...')
		while True:
			try:
				# Attempt to recognize the user's speech input
				result = self.speech_recognition_engine.attempt_speech_recognition()
				# If the user's speech input was recognized, return the recognized text
				if self.speech_recognition_engine.handle_result(result):
					return self.speech_recognition_engine.handle_recognized_speech(result)
			except Exception as e:
				return e

			# Terminate the program if there is no user input for a default of 5 minutes
			if time() - begin_timer >= self.inavtivity_timeout:  
				print("The program has been terminated due to inactivity.")
				sys.exit()
    
	def _load_in_settings(self):
		"""
  		Loading in necessary data from 'master_settings.json'
    	"""
		self.reconfigure_recognizer = self.master_settings.retrieve_property('functions', 'reconfigure_recognizer')
   
	def _check_and_handle_preconditions(self):
		"""
		Initial flag check
		"""
		# Check if the recognizer needs to be reconfigured
		# This is necessary if the user changes the language setting
		if self.reconfigure_recognizer:
			self.speech_recognition_engine.reconfigure_recognizer()