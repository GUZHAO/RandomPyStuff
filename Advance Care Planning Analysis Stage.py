# Load requisite packages
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
import numpy as np
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import string
from operator import is_not
from functools import partial
from wordcloud import WordCloud
from collections import Counter
import re
import nltk
from nltk.stem.porter import PorterStemmer
import matplotlib.pyplot as plt

# nltk.download('punkt')
plotly.tools.set_credentials_file(username='GUZHAO', api_key='yKp3gPHe80DscNZTfHOl')

'''Manipulate Data'''
data_df = pd.read_json('C:/Users/gz056/Downloads/acp.json')
# Get a list of headers
print(list(data_df))
# Remove any null value
df_clean = data_df \
    # .dropna(axis=1, how='any')
# Sort data by question number
df_sorted = df_clean.sort_values(by='SER_ILL', ascending=True)
# Get the number of row
df_num = df_sorted.shape[0]

# Frequency Table on questions answered
x = df_sorted['SER_ILL_DISPLAY']
trace = go.Histogram(x=x, xbins=dict(start=np.min(x), size=0.25, end=np.max(x)),
                     marker=dict(color='rgb(0, 0, 100)'))

layout = go.Layout(
    title="Histogram Frequency Counts"
)

fig = go.Figure(data=go.Data([trace]), layout=layout)
py.iplot(fig, filename='histogram-freq-counts')

# System q2 q3 and q4 values for reference
q2_phrase = ['live as long as possible',
             'be comfortable',
             'be mentally aware',
             'de independent',
             'be at home',
             'achieve goal',
             'provide support for family']

q3_phrase = ['pain',
             'other physical suffering',
             'inability to care for others',
             'loss of control',
             'finances',
             'being a burden']

q4_phrase = ['curable',
             'incurable',
             'days - weeks',
             'weeks - months',
             'months - years',
             'a few years',
             'continued decline',
             'not discussed']


def tokenize_phrase(text):
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if len(w) > 2]
    return tokens


def phrase_pic(q_name, pic_name):
    df_q_value = df_sorted.loc[df_sorted['SER_ILL'] == q_name]['SER_ILL_CONV'].values
    df_q_value_rn = filter(partial(is_not, None), df_q_value)
    q_text = [word.replace(" ", "") for word in df_q_value_rn]
    df_q_value_join = " ".join(q_text)
    q_ctr = Counter(tokenize_phrase(df_q_value_join))

    # cloud for words
    wordcloud = WordCloud(width=800, height=400)
    wordcloud.fit_words(q_ctr)

    fig = plt.figure(figsize=(5, 3))  # Prepare a plot 5x3 inches
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("C:/Users/gz056/Downloads/" + pic_name + ".png", dpi=800)


phrase_pic('R PHS AMB SICG QUESTION 2', pic_name="q2")
phrase_pic('R PHS AMB SICG QUESTION 3', pic_name="q3")
phrase_pic('R PHS AMB SICG PROGNOSIS', pic_name="q4")


def tokenize(text):
    text = text.lower()
    text = re.sub('[' + string.punctuation + '0-9\\r\\t\\n]', ' ', text)
    tokens = nltk.word_tokenize(text)
    tokens = [w for w in tokens if len(w) > 2]
    tokens = [w for w in tokens if w not in ENGLISH_STOP_WORDS]
    return tokens


def stemwords(words):
    stemmer = PorterStemmer()
    words = [stemmer.stem(w) for w in words]  # stem words
    return words


def phrase_comm(qc_name, c_name, pic_name):
    df_qc_value = df_sorted.loc[df_sorted['SER_ILL'] == qc_name][c_name].values
    df_qc_value_rn = filter(partial(is_not, None), df_qc_value)
    df_q_value_join = " ".join(df_qc_value_rn)
    qc_ctr = Counter(tokenize(df_q_value_join))
    # cloud for words
    wordcloud = WordCloud(width=800, height=400)
    wordcloud.fit_words(qc_ctr)

    fig = plt.figure(figsize=(5, 3))  # Prepare a plot 5x3 inches
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("C:/Users/gz056/Downloads/" + pic_name + ".png", dpi=800)


phrase_comm('R PHS AMB SICG QUESTION 2', 'SER_ILL_CONV_COMM', 'q2_comm')
phrase_comm('R PHS AMB SICG QUESTION 3', 'SER_ILL_CONV_COMM', 'q3_comm')
phrase_comm('R PHS AMB SICG PROGNOSIS', 'SER_ILL_CONV_COMM', 'q4_comm')
phrase_comm('R PHS AMB SICG QUESTION 1', 'SER_ILL_CONV', 'q1')
phrase_comm('R PHS AMB SICG QUESTION 5', 'SER_ILL_CONV', 'q5')
phrase_comm('R PHS AMB SICG QUESTION 6', 'SER_ILL_CONV', 'q6')
phrase_comm('R PHS AMB SICG QUESTION 1', 'SER_ILL_CONV_COMM', 'q1_comm')
phrase_comm('R PHS AMB SICG QUESTION 5', 'SER_ILL_CONV_COMM', 'q5_comm')
phrase_comm('R PHS AMB SICG QUESTION 6', 'SER_ILL_CONV_COMM', 'q6_comm')
