import os
import pickle
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

import streamlit as st

API_KEY = st.secrets["API_KEY"]

API_BASE="http://www.omdbapi.com/"
#API_IMG_500=
if not API_KEY:
    raise RuntimeError("API_KEY missing.put it in .env as API_KEY=xxxx")

print(API_KEY)


base_dir = os.path.dirname(os.path.abspath(__file__))

df = pickle.load(open(os.path.join(base_dir, "df.pkl"), "rb"))
tfidf_matrix = pickle.load(open(os.path.join(base_dir, "tfidf_matrix.pkl"), "rb"))
indices = pickle.load(open(os.path.join(base_dir, "indices.pkl"), "rb"))

indices = {k.lower(): v for k, v in indices.items()}

def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
        data = requests.get(url).json()

        poster = data.get("Poster")

        if poster and poster != "N/A":
            return poster
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(title):
    title = title.lower()
    #matches = [movie for movie in indices.keys() if title in movie]

    matches = [k for k in indices.keys() if title in k]

    if not matches:
        return [], []

    idx = indices[matches[0]]

    #closest_title = matches[0]
    #idx = indices[closest_title]

    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix)[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

    movie_indices = [i[0] for i in sim_scores]

    names = df['title'].iloc[movie_indices].tolist()
    posters = [fetch_poster(m) for m in names]

    return names, posters