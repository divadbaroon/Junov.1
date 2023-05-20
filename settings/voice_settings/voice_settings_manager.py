import json
import os

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the bot_settings.json file in the 'voice' folder
voice_settings_path = os.path.join(current_directory, 'voice_settings.json')


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
        self.data = self.load_properties()
  
    def load_properties(self):
        """
        Loads the settings from "voice_settings.json" and saves them in the instance variable 'data'
        """ 
  
        # load data from "voice_settings.json"
        try:
            with open(voice_settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "voice_settings.json" is missing.\nMake sure all files are located within the same folder.')
            return {}

    def retrieve_property(self, setting):
        """
        Returns the desired setting from "voice_settings.json"
        :param setting (str): The setting to be retrieved
        """
        property_value = self.data.get(setting, None)
        if isinstance(property_value, dict):
            return list(property_value.keys())
        return property_value

    def get_language_country_code(self, language):
        """Gets the country code for the given language"""
        country_code = self.data['language_country_codes'].get(language)
        return country_code
