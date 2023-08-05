import json
import os

# Construct the path to the master_settings.json file in the 'master_settings' folder
current_directory = os.path.dirname(os.path.abspath(__file__))
master_settings_path = os.path.join(current_directory, 'master_settings.json')

class MasterSettingsManager:
    """
    A class that can retrieve and save properties to "master_settings.json".
    """
    def __init__(self):
        self.data = self.load_master_settings_data()

    def load_master_settings_data(self) -> dict:
        """Loads the data from "master_settings.json" and returns it as a dictionary."""
        try:
            with open(master_settings_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f'The file "{master_settings_path}" is missing.')
            raise SystemExit()

    def retrieve_property(self, setting: str, subsetting:str = None) -> str:
        """Retrieves a property from "master_settings.json" and returns it."""
        if subsetting:
            return self.data['settings'].get(setting).get(subsetting)
        else:
            return self.data['settings'].get(setting)
            
    def retrieve_properties(self) -> dict:
        """Retrieves all properties from "master_settings.json" and returns them."""
        return self.data['settings']

    def save_property(self, setting: str, value: str, subsetting:str = None) -> None:
        """Save a property to "master_settings.json."""
        if subsetting:
            self.data['settings'][setting][subsetting] = value
        else:
            self.data['settings'][setting] = value
            
        # write data back
        with open(master_settings_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def reload_settings(self) -> None:
        """Reloads the data from "master_settings.json" and stores it in self.data."""
        self.data = self.load_master_settings_data()	
        