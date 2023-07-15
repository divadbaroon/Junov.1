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
			
	def __init__(self, speech_verbalizer:object, bot_settings:object, voice_settings:object):
		"""
		Initializes an object of BotBehavior class.
	   	"""
		self.speech_verbalizer = speech_verbalizer
		self.bot_settings =  bot_settings
		self.voice_settings = voice_settings

	def mute(self) -> str:
		"""
		Sets mute status to True in bot_settings.json
		"""
		mute_status = self.bot_settings.retrieve_property('status', 'mute')
		if mute_status:
			response = 'I am already muted.'
		else:
			self.bot_settings.save_property('status', True, 'mute')
			response =  'I am now muted.'

		return response
		
	def unmute(self) -> str:
		"""
		Sets mute status to False in bot_settings.json
		"""
		mute_status = self.bot_settings.retrieve_property('status', 'mute')
		if not mute_status:
			return 'I am already unmuted.'
		else:
			self.bot_settings.save_property('status', False, 'mute')
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

	def change_role(self, new_role:str) -> str:
		"""
		Saves the new role in bot_settings.json
		"""
		self.bot_settings.save_property('role', new_role)
		return f'Ok, I have changed my role to {new_role}.'

	def change_gender(self, new_gender:str) -> str:
		"""
		Saves the new role in bot_settings.json
		"""
		# check if gender is currently supported
		if new_gender not in ['male', 'female']:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
      
		# Save the new gender and update the voice
		self.bot_settings.save_property('gender', new_gender, 'current')
		self._reconfigure_voice(new_gender)
  
		return f'Ok, I have changed my gender to {new_gender}.'

	def change_language(self, new_language:str) -> str:
		"""
		Saves the new language in bot_settings.json
		"""
		# Extracting all currently supported languages
		currently_supported_languages = self.voice_settings.available_languages()
		new_language = new_language.lower()

		# check if language is currently supported
		if new_language not in currently_supported_languages:
			return f'Sorry, {new_language} is not currently supported.' 
      
		# Save the new language and update the voice
		self.bot_settings.save_property('language', new_language, 'current')
		self._reconfigure_voice(new_language)
  
		return f'Ok, I have changed my language to {new_language}.'

	def change_voice(self) -> str:
		"""
		Saves the new voice name in bot_settings.json
		"""
		gender = self.bot_settings.retrieve_property('gender', 'current')
		language = self.bot_settings.retrieve_property('language', 'current')
		current_voice_name = self.bot_settings.retrieve_property('voice', 'current_voice_name')

		new_voice_name = self.voice_settings.retrieve_next_voice_name(gender, language, current_voice_name)
 
		self._update_voice_name(new_voice_name)
  
		return 'Ok, I have changed my voice.'

	def randomize_voice(self) -> str:
		"""
		Saves the randomized voice name in bot_settings.json
		"""
		gender = self.bot_settings.retrieve_property('gender', 'current')
		language = self.bot_settings.retrieve_property('language', 'current')
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
			current_gender = self.bot_settings.retrieve_property('gender', 'current')	
			new_voice_name = self.voice_settings.retrieve_voice_name(current_gender, new_property)
		else:
			current_language = self.bot_settings.retrieve_property('language', 'current')
			new_voice_name = self.voice_settings.retrieve_voice_name(new_property, current_language)
		
		self._update_voice_name(new_voice_name)

	def _update_voice_name(self, new_voice_name:str) -> None:
		# Saving current voice name first before it is replaced
		current_voice_name = self.bot_settings.retrieve_property('voice', 'name')
		self.bot_settings.save_property('voice', current_voice_name, 'previous_voice_name')
		# Setting new voice name as current
		self.bot_settings.save_property('voice', new_voice_name, 'current_voice_name')
		# Telling the bot to reconfigure the voice synthesizer using the new voice name
		self.bot_settings.save_property('voice', True, 'reconfigure')