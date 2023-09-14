import os
import requests
import openai
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential
from langchain.llms import AzureOpenAI

# WARNING: BE CAREFUL NOT TO LEAK THE API KEY
# Create .env file in project root folder and copy the API_KEY and API_BASE from 1Password there.
load_dotenv()
openai.api_key = os.getenv('API_KEY')
openai.api_base = os.getenv('API_BASE')
openai.api_type = 'azure'
openai.api_version = '2023-05-15'

def get_azure_openai():
    llm = AzureOpenAI(
        openai_api_type="azure",
        openai_api_version="2023-05-15",
        deployment_name="gpt-35-turbo",
        openai_api_base=os.getenv('API_BASE'),
        openai_api_key=os.getenv('API_KEY')
    )
    return llm

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text) -> list[float]:
    return openai.Embedding.create(input=[text], engine='text-embedding-ada-002')["data"][0]["embedding"]

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def generate_text(personality, prompt, temperature=1):
    response = openai.ChatCompletion.create(
        engine='gpt-35-turbo',
        temperature=temperature,
        messages=[
            {"role": "system", "content":personality},
            {"role": "user", "content":prompt}
        ]
    )
    return response['choices'][0]['message']['content']