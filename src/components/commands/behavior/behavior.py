from settings.settings_orchestrator import SettingsOrchestrator
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
			
	def __init__(self, speech_verbalizer):
		"""
		Initializes an object of BotBehavior class.
	   	"""
		self.speech_verbalizer = speech_verbalizer
		self.bot_settings = SettingsOrchestrator()

	def mute(self) -> str:
		"""
		Saves the mute status of the bot to True in bot_properties.json
		"""
		mute_status = self.bot_settings.retrieve_bot_property('mute_status')
		if mute_status:
			return 'I am already muted.'
		else:
			self.bot_settings.save_bot_property('mute_status', True)
			return 'I am now muted.'
		
	def unmute(self) -> str:
		"""
		Saves the mute status of the bot to False in bot_properties.json
		"""
		mute_status = self.bot_settings.retrieve_bot_property('mute_status')
		if not mute_status:
			return 'I am already unmuted.'
		else:
			self.bot_settings.save_bot_property('mute_status', False)
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
		self.bot_settings.save_bot_property('role', new_role)
		return f'Ok, I have changed my role to {new_role}.'

	def change_gender(self, new_gender:str) -> str:
		"""
		Changes the bot's gender
		:param new_gender: (str) the new gender to change to
		"""
		if new_gender in ['male', 'female']:
			# Save the new gender to bot_properties.json
			self.bot_settings.save_bot_property('gender', new_gender)
			# Get the new voice name
			gender = self.bot_settings.retrieve_bot_property('gender')
			current_language = self.bot_settings.retrieve_bot_property('language')
			new_voice_name = self.bot_settings.retrieve_voice_name(gender, current_language)
			
			self._update_voice_name(new_voice_name)
   
			return f'Ok, I have changed my gender to {new_gender}.'
		else:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
			
	def change_language(self, new_language:str) -> str:
		"""
		Changes the bot's language
		:param new_language: (str) the new language to change to
		"""
		# Extracting all currently supported languages
		languages = self.bot_settings.retrieve_available_languages()
		# Check if language is supported
		if new_language.lower() in languages:
			# Save the new language to bot_properties.json
			self.bot_settings.save_bot_property('language', new_language.lower())
			# Get the new voice name
			gender = self.bot_settings.retrieve_bot_property('gender')
			current_language = self.bot_settings.retrieve_bot_property('language')
			new_voice_name = self.bot_settings.retrieve_voice_name(gender, current_language)
			
			self._update_voice_name(new_voice_name)
   
			return f'Ok, I have changed my language to {new_language}.'
		else:
			return f'Sorry, {new_language} is not currently supported.'

	def change_voice(self) -> str:
		"""
		Changes to the next bot's voice name
		"""
		gender = self.bot_settings.retrieve_bot_property('gender')
		language = self.bot_settings.retrieve_bot_property('language')
		voices = self.bot_settings.retrieve_voice_names(gender, language)
		current_voice_name = self.bot_settings.retrieve_bot_property('current_voice_name')
		new_voice_name = ''

		# If voices is not a list then there is only one available voice for that language
		if isinstance(voices, str):
			return f'Sorry, I only have one voice available at the moment for {language}.'
		else:
			# Change to the next voice name in the list
			for index, value in enumerate(voices):
				if value == current_voice_name:
					if index == len(voices) - 1:
						new_voice_name = voices[0]
					else:
						new_voice_name = voices[index + 1]
					break
 
		self._update_voice_name(new_voice_name)
  
		return 'Ok, I have changed my voice.'

	def randomize_voice(self) -> str:
		"""
		Randomizes the bot's voice
		"""
		gender = self.bot_settings.retrieve_bot_property('gender')
		language = self.bot_settings.retrieve_bot_property('language')
		voices = self.bot_settings.retrieve_voice_names(gender, language)
		new_voice_name = ''
  
		# If there is only one voice available for that particular language and gender it cannot be changed
		if len(voices) == 1:
			return 'Sorry, I only have one voice available at the moment.'

		# Randomly select a voice name from the list of voice names
		else:
			new_voice_name = voices[random.randint(0, len(voices) - 1)]

		self._update_voice_name(new_voice_name)

		return 'Ok, I have changed to a random voice.'

	def _update_voice_name(self, new_voice_name):
		# Update the current voice name
		voice_engine = self.bot_settings.retrieve_bot_property('voice_engine')
		if voice_engine == 'azure':
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
		else:
			self.bot_settings.save_bot_property('current_elevenlabs_voice_name', new_voice_name)