import streamlit as st
import os
import yaml
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.customization.profiles.profile_manager import ProfileManager
from configuration.manage_secrets import ConfigurationManager
from src.customization.voices.voice_settings_manager import VoiceSettingsManager
from usage.create_profile.create_new_profile import create_custom_profile

st.title("Profile Management")
st.write(
    """
    Use this interface to manage the profiles within your system. You can create, update, and delete profiles.
    """
)

# Initialize session state
if 'page_state' not in st.session_state:
    st.session_state.page_state = "default"


def load_in_profile_data():
    manager = ConfigurationManager()
    available_languages = VoiceSettingsManager().retrieve_available_languages()
    available_languages.sort()
    
    gpt_models = manager.retrieve_config_value('GPT-MODELS')

    directory_path = "src/customization/packages"
    available_packages = [None] + os.listdir(directory_path)
    
    available_voices = VoiceSettingsManager().retrieve_available_voices()
    
    return available_languages, gpt_models, available_packages, available_voices


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


def update_profile():
    all_profiles = os.listdir('src/customization/profiles/profile_storage')
    selected_profile = st.selectbox("Choose a Profile", all_profiles)

    with open(f'src/customization/profiles/profile_storage/{selected_profile.lower()}/settings.yaml', 'r') as file:
        profile = yaml.safe_load(file)

    display_and_edit_fields(profile)

    if st.button("Save Changes"):
        with open(f'src/customization/profiles/profile_storage/{selected_profile.lower()}/settings.yaml', 'w') as file:
            yaml.dump(profile, file, default_flow_style=False)
        st.success(f"{selected_profile} profile updated!")
        MasterSettingsManager().save_property('profile', selected_profile)


def create_profile():
    profile_name = st.text_input("Enter a Profile Name")
    with open(f'src/customization/profiles/profile_storage/default/settings.yaml', 'r') as file:
        profile = yaml.safe_load(file)

    display_and_edit_fields(profile)

    if st.button("Create New Profile"):
        create_custom_profile(config=profile, profile_name=profile_name)
        st.success(f"{profile_name} profile created!")
        MasterSettingsManager().save_property('profile', profile_name)


def remove_profile():
    all_profiles = os.listdir('src/customization/profiles/profile_storage')
    selected_profile = st.selectbox("Choose a Profile", all_profiles)

    if st.button("Delete Profile"):
        ProfileManager().remove_profile(profile_name=selected_profile)
        st.success(f"{selected_profile} profile deleted!")


# Main Interface
menu_functions = {
    'update_profile': update_profile,
    'create_profile': create_profile,
    'remove_profile': remove_profile
}

options = list(menu_functions.keys())
activity = st.sidebar.selectbox("Choose an Action", options)

menu_functions[activity]()
