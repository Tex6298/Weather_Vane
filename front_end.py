import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data

from weatherVane import WeatherVane



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
@st.cache
def send_text_to_gpt3_to_parse(input):
    summary = gpt3_text_parser(input)
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
    try:
        summary = send_text_to_gpt3_to_parse(input)
    except Exception as e:
        st.sidebar.error("Something went wrong, please try again!\n These are the common causes of errors:\n - ")
        st.stop()

    # Show the summary
    st.header("📖 presentations Summary")
    st.write("This is a summary of what we think text is about:")
    st.markdown(summary)