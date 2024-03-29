import os
import yaml
import shutil
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager

profiles_path = f"src/customization/profiles/profile_storage"

class ProfileManager:
    
    def create_profile(self, config, profile_name) -> None:
        """
        Creates a new profile with a given name and config
        A directory is created with the given name and the config is saved in a settings.yaml file
        """
        self._make_profile_directory(config, profile_name)
        
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
        
        if property_name in ['name', 'gender', 'language', 'personality', 'persona', 'prompt', 'role']:
            return profile_data['entity'][property_name]
        if property_name in ['gpt_model', 'package', 'startup_sound', 'tts', 'voice_name', 'voice_recognition_engine']:
            return profile_data['system'][property_name]
        if property_name in ['user_name', 'user_gender']:
            if property_name == 'user_name':
                property_name = 'name'
            if property_name == 'user_gender':
                property_name = 'gender'
            return profile_data['user'][property_name]
        
    def save_property(self, property_name:str, property_value:str, profile_name=None) -> None:
        """
        Saves a given property to a given profile
        """
        if not profile_name:    
            profile_name = MasterSettingsManager().retrieve_property('profile')
            
        profile_data = self._load_profile_data(profile_name)
        
        if property_name in ['name', 'gender', 'language', 'personality', 'persona', 'prompt', 'role']:
            profile_data['entity'][property_name] = property_value
        if property_name in ['gpt_model', 'package', 'startup_sound', 'tts', 'voice_name', 'voice_recognition_engine']:
            profile_data['system'][property_name] = property_value
        if property_name in ['user_name', 'user_gender']:
            if property_name == 'user_name':
                property_name = 'name'
            if property_name == 'user_gender':
                property_name = 'gender'
            profile_data['user'][property_name] = property_value
            
        with open (os.path.join(profiles_path, profile_name, 'settings.yaml'), 'w') as file:
            yaml.dump(profile_data, file)
        
    def _make_profile_directory(self, config, profile_name) -> None:
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
                    yaml.dump(config, file)
                if file_name == "conversation_history.yaml":
                    yaml.dump({"conversation": []}, file)
                if file_name == "logs.yaml":  
                    yaml.dump({"log_sessions": []}, file)
                    
    def _load_profile_data(self, profile_name) -> dict:
        """
        Loads a profile with a given name
        """
        profile_settings_path = f"{profiles_path}/{profile_name}/settings.yaml"
        try:
            with open(profile_settings_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            return e 
