import streamlit as st
from src.customization.voices.voice_settings_manager import VoiceSettingsManager
from configuration.manage_secrets import ConfigurationManager
import requests

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
    st.title("Create a Custom Voice")

    st.write(
        """
        Upload a high-quality audio sample of a voice you would like cloned (A least 5-minutes of quality sample audio is recommended). After cloning is complete, update or create a profile that uses the new Elevenlabs voice name.
        """
    )

    voice_name = st.text_input("Enter a name for the new voice:")
    file = st.file_uploader("Upload a high-quality audio file (mp3 format) of the desired voice:", type=["mp3"])

    if voice_name and file:
        if st.button("Create Voice"):
            if create_custom_voice(voice_name, file):
                st.success(f"The voice '{voice_name}' has been successfully created!")
                VoiceSettingsManager().save_custom_voice(voice_name)
            else:
                st.error("An error occurred while creating the voice. Please try again later.")

def overview():
    st.title("Custom Voice Creation Overview")
    st.write("""
    Welcome to Juno's Custom Voice Creator!

    With this interface, you can:

    1. **Create Your Own Custom Voice**: Convert a high-quality audio sample into a voice that can be used by ElevenLabs' voice generation service.
    
    2. **Test Your Voice**: After successfully creating a custom voice, ensure it meets your expectations by testing it live.
    
    Start by uploading a clear, high-quality audio sample. This sample is essential to create a voice that is representative of the source. Ideally, the sample should be at least 5 minutes long for optimal results. After the cloning process, you can update or create a profile within Juno that uses the new ElevenLabs voice name.
    
    Dive in and craft your unique voice!
    """)

def test_voice():
    pass

def voice_cloning_interface():

    # Main Interface
    menu_functions = {
        "📘 About": overview,
        '🎓 Create Custom Voice': create_and_save_custom_voice,
        '✅ Test your Voice': test_voice
    }

    options = list(menu_functions.keys())
    activity = st.sidebar.selectbox("Select an Option", options)

    menu_functions[activity]()
