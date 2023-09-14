import os

import pandas as pd
import numpy as np
import scipy.stats as stats

from langchain.embeddings import HuggingFaceBgeEmbeddings
from openai_functions import generate_text
from dotenv import load_dotenv

model_name = "BAAI/bge-large-en-v1.5"
model_kwargs = {'device':'cpu'}
encode_kwargs = {'normalize_embeddings':True} # True for cosine similarity
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
)

def get_cdf_value_total_users(total_users):
    normal_distribution = stats.norm(138.68688845401175, 401.4369149410682)
    return normal_distribution.cdf(total_users)

def get_cdf_value_avg_session_time(avg_session_time):
    normal_distribution = stats.norm(119.10314145544227, 109.39267698309507)
    return normal_distribution.cdf(avg_session_time)

def get_topics(text):
    prompt = f"Given the following blog text “{text}” extract at most 5 important key topics, summarized into either 2 or 3 words for each key topic. Write it out as a python list and don't return anything else."
    topics = generate_text(prompt, temperature=0)
    return topics

def get_gpt_blog_title_and_target_audience(title_field, target_audience_field):
    personality = "You are an expert at writing software tech related blogs for an software consultancy company. You know what is trendy and relevant in the tech world"
    prompt = f"""
    Come up with pairs of title and target audience, also explain why you chose them. Here is what I have so far (don't modify if exists):
    title: {title_field}
    target audience: {target_audience_field}
    """
    tips = generate_text(personality, prompt, temperature=1)
    return tips

def get_gpt_intro_paragraph(title_field, target_audience_field):
    personality = "You are an expert at writing software tech related blogs for an IT consultancy company. You know how to write interesting intros"
    prompt = f"""
    Suggest intro paragraph given these guidelines:
    - max 500 characters
    - summarizes what your blog post is all about
    - make a great first impression and catch the reader’s attention
    - encourage people to keep reading it
    - one paragraph
    - prefer around 3 sentences
    - avoid excessive repetition

    Also here's the title and target audience:
    - title: {title_field}
    - target audience: {target_audience_field}
    """
    intro_suggestion = generate_text(personality, prompt, temperature=1)
    return intro_suggestion

def get_gpt_blog_body_text(previously_suggested_intro):
    personality = "You are an expert at writing software tech related blogs for an IT consultancy company. You know how to write blogs that keep your readers. Use markdown"
    prompt = f"""
    Continue from my intro paragraph following these guidelines, don't include title and intro paragraph in your text:
    - add subheadings and nested subheadings to bring in more structure
    - deliver your messsage accordingly since readers’ time is limited
    - marketing campaign related blogs have 4000 to 6000 characters otherwise no limits

    Also here's my intro paragraph:
    '{previously_suggested_intro}'
    """
    body_text_suggestion = generate_text(personality, prompt, temperature=1)
    return body_text_suggestion

def get_gpt_tips(title_field, target_audience_field, intro_field, body_field):
    personality = "You are an expert at writing blogs for an IT consultancy company."
    prompt = f"""
    Give fair tips and feedback on the blog below, such as how to improve, what is missing from the target audiences perspective, etc:
    
    title: '{title_field}'
    target audience: '{target_audience_field}'
    intro paragraph: '{intro_field}'
    body: '{body_field}'
    """
    suggestions = generate_text(personality, prompt, temperature=0.5)
    return suggestions


def rewrite(prompt, text):
    personality = "You are an expert at writing software tech related blogs for an IT consultancy company. You know how to fix and improve blogs"
    prompt = f"""
    Rewrite the text below given this instruction '{prompt}':
    '{text}'
    """
    rewritten_text = generate_text(personality, prompt, temperature=0.2)
    return rewritten_text


def get_similar_blogs(title):
    df = pd.read_csv('data/processed/futurice/blogs2.csv')
    df = df[df['title'] != title]
    embedded_text = model.embed_query(title)
    df['similarity'] = df['bge embedded title'].apply(eval).apply(lambda x: np.dot(x, embedded_text))
    df = df[df['similarity'] >= 0.7]
    df = df.sort_values(by='similarity', ascending=False)

    return df

def get_similar_blogs_competitors(title):
    df = pd.read_csv('data/processed/competitors/blogs.csv')
    embedded_title = model.embed_query(title)
    df['similarity'] = df['bge'].apply(eval).apply(lambda x: np.dot(x, embedded_title))
    df = df[df['similarity'] >= 0.72]
    df = df.sort_values(by='similarity', ascending=False)

    return df