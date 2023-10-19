import yaml
from src.customization.profiles.profile_manager import ProfileManager
 
def create_custom_profile():
    """
    Create and save a custom profile to be used by Juno
    """
    
    # open file located within /profiles/profile_storage/defualt/settings.yaml
    with open ('usage/create_profile/example_profile.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        
    # Creates and saves profiles
    ProfileManager().create_profile(config=config, profile_name='obama') 
    
    # To see profiles 
    #print(ProfileManager().load_profile_data())
    
    # delete profiles
    # ProfileManager().remove_profile(profile_name='time_traveler') 
    
create_custom_profile()