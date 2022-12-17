import altair as alt
import pandas as pd
import streamlit as st
import openai
from quick_start import *
from weatherVane import WeatherVane
import ast



# General helper functions

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""


def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

alt.themes.enable("streamlit")

st.set_page_config(
    page_title="WeatherVane", page_icon="⬇", layout="wide"
)

# -------------------------------------------------------------------------------------------------------------------

# -------------------------------------- FUNCTIONS ---------------------------------------------------------------------

slides = []
text_input_template = """
Inspect the following text:

{}

Identify key points and prepare the information in a python list of slides where each slide is appended as an item 
on the list slides = []. write the list on the same line. The presentation should clearly introduce the subject, elaborate
key points and call out important conclusions. Prepare the presentation with 12 slides with the conclusion on the 12th slide.
output should be a list of range(0,11) 
"""

@st.cache
def gpt3_text_parser(input, temp=0.0):
  # Completion function call engine: text-davinci-003

    Platformresponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text_input_template.format(input),
        temperature=temp,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )
    summary = Platformresponse.choices[0].text
    return summary


@st.cache
def gpt3_summary(input, temp=0.0):
  # Completion function call engine: text-davinci-003

    Platformresponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt="Compress this into words for DALL-E 2 prompt, make sure it will be allowed by the safety system : {}".format(input),
        temperature=temp,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )
    summary = Platformresponse.choices[0].text
    return summary

# -------------------------------------------------------------------------------------------------------------------


# ----------------------------------  MAIN PAGE ---------------------------------------------------------------------
st.title("WeatherVane")



# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------- SIDEBAR ---------------------------------------------------------------------
# Generate a sidebar for the streamlit app

st.sidebar.image(
    "images/weathervane4.jpg",
    width=200,
    use_column_width=True,
    output_format="jpg",
    caption="WeatherVane",
)

st.sidebar.text("v1.0.0")

st.sidebar.title("WeatherVane")
st.sidebar.markdown(
    """
    This is a web application for the Team WeatherVane project. The purpose of this app is to
    allow users to implement powerful presentations from data and prompts, streamlining the
    presentation of data utilising AI.
    """
)

st.sidebar.write("Insert presentation text below to get started!")
st.sidebar.info('An example', icon="ℹ️")

# Create a text box for the user to paste a YouTube URL
input = st.sidebar.text_input("Input text (Press Enter to apply)")

warning_text = """
This may take a couple of minutes, GPT-3 are working hard to do some crazy shiz! We are:\n
- 📹 Extracting the key points from the text
- 📈 Generating slide info
- 💵 
"""

if input != "":
    st.balloons()
    st.sidebar.warning(warning_text, icon="⏳")
    # ------------------------------ 1. Send URL to the BlueAgent and return the summary & code ------------------------------
    
    summary = gpt3_text_parser(input)
      
    
    presentation = create_presentation("test6ab9")
    summary = " ".join(line.strip() for line in summary.splitlines())
    
    # Show the summary
    st.header("📖 presentations Summary")
    st.write("Check your Google drive:")
    n= 0
    summary_list = eval(summary.split('slides = ')[1])
    
    for slide in summary_list:    
        page_id = f"page{n}"
        pres_id = presentation.get('presentationId')
        create_slide(pres_id, page_id, n)
        slide = gpt3_summary(slide)
        create_image(str(slide), pres_id, page_id)
        n += 1
