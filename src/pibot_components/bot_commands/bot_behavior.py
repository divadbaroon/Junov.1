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
			
	def __init__(self):
		"""
		Initializes an object of BotBehavior class.
	   	"""
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
		return {'action':'pause', 'response':'I am now paused.'}

	def change_persona(self, new_persona:str) -> str:
		"""
		Saves the new persona of the bot to bot_properties.json
		:param new_persona: (str) the new persona to change to
		"""
		self.bot_settings.save_bot_property('persona', new_persona)
		return f'Ok, I have changed my persona to {new_persona}.'

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
			# Update the current voice name
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
   
			return {'action': 'change_gender', 'response': f'Ok, I have changed my gender to {new_gender}.'}
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
			# Update the current voice name
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
   
			return {'action': 'change_language', 'response': f'Ok, I have changed my language to {new_language}.'}
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
		
		# Update the current voice name
		self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
  
		return {'action': 'change_voice', 'response': 'Ok, I have changed my voice.'}

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

		# Update the current voice name
		self.bot_settings.save_bot_property('current_voice_name', new_voice_name)

		return {'action': 'randomize_voice', 'response': 'Ok, I have changed to a random voice.'}