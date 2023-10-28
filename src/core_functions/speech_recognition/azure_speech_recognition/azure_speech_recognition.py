import azure.cognitiveservices.speech as speechsdk
from src.customization.packages.virtual_assistant.commands.translate_speech.translate_speech import TranslateSpeech

import streamlit as st

class AzureSpeechRecognition:
	"""
	Handles the speech recognition using Azure's Speech SDK
	"""
	
	def __init__(self, speech_objects:dict, api_keys:dict, setting_objects:dict):
		self._load_in_settings(speech_objects, setting_objects)
		self.translator = TranslateSpeech(api_keys['TRANSLATOR-API-KEY'], setting_objects)
  
	def attempt_speech_recognition(self) -> str:
		"""
		A 5-second attempt to recognize the user's speech input
  		"""
		try:
			result = self.speech_recognizer.recognize_once_async().get() 
		except Exception as e:
			print(f"Error occurred during speech recognition: {e}")
   
		return result

	def handle_result(self, result:str) -> str:
		"""
		Handles the result of the speech recognition. Code is from Azure's Speech SDK documentation.
		"""
		if result.reason == speechsdk.ResultReason.RecognizedSpeech:
			return True
		elif result.reason == speechsdk.ResultReason.NoMatch:
			pass
		elif result.reason == speechsdk.ResultReason.Canceled:
			cancellation_details = result.cancellation_details
			print("Speech Recognition canceled: {}".format(cancellation_details.reason))
			if cancellation_details.reason == speechsdk.CancellationReason.Error:
				print("Error details: {}".format(cancellation_details.error_details))
				print("Did you set the speech resource key and region values?")
		return None

	def handle_recognized_speech(self, result) -> str:
		"""
  		Handles the recognized speech input
    	"""
		recognized_speech = result.text
  
		print(f"\nInput:\nUser: {recognized_speech}")
  
		# If the gui is being used, write the user input to it
		if self.gui:
			self._write_input_to_gui(recognized_speech)
  
		return recognized_speech.replace('.', '').strip()

	def reconfigure_recognizer(self) -> None:
		"""
  		Reconfigures the speech recognizer with the new language setting
    	"""
		# Get the new language setting
		current_language = self.profile_settings.retrieve_property('language')

		# Recognizer needs language-country code
		language_country_code = self.voice_settings.retrieve_language_country_code(current_language)

		self.speech_config.speech_recognition_language = language_country_code
		self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
  
	def _write_input_to_gui(self, recognized_speech) -> None:
		"""
		Write user input to gui if it is being used
		"""
		if self.user_name:
			with st.chat_message("user"):
				st.write(f'{self.user_name.title()}: {recognized_speech}')
		else:
			with st.chat_message("user"):
					st.write(f'User: {recognized_speech}')
  
	def _load_in_settings(self, speech_objects, setting_objects): 
		"""
		Loads in the speech and setting objects
		"""
		self.speech_recognizer = speech_objects['speech_recognizer']
		self.speech_config = speech_objects['speech_config']
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.master_settings = setting_objects['master_settings']
		self.profile_name = self.master_settings.retrieve_property('profile')
		self.gui = self.master_settings.retrieve_property('functions', 'gui')
		#self.user_name = self.profile_settings.retrieve_property('user_name', self.profile_name)
		self.user_name = None