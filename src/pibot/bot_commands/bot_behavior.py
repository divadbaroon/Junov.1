import sys
import os

# Get the current script's directory and its parent directory
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
grandparent_directory = os.path.dirname(parent_directory)
greatgrandparent_directory = os.path.dirname(grandparent_directory)

# Add the parent directory to sys.path
if greatgrandparent_directory not in sys.path:
    sys.path.append(greatgrandparent_directory)
    
from settings.settings_manager import SettingsOrchestrator
import random

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
		self.bot_settings = SettingsOrchestrator()

	def toggle_mute(self):
		"""
		Mutes the bot
		"""
		self.bot_settings.save_bot_property('mute_status', True)
		return 'I am now muted.'
		
	def untoggle_mute(self):
		"""
		Unmutes the bot
		"""
		self.bot_settings.save_bot_property('mute_status', False)
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

		self.bot_settings.save_bot_property('persona', new_persona)
		return f'Ok, I have changed my persona to {new_persona}.'

	def change_gender(self, new_gender:str):
		"""
		Changes the bot's gender
		:param new_gender: (str) the new gender to change to
		"""
		if new_gender in ['male', 'female']:
			# Save the new gender to bot_properties.json
			self.bot_settings.save_bot_property('gender', new_gender)
			# Get the new voice name
			new_voice_name = self.bot_settings.get_bot_property('voice_name')
			# Update the current voice name
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
   
			response = f'Ok, I have changed my gender to {new_gender}.'
			return {'change_gender': new_gender, 'response': response}
		else:
			return f"Sorry, I only support 'Male' or 'Female' at the moment. Please choose one of these options."
			
	def change_language(self, new_language:str):
		"""
		Changes the bot's language
		:param new_language: (str) the new language to change to
		"""
		# Extracting all currently supported languages
		languages = self.bot_settings.get_bot_property('languages')
		# Check if language is supported
		if new_language.lower() in languages:
			# Save the new language to bot_properties.json
			self.bot_settings.save_bot_property('language', new_language.lower())
			# Get the new voice name
			new_voice_name = self.bot_settings.get_bot_property('voice_name')
			# Update the current voice name
			self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
   
			response = f'Ok, I have changed my language to {new_language}.'
			return {'change_language': new_language, 'response': response}
		else:
			return f'Sorry, {new_language} is not currently supported.'

	def change_voice(self):
		"""
		Changes to the next bot's voice name
		"""
		voices = self.bot_settings.get_bot_property('voice_names')
		current_voice_name = self.bot_settings.get_bot_property('current_voice_name')
		new_voice_name = ''

		# If there is only one voice available for that particular language and gender it cannot be changed
		if len(voices) == 1:
			return 'Sorry, I only have one voice available at the moment.'

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
		return {'change_voice_name': new_voice_name, 'response':'Ok, I have changed my voice.'}

	def randomize_voice(self):
		"""
		Randomizes the bot's voice
		"""
		voices = self.bot_settings.get_bot_property('voice_names')
		new_voice_name = ''
  
		# If there is only one voice available for that particular language and gender it cannot be changed
		if len(voices) == 1:
			return 'Sorry, I only have one voice available at the moment.'

		# Randomly select a voice name from the list of voice names
		else:
			new_voice_name = voices[random.randint(0, len(voices) - 1)]

		# Update the current voice name
		self.bot_settings.save_bot_property('current_voice_name', new_voice_name)
		return {'change_voice_name': new_voice_name, 'response':'Ok, I have changed to a random voice.'}
