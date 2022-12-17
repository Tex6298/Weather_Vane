import openai
import requests

from WeatherVane import gpt3_text_parser


class WeatherVane:
    def __init__(self, openai_api):
        openai.api_key = "openai_api"
        self.input = self.slide_summary_generator

    def slide_summary_generator(self):
        text = gpt3_text_parser(self.input)
        return text
