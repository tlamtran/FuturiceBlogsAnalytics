# 'streamlit run ./src/occurrences_demo.py' in src folder
import pandas as pd
import spacy
import streamlit as st
from nltk.stem.porter import *


@st.cache_data
def load_data():
    # python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')

    names = ['Accenture', 'Futurice', 'Tietoevry']
    paths = ['data/processed/stemmed/accenture.csv', 'data/processed/stemmed/futurice.csv',
             'data/processed/stemmed/tietoevry.csv']

    dfs = []
    for i in range(len(names)):
        df = pd.read_csv(paths[i])

        df.name = names[i]
        df['date'] = pd.to_datetime(df['date'])
        dfs.append(df)
    return nlp, names, dfs


def run_app():
    stemmer = PorterStemmer()
    nlp, names, data = load_data()

    option = st.text_input('Enter a search term, e.g. Generative AI, Virtual Reality or Metaverse')
    stemmed_box = st.checkbox('Use stemmed words', value=False)

    agg_df = []
    for i in range(len(data)):
        df = data[i]
        if stemmed_box:
            df = df[df['stemmed'].str.contains(rf"\b{' '.join(stemmer.stem(str(w)) for w in nlp(option))}\b",
                                               regex=True,
                                               na=False)]
        else:
            df = df[df['text'].str.lower().str.contains(rf'\b{option.strip().lower()}\b', regex=True, na=False)]

        s: pd.Series = df.groupby(pd.Grouper(key='date', freq='1M')).count()['text']
        s.name = names[i]
        agg_df.append(s)

    df = pd.concat(agg_df, axis=1)
    st.line_chart(df)
