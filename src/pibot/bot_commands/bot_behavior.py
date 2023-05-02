
from configuration.bot_properties import BotProperties

class BotBehavior:
	"""
	A class that contains methods to change the behavior of the chatbot.
		
	Atributes:
	speech_verbalizer: an object of the SpeechVerbalizer class
	bot_properties: an object of the BotProperties class
	"""
			
	def __init__(self):
		"""
		Initializes an object of BotBehavior class.
	   	"""
		self.bot_properties = BotProperties()

	def toggle_mute(self):
		"""
		Mutes the bot
		"""
		self.bot_properties.save_property('mute_status', True)
		return 'I am now muted.'
		
	def untoggle_mute(self):
		"""
		Unmutes the bot
		"""
		self.bot_properties.save_property('mute_status', False)
		return 'I am now unmuted.'

	def pause(self):
		"""
		Pauses the bot
		The user must press the spacebar to unpause the bot
		"""
		user_input = ''
		while user_input != ' ':
			user_input = input('Press spacebar to unpause: ')
		return 'I am now unpaused.'

	def change_persona(self, new_persona:str):
		"""
		Changes the bot's persona
		:param new_persona: (str) the new persona to change to
		"""

		self.bot_properties.save_property('persona', new_persona)
		return f'Ok, I have changed my persona to {new_persona}.'

	def change_gender(self, new_gender:str):
		"""
		Changes the bot's gender
		:param new_gender: (str) the new gender to change to
		"""
		if new_gender in ['male', 'female']:
			self.bot_properties.save_property('gender', new_gender)
			response = f'Ok, I have changed my gender to {new_gender}.'
			return {'gender': new_gender, 'speech': response}
		else:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
			
	def change_language(self, new_language:str):
		"""
		Changes the bot's language
		:param new_language: (str) the new language to change to
		"""
		# Extracting all currently supported languages
		languages = self.bot_properties.retrieve_property('languages')
		# Check if language is supported
		if new_language.lower() in languages:
			response = f'Ok, I have changed my language to {new_language}.'
			return {'language': new_language, 'speech': response}
		else:
			return f'Sorry, {new_language} is not currently supported.'