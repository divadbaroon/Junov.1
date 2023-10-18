import sys
from time import time
from .azure_speech_recognition.azure_speech_recognition import AzureSpeechRecognition
from src.utilities.logs.log_performance import PerformanceLogger

logger = PerformanceLogger()

class SpeechRecognition:
	"""
	A class that utilizes Azure's Cognitive Speech Service to recognize the user's speech input.
	""" 
	
	def __init__(self, speech_objects:dict, api_keys:dict, setting_objects:dict):
		"""
		Initializes settings and speech recognition engine		
  		"""
		self._load_in_settings(setting_objects)
  
		# Initialize the speech recognition engine
		if self.speech_recognition_engine == 'azure':
			self.speech_recognition_engine = AzureSpeechRecognition(speech_objects, api_keys, setting_objects)

	@logger.log_operation
	def listen(self) -> str:
		"""
		Listens for speech input and returns the recognized text in lowercase.
		:return: (str) The recognized speech input as a lowercase string.
		"""
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
				print(f"Error occurred during speech recognition: {e}")

			# Terminate the program if there is no user input for a default of 5 minutes
			if time() - begin_timer >= self.inavtivity_timeout:  
				print("The program has been terminated due to inactivity.")
				sys.exit()
    
	def _load_in_settings(self, setting_objects:dict) -> None:
		"""
  		Loading in necessary data from 'master_settings.json'
    	"""
		self.master_settings = setting_objects['master_settings']
		self.profile_settings = setting_objects['profile_settings']
		self.inavtivity_timeout = self.master_settings.retrieve_property('timeout', 'inactivity')
		self.speech_recognition_engine = self.profile_settings.retrieve_property('voice_recognition_engine')
   
	def _check_and_handle_preconditions(self) -> None:
		"""
		Initial flag check
		"""
		reconfigure_recognizer = self.master_settings.retrieve_property('functions', 'reconfigure_recognizer')
		if reconfigure_recognizer:
			self.speech_recognition_engine.reconfigure_recognizer()