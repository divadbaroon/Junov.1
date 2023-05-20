import json
import os

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)

# Construct the path to the bot_settings.json file in the 'voice' folder
voice_settings_path = os.path.join(parent_directory, 'voice', 'bot_settings.json')


class BotSettingsManager:
    """
    A class that can retrieve and save properties in "bot_settings.json".
    Data is loaded from the "bot_settings.json" when the class is instantiated.
    The user can then retrieve or save properties from the file.
    """
    def __init__(self):
        self.data = self.load_properties()

    def load_properties(self):
        try:
            with open(voice_settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "bot_settings.json" is missing.\nMake sure all files are located within the same folder.')
            raise SystemExit()

    def get_voice_name(self, single_voice=False):
        gender = self.data['chatbot'].get('gender')
        language = self.data['chatbot'].get('language')
        voice_name = self.data[f'{gender}_voices'].get(language)
        if single_voice and isinstance(voice_name, list):
            return voice_name[0]
        return voice_name

    def retrieve_property(self, setting: str):
        if setting == 'voice_names':
            return self.get_voice_name()
        if setting == 'voice_name':
            return self.get_voice_name(single_voice=True)
        elif setting in ('languages', 'female_voices', 'male_voices'):
            return list(self.data[setting].keys())
        elif setting == 'language_codes':
            return self.data[setting]
        elif setting == 'bot_settings':
            return self.data['chatbot']
        else:
            return self.data['chatbot'].get(setting)

    def save_property(self, setting: str, value):
        self.data['chatbot'][setting] = value.lower() if isinstance(value, str) else value
        with open(voice_settings_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_language_country_code(self, language: str) -> str:
        return self.data['language_country_codes'].get(language)

    def reload_settings(self):
        self.data = self.load_properties()	
