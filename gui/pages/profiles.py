import streamlit as st
import os
import yaml
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.customization.profiles.profile_manager import ProfileManager
from configuration.manage_secrets import ConfigurationManager
from src.customization.voices.voice_settings_manager import VoiceSettingsManager
from usage.create_profile.create_new_profile import create_custom_profile

# Initialize session state
if 'page_state' not in st.session_state:
    st.session_state.page_state = "default"

def load_in_profile_data():
    manager = ConfigurationManager()
    available_languages = VoiceSettingsManager().retrieve_available_languages()
    
    all_gpt_models = []

    gpt_models = manager.retrieve_config_value('GPT-MODELS')

    for model in gpt_models:
        if isinstance(model, dict):
            all_gpt_models.extend(model.keys())
        else:
            all_gpt_models.append(model)


    directory_path = "src/customization/packages"
    available_packages = [None] + os.listdir(directory_path)
    
    available_voices = VoiceSettingsManager().retrieve_available_voices()
    
    return available_languages, all_gpt_models, available_packages, available_voices

def display_sorted_fields(profile_dict, parent_key=""):
    available_language, all_gpt_models, available_packages, available_voices = load_in_profile_data()

    for key, value in profile_dict.items():
        unique_key = f"{parent_key}_{key}"

        display_map = {
            'gender': (["Male", "Female"], "Gender"),
            'language': (available_language, "Language"),
            'gpt_model': (all_gpt_models, "GPT Model"),
            'package': (available_packages, "Package"),
            'startup_sound': ([True, False], "Startup Sound"),
            'tts': (["Azure", "Elevenlabs"], "TTS Engine"),
            'voice_name': (available_voices, "Voice Name"),
            'voice_recognition_engine': (['Azure'], "Voice Recognition Engine")
        }

        if key.lower() in display_map:
            options, label = display_map[key.lower()]

            # Move the current value to the front of the list
            if value in options:
                options.remove(value)
                options.insert(0, value)

            profile_dict[key] = st.selectbox(label, options, key=f"selectbox_{unique_key}")
        elif isinstance(value, dict):
            st.subheader(key.capitalize())
            display_and_edit_fields(value, unique_key)
        else:
            profile_dict[key] = st.text_input(key.capitalize(), value, key=f"textinput_{unique_key}")

def display_and_edit_fields(profile_dict, parent_key=""):
    available_language, gpt_models, available_packages, available_voices = load_in_profile_data()
    
    for key, value in profile_dict.items():
        unique_key = f"{parent_key}_{key}"

        display_map = {
            'gender': (["Male", "Female"], "Gender"),
            'language': (available_language, "Language"),
            'gpt_model': (gpt_models, "GPT Model"),
            'package': (available_packages, "Package"),
            'startup_sound': ([True, False], "Startup Sound"),
            'tts': (["Azure", "Elevenlabs"], "TTS Engine"),
            'voice_name': (available_voices, "Voice Name"),
            'voice_recognition_engine': (['Azure'], "Voice Recognition Engine")
        }

        if key.lower() in display_map:
            options, label = display_map[key.lower()]
            profile_dict[key] = st.selectbox(label, options, key=f"selectbox_{unique_key}")
        elif isinstance(value, dict):
            st.subheader(key.capitalize())
            display_and_edit_fields(value, unique_key)
        else:
            profile_dict[key] = st.text_input(key.capitalize(), value, key=f"textinput_{unique_key}")
            
def display_and_edit_fields2(profile_dict, parent_key=""):
    available_language, gpt_models, available_packages, available_voices = load_in_profile_data()
    
    for key, value in profile_dict.items():
        unique_key = f"{parent_key}_{key}"

        display_map = {
            'gender': (["Male", "Female"], "Gender"),
            'language': (available_language, "Language"),
            'gpt_model': (gpt_models, "GPT Model"),
            'package': (available_packages, "Package"),
            'startup_sound': ([True, False], "Startup Sound"),
            'tts': (["Azure", "Elevenlabs"], "TTS"),
            'voice_name': (available_voices, "Voice Name"),
            'voice_recognition_engine': (['Azure'], "Voice Recognition Engine")
        }

        if key.lower() in display_map:
            options, label = display_map[key.lower()]
            profile_dict[key] = st.selectbox(label, options, key=f"selectbox_{unique_key}")
        elif isinstance(value, dict):
            st.subheader(key.capitalize())
            display_and_edit_fields(value, unique_key)
        else:
            profile_dict[key] = st.text_input(key.capitalize(), value, key=f"textinput_{unique_key}")
            
    return profile_dict

