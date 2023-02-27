import json

class BotProperties():
	"""
	A class that can be used to retrieve and save settings from "bot_properties.json"
	"""
	
	def get_property(self, setting):
		"""
		Returns the desired setting attribute from "bot_properties.json"
		:param setting (str): The setting to be retrieved
		"""
		try:
			with open("bot_properties.json", "r") as f:
				data = json.load(f)
			
			# get the bot's voice name given its gender and language
			if setting == 'voice_name':
				gender = data['chatbot'].get('gender')
				language = data['chatbot'].get('language')
				if gender == 'female':
					voice_name =  data['female_voices'].get(language)
				elif gender == 'male':
					voice_name =  data['male_voices'].get(language)

				return voice_name

			# Get available languages
			elif setting == 'languages':
				return list(data['female_voices'].keys())

			# Get available language codes
			elif setting == 'language_codes':
				return data['language_codes']
			
			return data['chatbot'].get(setting)
		
		except FileNotFoundError:
			print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
	
	def save_property(self, setting, value):
		"""
		Saves the desired setting to "bot_properties.json"
		:param setting (str) The setting to be retrieved
		:param value (str) The setting value to be saved
		"""
		try:
			with open("bot_properties.json", "r") as f:
				data = json.load(f)
			
			# saving the setting's value to data
			if setting == 'mute_status':
				data['chatbot'][setting] = value
			elif setting in ['persona', 'gender', 'language']:
				data['chatbot'][setting] = value.lower()
			
			# writing the data back to bot_properties.json
			with open("bot_properties.json", "w") as f:
				json.dump(data, f, indent=4)
		except FileNotFoundError:
			print('The file "bot_properties.json" is missing.\nMake sure all files are located within the same folder')
