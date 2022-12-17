import openai
import requests

openai_api = "API"

openai.api_key = openai_api


# Template to parse input text and prepare for presentation
text_input_template = """
Inspect the following text:

{}

Identify key points and prepare the information in an ideal format so that it can be copied and pasted into a powerpoint
presentation, using bullet points if it becomes appropriate. The presentation should clearly introduce the subject, elaborate
key points and call out important conclusions.

"""


def gpt3_text_parser(input, temp=0.2):
  # Completion function call engine: text-davinci-003

    Platformresponse = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text_input_templatee.format(input),
        temperature=temp,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        )

    return Platformresponse.choices[0].text


def WeatherVane(input):
    """
    This function is the master WeatherVane! It does the following:
    (1) Take input text and parses it ready for presenting

    @param: input - Presentation topic text 
    """
    data = gpt3_text_parser(input)
    
    return data
