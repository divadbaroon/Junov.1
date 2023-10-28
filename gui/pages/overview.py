import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# Convert the image to base64
def get_image_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

st.set_page_config(page_title="Overview")

def display_documentation():
    # Introduction
    st.write("""         
    ## What is Juno?       
    Juno is a platform to customize and interact with intelligent and adaptive virtual entities. It integrates leading AI technologies to deliver a customizable and responsive solution for a wide-range of use-cases.
    Juno utilizes packages, profiles, custom voices, and optional GPT fine-tuning to maximize its customization capabilities
    """)

    # Features Breakdown
    st.write("""
    ## Features Breakdown

    ### Packages
    **Packages** offer custom commands that define Juno's behavior. They act like plugins, enhancing its capabilities and allowing for specialization based on specific requirements.

    ### Profiles
    **Profiles** offer a unique twist to user experience. They allow the customization of Juno's behavior, tailoring interactions based on user preferences, tech stack, and specific traits.

    ### Voice Cloning
    With **Voice Cloning**, Juno can mimic any voice. This is possible with Elevenlabs technology, where a short audio clip can be used to generate a synthetic voice that sounds strikingly similar to the original.

    ### Fine-Tuning
    **Fine-tuning** ensures that Juno's responses are tailored for specific scenarios. By adjusting GPT-3.5-Turbo's output with specialized training data, users can ensure the AI's output matches their specific needs.

    """)

    # Conclusion
    st.write("""
    Together, these features make Juno a versatile and powerful conversational AI tool. For a deeper dive into each feature and detailed documentation, please refer to the main documentation.
    """)
    
def overview_interface():
    display_documentation()

