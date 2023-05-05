import json
import os

# Get the current script's directory and the configuration directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the bot_settings.json file
bot_settings_path = os.path.join(current_directory, 'bot_settings.json')

class BotProperties():
	"""
	A class that can  retrieve and save properties in "bot_settings.json".
	Data is loaded from the "bot_settings.json" when the class is instantiated.
	The user can then retrieve or save properties from the file.
	"""
 
	def __init__(self):
		"""
		Instantiates the class and loads the data from "bot_settings.json"
		"""
		self.data = self.load_properties()
  
	def load_properties(self) -> None:
		"""
		Loads the settings from "bot_settings.json" and saves them in the instance variable 'data'
		""" 
  
		# load data from "bot_settings.json"
		try:
			with open(bot_settings_path, "r") as f:
				return json.load(f)
		except FileNotFoundError:
			print('The file "bot_settings.json" is missing.\nMake sure all files are located within the same folder.')
			raise SystemExit()
	 
	def retrieve_property(self, setting:str) -> str:
		"""
		Returns the desired setting from "bot_settings.json"
		:param setting (str): The setting to be retrieved
		"""
		  
		# Returns the bot's voice names for a particular gender and language
		# If the bot has multiple voices for a particular language, it will return a list
		if setting == 'voice_names':
			gender = self.data['chatbot'].get('gender')
			language = self.data['chatbot'].get('language')
			if gender == 'female':
				voice_name =  self.data['female_voices'].get(language)
			elif gender == 'male':
				voice_name =  self.data['male_voices'].get(language)
			
			return voice_name

		# Returns the bot's voice names for a particular gender and language
		# If the bot has multiple voices for a particular language, it will return the first value in the list
		if setting == 'voice_name':
			gender = self.data['chatbot'].get('gender')
			language = self.data['chatbot'].get('language')
			if gender == 'female':
				voice_name =  self.data['female_voices'].get(language)
			elif gender == 'male':
				voice_name =  self.data['male_voices'].get(language)
    
			if isinstance(voice_name, list):
				return voice_name[0]
			else:
				return voice_name

		# Get language
		elif setting == 'languages':
			return list(self.data['female_voices'].keys())

		# Get female voices
		elif setting == 'female_voices':
			return list(self.data['female_voices'].keys())

		# Get male voices
		elif setting == 'male_voices':
			return list(self.data['male_voices'].keys())

		# Get language codes
		elif setting == 'language_codes':
			return self.data['language_codes']

		elif setting == 'bot_settings':
			return self.data['chatbot']

		else:
			# return the desired setting
			return self.data['chatbot'].get(setting)

	def save_property(self, setting:str, value) -> None:
		"""
		Saves the desired setting to "bot_settings.json"
		:param setting (str) The setting to be saved
		:param value (str) The setting value to be saved
		"""
  
		# saving the setting's value to data
		if setting == 'mute_status':
			self.data['chatbot'][setting] = value
		if setting == 'reconfigure':
			self.data['chatbot'][setting] = value
		if setting == 'reconfigure':
			self.data['chatbot'][setting] = value
		if setting == 'current_voice_name':
			self.data['chatbot'][setting] = value
		if setting == 'gender':
			self.data['chatbot'][setting] = value.lower()
		if setting == 'language':
			self.data['chatbot'][setting] = value.lower()
		if setting == 'persona':
			self.data['chatbot'][setting] = value.title()
		
		# writing the data back to bot_settings.json
		with open(bot_settings_path, "w") as f:
			json.dump(self.data, f, indent=4)
   
	def get_language_country_code(self, language: str) -> str:
		"""Gets the country code for the given language"""
		country_code = self.data['language_country_codes'].get(language)
		return country_code

	def reload_settings(self):
		"""Reloads the data from bot_settings.json"""
		with open(bot_settings_path, 'r', encoding='utf-8') as file:
			self.data = json.load(file)
