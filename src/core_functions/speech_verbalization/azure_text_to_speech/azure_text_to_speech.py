import azure.cognitiveservices.speech as speechsdk

class AzureTextToSpeech:
	"""
 	A class that utilizes Azure's Speech Service to verbalize the bot's response.
  	"""
   
	def __init__(self, profile_name:str, speech_objects:dict, setting_objects:dict):
		self.profile_name = profile_name
		self._load_in_settings(setting_objects, speech_objects)
  
	def text_to_speech(self, speech:str, language_country_code:str) -> None:
		"""
  		Performs text-to-speech using Azure's Speech Service.
    	"""
		# prepare ssml file to be used for azure text to speech
		ssml = self._prepare_ssml(speech, language_country_code)
		# perform text to speech
		self.speech_synthesizer.speak_ssml(ssml)
  
	def _prepare_ssml(self, speech:str, language_country_code:str) -> str:
		"""
		Prepare data in ssml format to be used for azure text to speech
		"""
		azure_voice_name = self._retrieve_azure_voice_name()
  
		# prepare ssml file to be used for azure text to speech
		ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
						<voice name="en-US-{azure_voice_name}">
							<prosody rate="1.0">
								<mstts:express-as style="assistant" styledegree="1">
									<lang xml:lang="{language_country_code}">
										{speech}
									</lang>
								</mstts:express-as>
							</prosody>
						</voice>
					</speak>'''
		return ssml

	def update_voice(self) -> None:
		"""
		Updates the voice name used for Azure's Speech Service and reconfigures the speech synthesizer.
  		"""
		azure_voice_name = self._retrieve_azure_voice_name()
		self.speech_config.speech_synthesis_voice_name = azure_voice_name
		self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)
  
	def _retrieve_azure_voice_name(self):
		"""
		Returns the Azure voice name associated with a given voice name
		"""
		current_gender = self.profile_settings.retrieve_property('gender', profile_name=self.profile_name)
		voice_name = self.profile_settings.retrieve_property('voice_name', profile_name=self.profile_name)
		return self.voice_settings.retrieve_azure_voice_name(current_gender, voice_name.title())
  
	def _load_in_settings(self, setting_objects:dict, speech_objects:dict) -> None:
		"""
		Loads necessary settings objects
		"""	
		self.profile_settings = setting_objects['profile_settings']
		self.voice_settings = setting_objects['voice_settings']
		self.speech_synthesizer = speech_objects['speech_synthesizer']
		self.speech_config = speech_objects['speech_config']
		self.audio_config = speech_objects['audio_config']