def read_values_from_fields(profile_dict, parent_key=""):
    # The structure here is similar to display_and_edit_fields
    # but instead of setting the widgets, we'll read values from them.
    
    for key, value in profile_dict.items():
        unique_key = f"{parent_key}_{key}"
        
        # For fields that were presented as selectboxes:
        if key.lower() in ['gender', 'language', 'gpt_model', 'package', 'startup_sound', 'tts', 'voice_name', 'voice_recognition_engine']:
            profile_dict[key] = st.session_state.get(f"selectbox_{unique_key}")
        
        # For nested dictionary structures, recursively read their values:
        elif isinstance(value, dict):
            read_values_from_fields(value, unique_key)
            
        # For fields that were presented as text inputs:
        else:
            profile_dict[key] = st.session_state.get(f"textinput_{unique_key}")

    return profile_dict
            
def overview():
    
    # Introduction
    st.write("""         
    ## What are Profiles?       
    Profiles allow you to customize the behavior of Juno, shaping its interactions based on specific users, technologies, and desired persona traits.
    """)

    # Features Breakdown
    st.write("""
    ### The following attribute make up a profile:

    ## Entity Attributes
    | Attribute  | Example Value  | Description |
    | :--------- | :------------ | :---------- |
    | `name`     | barack obama  | The name of the entity |
    | `gender`   | male          | Gender of the entity |
    | `language` | english       | Language entity speaks in (Refer to documentation for available languages) |
    | `personality` | friendly   | Describes the overall temperament of the entity |
    | `persona`  | barack obama  | The entity will act as if they are this persona |
    | `prompt`   | you are an assistant designed to concisely help the user with their queries | Prompt used to query GPT |
    | `role`     | assistant     | Role of the entity |
    
    ## System Attributes
    | Attribute               | Example Value   | Description |
    | :----------------------- | :-------------- | :---------- |
    | `gpt_model`              | gpt-3.5-turbo   | Model used for generating responses (Fine-tuning recommended. See /training) |
    | `package`                | virtual_assistant | Optional package for added functionalities. See [packages](#packages) for more information |
    | `startup_sound`          | true           | Whether to play a startup sound |
    | `voice_name`             | barack obama   | Voice used for text-to-speech. In this example, I am using a custom-made voice modeled after Barack Obama, created using Elevenlabs |
    | `text_to_speech_engine`  | elevenlabs     | Engine used for text-to-speech (e.g., Elevenlabs or Azure) |
    | `voice_recognition_engine` | azure        | Engine used for voice recognition |
    
    ## User Attributes
    | Attribute   | Example Value | Description |
    | :----------- | :------------ | :---------- |
    | `user_name`  | james          | Name of the user interacting with the entity |
    | `user_gender`| male         | Gender of the user |
    | `user_age`   | 22          | Age of the user |

    """)
            

def view_profile():
    
    st.title("View a Profile")
    st.write(
        """
        Use this interface to select and view/update a preexisting profile.
        """
    )
    
    all_profiles = os.listdir('src/customization/profiles/profile_storage')
    selected_profile = st.selectbox("Choose a Profile", all_profiles)

    with open(f'src/customization/profiles/profile_storage/{selected_profile.lower()}/settings.yaml', 'r') as file:
        profile = yaml.safe_load(file)

    display_sorted_fields(profile)

    if st.button("Save Changes"):
        with open(f'src/customization/profiles/profile_storage/{selected_profile.lower()}/settings.yaml', 'w') as file:
            yaml.dump(profile, file, default_flow_style=False)
        st.success(f"{selected_profile} has been updated!")
        MasterSettingsManager().save_property('profile', selected_profile)
        
def create_profile():
    st.title("Create a Profile")
    st.write("""
        Use this interface to create a new profile.
    """)
    
    profile_name = st.text_input("Enter a Profile Name")
    profile_name = profile_name.replace(' ', '_')
    
    # load default profile 
    with open(f'src/customization/profiles/profile_storage/default/settings.yaml', 'r') as file:
        profile = yaml.safe_load(file)

    display_and_edit_fields2(profile)

    if st.button("Create New Profile"):
        config = read_values_from_fields(profile)

        create_custom_profile(config=config, profile_name=profile_name)
        st.success(f"{profile_name} profile created!")
        MasterSettingsManager().save_property('profile', profile_name)

def remove_profile():
    
    st.title("Remove a Profile")
    st.write(
        """
        Use this interface to remove a preexisting profile.
        """)
    all_profiles = os.listdir('src/customization/profiles/profile_storage')
    selected_profile = st.selectbox("Choose a Profile", all_profiles)

    if st.button("Delete Profile"):
        if selected_profile != 'default':
            ProfileManager().remove_profile(profile_name=selected_profile)
            MasterSettingsManager().save_property('profile', 'default')
            st.success(f"{selected_profile} profile deleted!")
        else:
            st.error('Cannot delete deflt profile.')
            
def profile_interaface():
            
    # Main Interface
    menu_functions = {
        "Overview": overview,
        'View Profile': view_profile,
        'Create Profile': create_profile,
        'Remove Profile': remove_profile
    }

    options = list(menu_functions.keys())
    activity = st.sidebar.selectbox("Select an Option", options)

    menu_functions[activity]()