import streamlit as st
import base64
from io import BytesIO
from PIL import Image

# Convert the image to base64
def get_image_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

st.set_page_config(page_title="Juno")

# Custom CSS to style the title and align the image next to it
st.markdown(
    """
    <style>
        .title-container {
            font-size: 10em;
            font-weight: bold;
            display: flex;
            align-items: center;
            padding: 1rem 0;
        }
        .title-container img {
            margin-left: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the image
img_path = 'src/utilities/juno_logo.png'
img = Image.open(img_path)
img_base64 = get_image_base64(img)

# Display the title and image side by side
st.markdown(
    f'''
    <div class="title-container">
        <div>Juno</div>
        <img src="data:image/png;base64,{img_base64}" width="170">
    </div>
    ''', 
    unsafe_allow_html=True
)

def _display_documentation():
    # Introduction
    st.write("""
    ## Overview

    Juno, a cutting-edge conversational AI, allows users to build, train, and deploy personalized and adaptive virtual entities. It integrates leading AI technologies to deliver a customizable and responsive solution for diverse applications.
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

_display_documentation()
