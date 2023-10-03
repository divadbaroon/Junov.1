import yaml
from profiles.profile_manager import ProfileManager
 
def create_custom_profile():
    """
    Create and save a custom profile to be used by Juno
    """
    
    # open file located within /profiles/profile_storage/defualt/settings.yaml
    with open ('profiles/profile_storage/default/settings.yaml', 'r') as file:
        default_config = yaml.load(file, Loader=yaml.FullLoader)
        
    # Creates and saves profiles
    ProfileManager().create_profile(config=default_config ) 
    
    # To see profiles 
    #print(ProfileManager().load_profile_data())
    
    # delete profiles
    # ProfileManager().remove_profile(profile_name='time_traveler') 
    
create_custom_profile()