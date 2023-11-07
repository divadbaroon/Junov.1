import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import os
from src.juno import Juno
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager

# import pages
from gui.pages.overview import overview_interface
from gui.pages.profiles import profile_interaface
from gui.pages.packages import package_interface
from gui.pages.voice_cloning import voice_cloning_interface
from gui.pages.fine_tuning import fine_tuning_interface

def juno():
    
    all_profiles = os.listdir('src/customization/profiles/profile_storage')
    selected_profile = st.sidebar.selectbox("Choose a Profile", all_profiles)
    
    # Initialize session states if not already set
    if 'chat_started' not in st.session_state:
        st.session_state.chat_started = False
        
    col1, col2 = st.sidebar.columns(2) 
    with col1:
        if st.button("Begin Session"):
            st.session_state.chat_started = True 
    with col2:
        if st.button("Reset Session"):
            st.session_state.chat_started = False
        
    if not st.session_state.chat_started:
        img_path = 'gui/logo.png'
        img = Image.open(img_path)
        st.image(img, use_column_width=True)

    elif st.session_state.chat_started:
        st.title('Conversation History:')
        MasterSettingsManager().save_property("profile", selected_profile)
        MasterSettingsManager().save_property("functions", True, "gui")
        new_session = Juno()
        new_session.run()
        st.session_state.chat_started = False
        
def main_interface():
    
    # Create a select box for page navigation
    page = st.sidebar.selectbox("Choose a page", ["Juno", "Overview", "Profiles", "Packages", "Voice Cloning", "Fine Tuning"])

    # Display content for selected page
    if page == "Juno":
        juno()
    elif page == "Overview":
        overview_interface()
    elif page == "Profiles":
        profile_interaface()
    elif page == "Packages":
        package_interface()
    elif page == "Voice Cloning":
        voice_cloning_interface()  
    elif page == "Fine Tuning":
        fine_tuning_interface()
