import json
import os

# Get the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the bot_settings.json file in the 'voice' folder
bot_settings_path = os.path.join(current_directory, 'bot_settings.json')

class BotSettingsManager:
    """
    A class that can retrieve and save properties to "bot_settings.json".
    """
    def __init__(self):
        self.data = self.load_bot_settings()

    def load_bot_settings(self):
        """Loads the data from "bot_settings.json" and returns it as a dictionary."""
        try:
            with open(bot_settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "bot_settings.json" is missing.\nMake sure all files are located within the same folder.')
            raise SystemExit()

    def retrieve_property(self, setting: str):
        """Retrieves a property from "bot_settings.json" and returns it."""
        return self.data['chatbot'].get(setting)

    def save_property(self, setting: str, value: str):
        """Save a property to "bot_settings.json."""
        if setting not in ['mute_status', 'current_voice_name']:
            value = value.lower()
        self.data['chatbot'][setting] = value
        with open(bot_settings_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def reload_settings(self):
        """Reloads the data from "bot_settings.json" and stores it in self.data."""
        self.data = self.load_bot_settings()	