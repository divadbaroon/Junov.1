import json
import os

# Construct the path to the bot_settings.json file in the 'bot_settings' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
bot_settings_path = os.path.join(current_directory, 'bot_settings.json')

class BotSettingsManager:
    """
    A class that can retrieve and save properties to "bot_settings.json".
    """
    def __init__(self):
        self.data = self.load_bot_settings()

    def load_bot_settings(self) -> dict:
        """Loads the data from "bot_settings.json" and returns it as a dictionary."""
        try:
            with open(bot_settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print('The file "bot_settings.json" is missing.\nMake sure all files are located within the same folder.')
            raise SystemExit()

    def retrieve_property(self, setting: str, subsetting:str = None) -> str:
        """Retrieves a property from "bot_settings.json" and returns it."""
        if subsetting:
            return self.data['bot'].get(setting).get(subsetting)
        else:
            return self.data['bot'].get(setting)
            
    def retrieve_properties(self) -> dict:
        """Retrieves all properties from "bot_settings.json" and returns them."""
        return self.data['bot']

    def save_property(self, setting: str, value: str, subsetting:str = None) -> None:
        """Save a property to "bot_settings.json."""
        if subsetting:
            self.data['bot'][setting][subsetting] = value
        else:
            self.data['bot'][setting] = value
        # write data back
        with open(bot_settings_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def reload_settings(self) -> None:
        """Reloads the data from "bot_settings.json" and stores it in self.data."""
        self.data = self.load_bot_settings()	