import streamlit as st
from src.customization.voices.voice_settings_manager import VoiceSettingsManager
from configuration.manage_secrets import ConfigurationManager
import requests

st.title("Upload Audio for Custom Voice Creation")

st.write(
    """
    Juno and ElevenLabs give you the capability to create custom voices. 
    Upload a high-quality audio sample and we'll work to generate a unique voice model for you.
    """
)

def create_custom_voice(voice_name, file):
    """
    Creates a custom voice using the ElevenLabs API.
    """
    api_keys = ConfigurationManager().retrieve_api_keys()

    url = "https://api.elevenlabs.io/v1/voices/add"
    headers = {
        "Accept": "application/json",
        "xi-api-key": api_keys['ELEVENLABS-API-KEY']
    }
    data = {
        'name': voice_name,
        'labels': '{"accent": "American"}',
        'description': 'Voice created using Juno platform'
    }
    files = {
        'files': (file.name, file.getvalue(), 'audio/mpeg')
    }

    response = requests.post(url, headers=headers, data=data, files=files)
    return response.status_code == 200

def create_and_save_custom_voice():
    """
    Interface to create and save a custom voice.
    """
    voice_name = st.text_input("Enter a name for the new voice:")
    file = st.file_uploader("Upload a high-quality audio file (mp3 format) of the desired voice:", type=["mp3"])

    if voice_name and file:
        if st.button("Create Voice"):
            if create_custom_voice(voice_name, file):
                st.success(f"The voice '{voice_name}' has been successfully created!")
                VoiceSettingsManager().save_custom_voice(voice_name)
            else:
                st.error("An error occurred while creating the voice. Please try again later.")

create_and_save_custom_voice()
