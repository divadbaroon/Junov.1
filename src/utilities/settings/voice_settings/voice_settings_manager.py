import json
import os
from customization.profiles.profile_manager import ProfileManager

# Construct the path to the master_settings.json file in the 'voice_settings' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
azure_voice_settings_path = os.path.join(current_directory, 'azure_voice_settings.json')
elevenlabs_voice_settings_path = os.path.join(current_directory, 'elevenlabs_voice_settings.json')

class VoiceSettingsManager:
    """
    A class that can retrieve and save properties from either "azure_voice_settings.json" 
    or "elevenlabs_voice_settings.json". Data is loaded from the "voice_settings.json" when 
    the class is instantiated. The user can then retrieve or save properties from the file.
    """
 
    def __init__(self):
        """
        Instantiates the class and loads the data from either "azure_voice_settings.json" or "elevenlabs_voice_settings.json"
        """
        self.profile_settings = ProfileManager()
        self.voice_engine = self.profile_settings.retrieve_property('voice_engine')
        self.data = self.load_voice_settings()
              
    def load_voice_settings(self, file_path:str=None):
        """
        Loads the settings from the appropriate file.
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
                        
    def retrieve_voice_name(self, gender:str, index:int=0) -> str:
        """
        Returns a voice name associated with a specified
        gender and language
        """
        voice_name = self.retrieve_voice_names(gender)
        voice_name = list(voice_name.keys()) 
        return voice_name[0]
             
    def retrieve_voice_names(self, gender:str) -> list:
        """
        Returns all voice names associated with a specified 
        gender and language
        """
        if gender == 'female':
            voice_names = self.data["female_voices"]
        if gender == 'male':
            voice_names = self.data["male_voices"]
        return voice_names
    
    def retrieve_azure_voice_name(self, voice_name:str) -> str:
        """
        Returns the Azure voice name assocaited with a given voice name.
        For example, the arg Amber would return en-US-AmberNeural
        """
        # return voice name in its appropriate format 
        if voice_name in self.data['female_voices']:
                return self.data['female_voices'][voice_name]
        elif voice_name in self.data['male_voices']:
                return self.data['male_voices'][voice_name]
    
    def available_languages(self) -> list:
        """
        Retrieves all of the available languages 
        """
        data = self.load_voice_settings(azure_voice_settings_path)
        language_codes = list(data["language_country_codes"].keys())
        return language_codes
    
    def retrieve_language_code(self, language:str) -> str:
        """
        Retrieves the language code associated with a specified language
        """
        # method is only applicable for azure text-to-speech engine
        data = self.load_voice_settings(azure_voice_settings_path)
        language_codes = data["language_codes"].get(language)
        return language_codes
        
    def retrieve_language_country_code(self, language:str) -> str:
        """
        Gets the country code for the given language
        """
        # method is only applicable for azure text-to-speech engine
        data = self.load_voice_settings(azure_voice_settings_path)
        country_codes = data['language_country_codes'].get(language)
        return country_codes
    