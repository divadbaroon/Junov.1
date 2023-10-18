import os
import yaml
import shutil
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager

current_directory = os.path.dirname(os.path.abspath(__file__))
profiles_path = os.path.join(current_directory, 'profile_storage')

class ProfileManager:
    
    def create_profile(self, profile_name, config) -> None:
        """
        Creates a new profile with a given name and config
        A directory is created with the given name and the config is saved in a settings.yaml file
        """
        self._make_profile_directory(profile_name, config)
        
    def remove_profile(self, profile_name) -> None:
        """
        Removes a profile with a given name
        """
        profile_path = f'{profiles_path}/{profile_name}'
        try:
            # Delete the directory associated with the profile
            shutil.rmtree(profile_path)
        except  FileNotFoundError:
            return
    
    def retrieve_property(self, property_name:str, profile_name='default') -> str:
        """
        Gets a given property from a given profile
        """
        if not profile_name:    
            profile_name = MasterSettingsManager().retrieve_property('profile')
            
        profile_data = self._load_profile_data(profile_name)
        
        if property_name in ['personality', 'prompt', 'role', 'language']:
            return profile_data['interaction'][property_name]
        if property_name in ['startup_sound', 'voice_recognition_engine', 'voice_engine', 'voice_name', 'package']:
            return profile_data['system'][property_name]
        if property_name in ['gender', 'name']:
            return profile_data['user'][property_name]
        
    def save_property(self, property_name:str, property_value:str, profile_name=None) -> None:
        """
        Saves a given property to a given profile
        """
        if not profile_name:    
            profile_name = MasterSettingsManager().retrieve_property('profile')
            
        profile_data = self.load_profile_data(profile_name)
        
        if property_name in ['personality', 'prompt', 'role', 'language']:
            profile_data['interaction'][property_name] = property_value
        if property_name in ['startup_sound', 'voice_recognition_engine', 'voice_engine', 'voice_name', 'package']:
            profile_data['system'][property_name] = property_value
        if property_name in ['gender', 'name']:
            profile_data['user'][property_name] = property_value
            
        with open (os.path.join('customization', 'personalization', 'profiles', 'profile_storage', profile_name, 'settings.yaml'), 'w') as file:
            yaml.dump(profile_data, file)
        
    def _make_profile_directory(self, profile_name, config) -> None:
        """
        Creates a directory with the given name and creates a settings.yaml, conversation_history.yaml, and logs.yaml file within the directory
        """
        directory_name = f'{profiles_path}/{profile_name}'
        
        # Create a new directory with the profile's name
        os.makedirs(directory_name, exist_ok=True)
        
        file_names = ["settings.yaml", "conversation_history.yaml", "logs.yaml"]
        
        # Create files in the directory
        for file_name in file_names:
            with open(os.path.join(directory_name, file_name), 'w') as file:
                if file_name == "settings.yaml":
                    formatted_config = self._format_config_data(config)
                    yaml.dump(formatted_config, file)
                if file_name == "conversation_history.yaml":
                    yaml.dump({"conversation": []}, file)
                if file_name == "logs.yaml":  
                    yaml.dump({"log_sessions": []}, file)
                    
    def _load_profile_data(self, profile_name) -> dict:
        """
        Loads a profile with a given name
        """
        profile_path = f'{profiles_path}/{profile_name}/settings.yaml'
        try:
            with open(profile_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return 

    def _format_config_data(self, config) -> dict:
        """
        Formats the config to be saved in the settings.yaml file
        """
        return {
            'user': {
                'name': config.get('name', 'Juno'),
                'gender': config.get('gender', 'female')
            },
            'system': {
                'startup_sound': config.get('startup_sound', False),
                'voice_engine': config.get('voice_engine', 'azure'),
                'voice_name': config.get('voice_name', 'Ana'),
                'package': config.get('package', None)
            },
            'interaction': {
                'role': config.get('role', None),
                'prompt': config.get('prompt', "you are a virtual assistant"),
                'personality': config.get('personality', 'friendly'),
                'language': config.get('language', 'english')
            }
        }
