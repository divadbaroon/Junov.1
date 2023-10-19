import json
import os
from src.customization.profiles.profile_manager import ProfileManager

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
        self.profile_settings = ProfileManager()
        self.voice_engine = self.profile_settings.retrieve_property('voice_engine')
        self.data = self._load_in_voice_data()
              
    def _load_in_voice_data(self, file_path:str=None) -> dict:
        """
        Loads the settings from the appropriate file.
        """
        file_path = self._get_file_path(file_path)
        return self._open_file(file_path)
            
    def retrieve_custom_voice_id(self, voice_name:str) -> str:
        """
        Returns id associated with a given custom elevenlabs voice name
        """
        for custom_voice in self.data['custom']['english']:
            if voice_name in custom_voice:
                return custom_voice[voice_name]
            
    def retrieve_azure_voice_name(self, gender:str, voice_name:str) -> str:
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
        language_codes = list(data["language_country_codes"].keys())
        return language_codes
    
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
        if not file_path:
            if self.voice_engine == 'azure':
                file_path = azure_voice_settings_path
            elif self.voice_engine == 'elevenlabs':
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

