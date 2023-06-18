import json
import os
from settings.bot_settings.bot_settings_manager import BotSettingsManager

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the bot_settings.json file in the 'voice' folder
azure_voice_settings_path = os.path.join(current_directory, 'azure_voice_settings.json')
elevenlabs_voice_settings_path = os.path.join(current_directory, 'elevenlabs_voice_settings.json')

class VoiceSettingsManager:
    """
    A class that can retrieve and save properties in "voice_settings.json".
    Data is loaded from the "voice_settings.json" when the class is instantiated.
    The user can then retrieve or save properties from the file.
    """
 
    def __init__(self):
        """
        Instantiates the class and loads the data from "voice_settings.json"
        """
        self.bot_settings = BotSettingsManager()
        self.voice_engine = self.bot_settings.retrieve_property('voice_engine')
        self.data = self.load_voice_settings()
  
    def load_voice_settings(self, file_path:str=None):
        """
        Loads the settings from "voice_settings.json" and saves them in the instance variable 'data'
        """ 
        if file_path:
            pass
        elif self.voice_engine == 'azure':
            file_path = azure_voice_settings_path
        else:
            file_path = elevenlabs_voice_settings_path
        
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "voice_settings.json" is missing.\nMake sure all files are located within the same folder.')

    def retrieve_voice(self, gender:str, language:str) -> str:
        """
        Returns the desired voice name from "voice_settings.json"
        :gender (str): The gender of the voice name
        :language (str): The language of the voice name
        """
        if gender == 'female':
            voice_name = self.data["female_voices"].get(language)
        if gender == 'male':
            voice_name = self.data["male_voices"].get(language)
            
        if isinstance(voice_name, list):
            voice_name = voice_name[0]
        
        return voice_name
    
    def retrieve_voices(self, gender:str, language:str) -> list:
        """
        Returns all voice names associated with a specific 
        gender and language from "voice_settings.json" as a list
        :gender (str): The gender of the voice name
        :language (str): The language of the voice name
        """
        if gender == 'female':
            voice_names = self.data["female_voices"][language]
        if gender == 'male':
            voice_names = self.data["male_voices"][language]
        
        return voice_names
    
    def available_languages(self) -> list:
        """
        Retrieves all of the available languages from "voice_settings.json"
        """
        language_codes = list(self.data["language_codes"].keys())
        return language_codes
    
    def retrieve_language_code(self, language:str) -> str:
        """
        Retrieves the language code associated with a specified language
        from "voice_settings.json"
        """
        data = self.load_voice_settings(azure_voice_settings_path)
        language_codes = data["language_codes"].get(language, None)
        return language_codes
        
    def retrieve_language_country_code(self, language:str) -> str:
        """Gets the country code for the given language"""
        data = self.load_voice_settings(azure_voice_settings_path)
        country_code = data['language_country_codes'].get(language)
        return country_code
    