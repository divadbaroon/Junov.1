import random

class BotBehavior:
	"""
	A class that contains methods to change the behavior of the chatbot.
	If the command a changing of the bot's voice, the response is returned as a dictionary
	and the voice is reinitialized with the new voice name in speech_verbalizer.py.
		
	Atributes:
	speech_verbalizer: an object of the SpeechVerbalizer class
	bot_properties: an object of the BotProperties class
	"""
			
	def __init__(self, speech_verbalizer:object, setting_objects:dict):
		"""
		Initializes an object of BotBehavior class.
	   	"""
		self.speech_verbalizer = speech_verbalizer
		self.master_settings =  setting_objects['master_settings']
		self.profile_settings = setting_objects['profile_settings']
		self.profile_name = self.master_settings.retrieve_property('profile')
		self.voice_settings = setting_objects['voice_settings']

	def mute(self) -> str:
		"""
		Sets mute status to True in master_settings.json
		"""
		mute_status = self.master_settings.retrieve_property('status', 'mute')
		if mute_status:
			response = 'I am already muted.'
		else:
			self.master_settings.save_property('status', True, 'mute')
			response =  'I am now muted.'

		return response
		
	def unmute(self) -> str:
		"""
		Sets mute status to False in master_settings.json
		"""
		mute_status = self.master_settings.retrieve_property('status', 'mute')
		if not mute_status:
			return 'I am already unmuted.'
		else:
			self.master_settings.save_property('status', False, 'mute')
			return 'I am now unmuted.'

	def pause(self) -> str:
		"""
		Pauses the bot until the user presses enter
		"""
		self.speech_verbalizer.verbalize_speech('I am now paused.')
		key_stroke = input('To unpause, press enter.')
		while key_stroke != '':
			key_stroke = input('To unpause, press enter.')
		return 'I am unpaused'

	def exit(self) -> str:
		"""
		Set exit status to True in master_settings.json
		"""
		self.master_settings.save_property('status', True, 'exit')
		return 'Exiting, goodbye!'

	def change_role(self, new_role:str) -> str:
		"""
		Saves the new role in master_settings.json
		"""
		self.profile_settings.save_property('role', new_role, self.profile_name)
		return f'Ok, I have changed my role to {new_role}.'

	def change_gender(self, new_gender:str) -> str:
		"""
		Saves the new role in master_settings.json
		"""
		# check if gender is currently supported
		if new_gender not in ['male', 'female']:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
      
		# Save the new gender and update the voice
		self.profile_settings.save_property('gender', new_gender, self.profile_name)
		self._reconfigure_voice(new_gender)
  
		return f'Ok, I have changed my gender to {new_gender}.'

	def change_language(self, new_language:str) -> str:
		"""
		Saves the new language in master_settings.json
		"""
		# Extracting all currently supported languages
		currently_supported_languages = self.voice_settings.available_languages()
		new_language = new_language.lower()

		# check if language is currently supported
		if new_language not in currently_supported_languages:
			return f'Sorry, {new_language} is not currently supported.' 
      
		# Save the new language and update the voice
		self.profile_settings.save_property('language', new_language, self.profile_name)
		self.master_settings.save_property('functions', True, 'reconfigure_recognizer')
  
		return f'Ok, I have changed my language to {new_language}.'

	def change_voice(self) -> str:
		"""
		Saves the new voice name in master_settings.json
		"""
		gender = self.profile_settings.retrieve_property('gender')
		language = self.profile_settings.retrieve_property('language')
		current_voice_name = self.profile_settings.retrieve_property('voice_name')

		new_voice_name = self.voice_settings.retrieve_next_voice_name(gender, language, current_voice_name)
 
		self._update_voice_name(new_voice_name)
  
		return 'Ok, I have changed my voice.'

	def randomize_voice(self) -> str:
		"""
		Saves the randomized voice name in master_settings.json
		"""
		gender = self.profile_settings.retrieve_property('gender')
		language = self.profile_settings.retrieve_property('language')
		voices = self.voice_settings.retrieve_voice_names(gender, language)
  
		# If there is only one voice available for that particular language and gender it cannot be changed
		if len(voices) == 1:
			return 'Sorry, I only have one voice available at the moment.'

		# Randomly select a voice name from the list of voice names
		else:
			new_voice_name = voices[random.randint(0, len(voices) - 1)]

		self._update_voice_name(new_voice_name)

		return 'Ok, I have changed to a random voice.'

	def _reconfigure_voice(self, new_property:str) -> None:
		"""
		Reconfigures the voice using the new gender or language.
		"""
		# checking if gender is being changed
		if new_property not in ['male', 'female']:
			current_gender = self.profile_settings.retrieve_property('gender')	
			new_voice_name = self.voice_settings.retrieve_voice_name(current_gender, new_property)
		else:
			current_language = self.profile_settings.retrieve_property('language')
			new_voice_name = self.voice_settings.retrieve_voice_name(new_property, current_language)
		
		self._update_voice_name(new_voice_name)

	def _update_voice_name(self, new_voice_name:str) -> None:
		# Setting new voice name as current
		self.profile_settings.save_property('voice_name', new_voice_name, self.profile_name )
		# Telling the bot to reconfigure the voice synthesizer using the new voice name
		self.master_settings.save_property('functions', True, 'reconfigure_verbalizer')