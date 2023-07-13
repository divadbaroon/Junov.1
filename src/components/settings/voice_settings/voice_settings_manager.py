import json
import os
from ..bot_settings.bot_settings_manager import BotSettingsManager

# Construct the path to the bot_settings.json file in the 'voice' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
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
        self.voice_engine = self.bot_settings.retrieve_property('voice', 'engine')
        self.data = self.load_voice_settings()
  
    def load_voice_settings(self, file_path:str=None):
        """
        Loads the settings from "voice_settings.json" and saves them in the instance variable 'data'
        """ 
        # get appropriate file path
        if not file_path:
            if self.voice_engine == 'azure':
                file_path = azure_voice_settings_path
            elif self.voice_engine == 'elevenlabs':
                file_path = elevenlabs_voice_settings_path

        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "voice_settings.json" is missing.\nMake sure all files are located within the same folder.')

    def retrieve_next_voice_name(self, gender:str, language:str, current_name:str=None) -> str:
        """
        Returns the next voice name from the given name
        """
        voice_names = self.retrieve_voice_names(gender, language)
        new_voice_name = None
        
        for index, name in enumerate(voice_names):
            if name == current_name:
                if index + 1 < len(voice_names): # Check if there's a next element in the list
                    new_voice_name = voice_names[index + 1]
                else: 
                    new_voice_name = voice_names[0]
        return new_voice_name
                        
    def retrieve_voice_name(self, gender:str, language:str, index:int=0) -> str:
        """
        Returns a voice name associated with a specific 
        gender and language from "voice_settings.json" as a list
        """
        voice_name = self.retrieve_voice_names(gender, language)
        if isinstance(voice_name, list):
            return voice_name[index]
        else:
            return voice_name
             
    def retrieve_voice_names(self, gender:str, language:str) -> list:
        """
        Returns all voice names associated with a specific 
        gender and language from "voice_settings.json" as a list
        """
        if gender == 'female':
            voice_names = self.data["female_voices"][language.lower()]
        if gender == 'male':
            voice_names = self.data["male_voices"][language.lower()]
        return voice_names
    
    def retrieve_azure_voice_name(self, voice_name:str) -> str:
        """
        Returns the Azure voice name assocaited with a given voice name.
        For example, the arg Amber would return en-US-AmberNeural
        """
        for name_pair in self.data['name_pairs']:
            if voice_name in name_pair:
                return name_pair[voice_name]
    
    def available_languages(self) -> list:
        """
        Retrieves all of the available languages from "voice_settings.json"
        """
        data = self.load_voice_settings(azure_voice_settings_path)
        language_codes = list(data["language_codes"].keys())
        return language_codes
    
    def retrieve_language_code(self, language:str) -> str:
        """
        Retrieves the language code associated with a specified language
        from "voice_settings.json"
        """
        # method is only applicable for azure text-to-speech engine
        data = self.load_voice_settings(azure_voice_settings_path)
        language_codes = data["language_codes"].get(language)
        return language_codes
        
    def retrieve_language_country_code(self, language:str) -> str:
        """Gets the country code for the given language"""
        # method is only applicable for azure text-to-speech engine
        data = self.load_voice_settings(azure_voice_settings_path)
        country_codes = data['language_country_codes'].get(language)
        return country_codes
    