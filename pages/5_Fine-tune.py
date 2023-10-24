import streamlit as st
from training.begin_gpt_training_session import OpenAIFineTuningJob
from src.utilities.settings.master_settings.master_settings_manager import MasterSettingsManager
from src.customization.profiles.profile_manager import ProfileManager

st.title("Fine-Tuning GPT-4 with Juno")

# Check if page_state is already initialized
if 'page_state' not in st.session_state:
    st.session_state.page_state = "default"

def fine_tune_GPT():
    """
    Initiates the fine-tuning process for the GPT model.
    """
    st.subheader("Start Fine-Tuning")
    model_name = st.text_input("Enter a name for your fine-tuned GPT model")
    file = st.file_uploader("Upload your training data (.jsonl format)", type=["jsonl"])
    
    if st.button("Begin Training"):
        if model_name and file:
            OpenAIFineTuningJob().start_finetuning(model_name=model_name, file=file)
            st.success("Training started successfully!")
            st.info("You'll receive an email shortly from OpenAI with your job ID. Once received, you can use the 'Add Fine-Tuned GPT Model' button to integrate your new model into Juno.")
        else:
            st.warning("Please provide both a model name and upload the training data to proceed.")

def add_model_to_juno():
    """
    Integrates a fine-tuned GPT model into Juno.
    """
    st.subheader("Integrate Your Fine-Tuned Model with Juno")
    model_name = st.text_input("Enter the job ID received from OpenAI:")

    if st.button("Integrate Model"):
        profile_name = MasterSettingsManager().retrieve_property('profile')
        ProfileManager().save_property('gpt_model', model_name, profile_name)
        st.success(f"Model {model_name} added to Juno!")

# Main interface logic
st.write("Fine-tuning GPT-4 can make it more suited to your specific tasks, enhancing its performance and accuracy.")

# Sidebar options
options = st.sidebar.radio("Choose an Action:", ["Main Menu", "Train a New Model", "Integrate Model with Juno"])

if options == "Train a New Model":
    fine_tune_GPT()

if options == "Integrate Model with Juno":
    add_model_to_juno()
