import json
import os
from src.customization.profiles.profile_manager import ProfileManager
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from configuration.manage_secrets import ConfigurationManager 

current_directory = os.path.dirname(os.path.abspath(__file__))
azure_voice_settings_path = os.path.join(current_directory, 'azure', 'azure_voices.json')
language_codes_path = os.path.join(current_directory, 'azure', 'language_codes.json')
elevenlabs_voice_settings_path = os.path.join(current_directory, 'elevenlabs', 'elevenlabs_voices.json')

class VoiceSettingsManager:
	"""
	Class for managing the voice settings for the Azure and Elevenlabs voice engines.
	"""
 
	def __init__(self):
		"""
		Instantiates the class and loads the data from either "azure_voices.json" or "elevenlabs_voices.json"
		"""
		self.configuration_manager = ConfigurationManager()
		self.profile_settings = ProfileManager()
		self.master_settings = MasterSettingsManager()
		self.profile_name = self.master_settings.retrieve_property('profile')
		self.text_to_speech_engine = self.profile_settings.retrieve_property('tts', self.profile_name )
		self.data = self._load_in_voice_data(elevenlabs_voice_settings_path)
			  
	def _load_in_voice_data(self, file_path:str=None) -> dict:
		"""
		Loads the settings from the appropriate file.
		"""
		if not file_path:
			file_path = self._get_file_path(file_path)
		return self._open_file(file_path)

	def _save_data(self, data):
		"""
		Saves data to a file
		"""
		with open(elevenlabs_voice_settings_path, "w") as file:
			json.dump(data, file)

	def save_custom_voice(self, voice_name, type):
		"""
		Saves a property and value
		"""
		if voice_name:
			self.data[type]['english'].append(voice_name)
			data = self.data
	
			self._save_data(data)
   
	def retrieve_voice_name(self, gender:str) -> str:
		"""
		Returns a voice name for a given gender
		"""
		if gender == 'female':
			return list(self.data["female_voices"])[0]
		if gender == 'male':
			return list(self.data["male_voices"])[0]

	def retrieve_available_voices(self) -> list:
		"""
		Returns all available voices
		"""
		all_voices =  list(self.data["female_voices"]['english'])
		male_voices = list(self.data["male_voices"]['english'])
		for voice in male_voices:
			all_voices.append(voice)
		custom_voice = list(self.data["custom"]['english'])
		for voice in custom_voice:
			all_voices.append(voice)
		return all_voices
		
	def retrieve_azure_voice_id(self, gender:str, voice_name:str) -> str:
		"""
		Returns the Azure voice name associated with a given voice name
		"""
		try:
			if voice_name in self.data[f'{gender}_voices'][voice_name]:
				return self.data[f'{gender}_voices'][voice_name]
		except:
				# default to Jenny if no custom voice is found
				return "JennyMultilingualV2Neural"
			
	def retrieve_available_languages(self) -> list:
		"""
		Retrieves all of the available languages 
		"""
		data = self._load_in_voice_data(language_codes_path)
		available_languages = list(data["language_country_codes"].keys())
		# Convert language codes to title case
		available_languages = [language_code.title() for language_code in available_languages]
		available_languages.remove('English')
		available_languages[0] = 'English'
		available_languages[1] = 'Arabic'
		return available_languages
	
	def retrieve_language_code(self, language:str) -> str:
		"""
		Retrieves the language code associated with a specified language
		"""
		data = self._load_in_voice_data(language_codes_path)
		language_codes = data["language_codes"].get(language)
		return language_codes
		
	def retrieve_language_country_code(self, language:str) -> str:
		"""
		Gets the country code for the given language
		"""
		data = self._load_in_voice_data(language_codes_path)
		country_codes = data['language_country_codes'].get(language)
		return country_codes
	
	def _get_file_path(self, file_path:str) -> str:
		"""
		Determine which voice file to open
		"""
		if file_path:
			if self.text_to_speech_engine.lower() == 'azure':
				file_path = azure_voice_settings_path
			elif self.text_to_speech_engine.lower() == 'elevenlabs':
				file_path = elevenlabs_voice_settings_path
		return file_path
	
	def _open_file(self, file_path:str) -> dict:
		"""
		Opens the file and returns the data
		"""
		try:
			with open(file_path, "r") as f:
				return json.load(f)
		except FileNotFoundError:
			print('The file "voice_settings.json" is missing.\nMake sure all files are located within the same folder.')

