import json
from comic_generation.generate_panels import generate_panels
from comic_generation.stability_ai import text_to_image
from comic_generation.add_text import add_text_to_panel
from comic_generation.create_strip import create_strip
import streamlit as st
from PIL import Image

api_key = st.secrets["OPENAI_API_KEY"]
stability_api_key=st.secrets["STABILITY_KEY"]

if api_key is None:
    raise ValueError(
        "OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

favicon = Image.open("favicon.png")


st.set_page_config(
    page_title="GenAI Demo | Trigent AXLR8 Labs",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

logo_html = """
<style>
    [data-testid="stSidebarNav"] {
        background-image: url(https://trigent.com/wp-content/uploads/Trigent_Axlr8_Labs.png);
        background-repeat: no-repeat;
        background-position: 20px 20px;
        background-size: 80%;
    }
</style>
"""
st.sidebar.markdown(logo_html, unsafe_allow_html=True)
st.title("Provide your story and wait for your comic. 😀")

if api_key:
    success_message_html = """
    <span style='color:green; font-weight:bold;'>✅ Powering the Chatbot using Open AI's 
    <a href='https://platform.openai.com/docs/models/gpt-3-5' target='_blank'>gpt-3.5-turbo-0613 model</a>!</span>
    """

    # Display the success message with the link
    st.markdown(success_message_html, unsafe_allow_html=True)
    openai_api_key = api_key
else:
    openai_api_key = st.text_input(
        'Enter your OPENAI_API_KEY: ', type='password')
    if not openai_api_key:
        st.warning('Please, enter your OPENAI_API_KEY', icon='⚠️')
        stop = True
    else:
        st.success('Get your comic ready in minutes!', icon='👉')


SCENARIO = st.text_area(
    "Enter your Story and the characters",
    """Characters: A IT industry Manager named Andy and Couple of Software developers with a Laptop.
The manager is a super guy who manages all his Developers.
Once there was a super powerful task which the  manager  assigned to on of his new developers and the developer was able to do it and the Manager was amazed and awarded him with a USA ticket.""",
)

STYLE = st.text_input("Enter the style of your characters", "Indian comic, coloured")
if st.button("Generate"):
    with st.spinner("Making a comic for you..."):
        print(f"Generate panels with style '{STYLE}' for this scenario: \n {SCENARIO}")

        panels = generate_panels(SCENARIO)

        with open("output/panels.json", "w") as outfile:
            json.dump(panels, outfile)

        panel_images = []

        for panel in panels:
            panel_prompt = panel["description"] + ", cartoon box, " + STYLE
            textData = f"Generate panel {panel['number']} with prompt: {panel_prompt}"
            st.markdown(textData)
            panel_image = text_to_image(panel_prompt)
            panel_image_with_text = add_text_to_panel(panel["text"], panel_image)
            panel_images.append(panel_image_with_text)

        res = create_strip(panel_images)
        st.image(res)



# Footer
footer_html = """
<div style="text-align: right; margin-right: 10%;">
    <p>
        Copyright © 2024, Trigent Software, Inc. All rights reserved. | 
        <a href="https://www.facebook.com/TrigentSoftware/" target="_blank">Facebook</a> |
        <a href="https://www.linkedin.com/company/trigent-software/" target="_blank">LinkedIn</a> |
        <a href="https://www.twitter.com/trigentsoftware/" target="_blank">Twitter</a> |
        <a href="https://www.youtube.com/channel/UCNhAbLhnkeVvV6MBFUZ8hOw" target="_blank">YouTube</a>
    </p>
</div>
"""

# Custom CSS to make the footer sticky
footer_css = """
<style>
.footer {
    position: fixed;
    z-index: 1000;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
}
</style>
"""


footer = f"{footer_css}<div class='footer'>{footer_html}</div>"

# Rendering the footer
st.markdown(footer, unsafe_allow_html=True)
