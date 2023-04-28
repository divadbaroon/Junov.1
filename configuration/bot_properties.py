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
		  
		# Get the bot's voice name given its gender and language
		if setting == 'voice_name':
			gender = self.data['chatbot'].get('gender')
			language = self.data['chatbot'].get('language')
			if gender == 'female':
				voice_name =  self.data['female_voices'].get(language)
			elif gender == 'male':
				voice_name =  self.data['male_voices'].get(language)
			return voice_name

		# Get language
		elif setting == 'languages':
			return list(self.data['female_voices'].keys())

		# Get language
		elif setting == 'female_voices':
			return list(self.data['female_voices'].keys())

		# Get language codes
		elif setting == 'language_codes':
			return self.data['language_codes']

		# Get language codes
		elif setting == 'user_name':
			return self.data['chatbot'].get('user_name')

		# Get language codes
		elif setting == 'user_language':
			return self.data['user'].get('language')

		# Get language codes
		elif setting == 'language_status':
			return self.data['user'].get('language_status')

		elif setting == 'bot_settings':
			return self.data['chatbot']

		else:
			# return the desired setting
			return self.data['chatbot'].get(setting)

	def save_property(self, setting:str, value:str) -> None:
		"""
		Saves the desired setting to "bot_settings.json"
		:param setting (str) The setting to be saved
		:param value (str) The setting value to be saved
		"""
  
		# saving the setting's value to data
		if setting == 'mute_status':
			self.data['chatbot'][setting] = value
		elif setting == 'language_status':
			self.data['user'][setting] = value
		elif setting in ['persona', 'gender', 'language']:
			self.data['chatbot'][setting] = value.lower()
			
		# writing the data back to bot_settings.json
		with open(bot_settings_path, "w") as f:
			json.dump(self.data, f, indent=4)

