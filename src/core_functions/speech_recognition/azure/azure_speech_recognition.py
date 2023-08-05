import azure.cognitiveservices.speech as speechsdk
from src.packages.virtual_assistant.high_intent.translate_speech.translate_speech import TranslateSpeech

class AzureSpeechRecognition:
	
	def __init__(self, speech_objects:dict, api_keys:dict, setting_objects:dict):
		self.speech_recognizer = speech_objects['speech_recognizer']
		self.speech_config = speech_objects['audio_config']
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
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
  
		# Get the current language setting
		current_language = self.profile_settings.retrieve_property('language')
		print(f"\nInput:\nUser: {recognized_speech}")

		# If the language is not English, translate the recognized speech to English	
		# This is because the LUIS model is trained in English
		if current_language != 'english':
			return self.translator.translate_speech(speech_to_translate=recognized_speech, current_language=current_language, new_language='english')

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
  