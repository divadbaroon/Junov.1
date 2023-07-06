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
		Saves the mute status of the bot to True in bot_properties.json
		"""
		mute_status = self.bot_settings.retrieve_property('status', 'mute')
		self.speech_verbalizer.verbalize_speech('I am now muted.')
		if mute_status:
			response = 'I am already muted.'
		else:
			self.bot_settings.save_property('status', True, 'mute')
			response =  'I am now muted.'

		self.speech_verbalizer.verbalize_speech(response)
		
	def unmute(self) -> str:
		"""
		Saves the mute status of the bot to False in bot_properties.json
		"""
		mute_status = self.bot_settings.retrieve_property('status', 'mute')
		if not mute_status:
			return 'I am already unmuted.'
		else:
			self.bot_settings.save_property('status', False, 'mute')
			return 'I am now unmuted.'

	def pause(self) -> dict:
		"""
		A dictionary containing the action and response of the bot is returned.
		The actual action of pausing the bot is done in the speech_verbalizer.py file.
		"""
		self.speech_verbalizer.verbalize_speech('I am now paused.')
		key_stroke = input('To unpause, press enter.')
		while key_stroke != '':
			key_stroke = input('To unpause, press enter.')
		return 'I am unpaused'

	def change_role(self, new_role:str) -> str:
		"""
		Saves the new role of the bot to bot_properties.json
		:param new_role: (str) the new role to change to
		"""
		self.bot_settings.save_property('role', new_role)
		return f'Ok, I have changed my role to {new_role}.'

	def change_gender(self, new_gender:str) -> str:
		"""
		Changes the bot's gender
		:param new_gender: (str) the new gender to change to
		"""
		if new_gender in ['male', 'female']:
			# Save the new gender to bot_properties.json
			self.bot_settings.save_property('gender', new_gender, 'current')
			# Get the new voice name
			current_language = self.bot_settings.retrieve_property('language', 'current')
			new_voice_name = self.voice_settings.retrieve_voice_name(new_gender, current_language)
			
			current_engine = self.bot_settings.retrieve_property('voice', 'engine')
			if current_engine == 'azure':
				current_voice_name = self.bot_settings.retrieve_property('voice', 'current_azure_voice_name')
			else:
				current_voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')

			self._update_voice_name(new_voice_name, current_voice_name)
   
			return f'Ok, I have changed my gender to {new_gender}.'
		else:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
			
	def change_language(self, new_language:str) -> str:
		"""
		Changes the bot's language
		:param new_language: (str) the new language to change to
		"""
		# Extracting all currently supported languages
		languages = self.voice_settings.available_languages()
		new_language = new_language.lower()
		# Check if language is supported
		if new_language in languages:
			# Save the new language to bot_properties.json
			self.bot_settings.save_property('language', new_language, 'current')
			# Get the new voice name
			gender = self.bot_settings.retrieve_property('gender', 'current')
			new_voice_name = self.voice_settings.retrieve_voice_name(gender, new_language)
			
			current_engine = self.bot_settings.retrieve_property('voice', 'engine')
			if current_engine == 'azure':
				current_voice_name = self.bot_settings.retrieve_property('voice', 'current_azure_voice_name')
			else:
				current_voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')
			self._update_voice_name(new_voice_name, current_voice_name)
   
			return f'Ok, I have changed my language to {new_language}.'
		else:
			return f'Sorry, {new_language} is not currently supported.'

	def change_voice(self) -> str:
		"""
		Changes to the next bot's voice name
		"""
		gender = self.bot_settings.retrieve_property('gender', 'current')
		language = self.bot_settings.retrieve_property('language', 'current')
		current_engine = self.bot_settings.retrieve_property('voice', 'engine')
		if current_engine == 'azure':
			current_voice_name = self.bot_settings.retrieve_property('voice', 'current_azure_voice_name')
		else:
			current_voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')

		new_voice_name = self.voice_settings.retrieve_next_voice_name(gender, language, current_voice_name)
 
		self._update_voice_name(new_voice_name, current_voice_name)
  
		return 'Ok, I have changed my voice.'

	def randomize_voice(self) -> str:
		"""
		Randomizes the bot's voice
		"""
		gender = self.bot_settings.retrieve_property('gender', 'current')
		language = self.bot_settings.retrieve_property('language', 'current')
		current_engine = self.bot_settings.retrieve_property('voice', 'engine')
		if current_engine == 'azure':
			current_voice_name = self.bot_settings.retrieve_property('voice', 'current_azure_voice_name')
		else:
			current_voice_name = self.bot_settings.retrieve_property('voice', 'current_elevenlabs_voice_name')
		voices = self.voice_settings.retrieve_voice_names(gender, language)
		new_voice_name = ''
  
		# If there is only one voice available for that particular language and gender it cannot be changed
		if len(voices) == 1:
			return 'Sorry, I only have one voice available at the moment.'

		# Randomly select a voice name from the list of voice names
		else:
			new_voice_name = voices[random.randint(0, len(voices) - 1)]

		self._update_voice_name(new_voice_name, current_voice_name)

		return 'Ok, I have changed to a random voice.'

	def _update_voice_name(self, new_voice_name, previous_voice_name):
		# Update the current voice name
		voice_engine = self.bot_settings.retrieve_property('voice', 'engine')
		if voice_engine == 'azure':
			self.bot_settings.save_property('current_azure_voice_name', new_voice_name)
			self.bot_settings.save_property('previous_azure_voice_name', previous_voice_name)
		elif voice_engine == 'elevenlabs':
			self.bot_settings.save_property('current_elevenlabs_voice_name', new_voice_name)
			self.bot_settings.save_property('previous_elevenlabs_voice_name', previous_voice_name)
		self.bot_settings.save_property('reconfigure_voice', True)