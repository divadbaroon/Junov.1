import streamlit as st

def overview():
    st.write(""" 
    # Packages Overview 📦
    
    Packages empower Juno by providing specialized command recognition and appropriate responses to user queries. 
    These commands are trained using data located within the `/training` directory. This training ensures that 
    the Azure CLU model can accurately detect and execute the intended commands. Dive into the `/training` directory
    to explore more about the training process.
    """)

def create_a_package():
    st.write(""" 
    ## TODO
    """) 
    
def display_package_table(title, data):
    st.markdown(f"## {title}")
    for section, commands in data.items():
        st.markdown(f"#### {section}")
        st.table(commands)

def basic_package():
    
    st.write(""" 
    ## Basic Package       
                      
    #### Control Behavior
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Mute  | I am now muted | Mutes responses | 
    | Unmute | I am not unmuted | Unmutes responses |
    | Pause | Pausing |  Pauses functionalities |
    | Unpause | Unpaused |  Resumes functionalities |
    | Exit | Exiting, goodbye! |  Terminates program |
    #### Personalization
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Change your language to {language} | Changing language to {language} | Changes language |
    | Change your gender to {gender} | Changing gender to {gender} | Changes gender |
    | Change your persona to {role} | Changing persona to {persona} | Changes persona |
    | Change voice | I have changed my voice | Changes voice |
    """)

def virtual_assistant_package():
    
    st.write(""" 
    ## Virtual Assistant Package       
                      
    #### Weather Retrieval
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | What is the weather in {location} | The weather in {location} is {temperature} degrees. | Fetches temperature via OpenWeatherMap API |
    #### Speech Translation
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Translate {speech} into {language} | {translated_speech} |  Uses Azure for speech translation |
    #### Control Lights
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Turn lights {off/on} | None | Controls smart LED lights |
    | Change light color to {color} | None | Changes light color |
    #### Control Music 
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Play {song} | None |  Plays song via Spotify API |
    | Pause song | None |  Pauses song via Spotify API |
    | Play next song | None |  Plays next song via Spotify API |
    | Lower volume | None | Decreases volume by 10% |
    | Raise volume | None | Increases volume by 10% |
    #### Set Alarm
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Set an alarm for {day and time} | Setting an alarm for {day and time} | Sets an alarm |
    #### Set Reminder
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Set a reminder for {day and time} to do {reminder} | Setting a reminder | Sets a reminder for {day and time} to do {reminder} |
    #### Set Timer
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Set a timer for {time} {metric} | Setting a timer for {time} {metric} | Sets a timer |
    #### News Retrieval 
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Give me the news | Sure here is what's going on in the world. {Gives a summary of the top 3 news articles (using a fine-tuned GPT-3.5-turbo model | Fetches top news headlines via News API |
    #### Web Browsing
    | Input | Response | Action |
    | ------- | -------- | -------- |
    | Open {website} | Opening {website} |  Opens website |
    | Search {speech} | Searching for {speech} |  Google search |
    | Search youtube for {speech} | Searching Youtube for {speech} | Searches YouTube |
    """)

def package_interface():

    # Main Interface
    menu_functions = {
        "Overview": overview,
        'Create Package': create_a_package,
        'Basic Package': basic_package,
        'Virtual Assistant Package': virtual_assistant_package
    }

    st.sidebar.title("Juno Package Guide")
    st.sidebar.markdown("Explore the world of Juno packages and discover their power.")
    options = list(menu_functions.keys())
    activity = st.sidebar.selectbox("🔍 Choose an Option", options)

    menu_functions[activity]()
