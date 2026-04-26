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
        url = "http://www.omdbapi.com/"
        params = {
            "t": title,
            "apikey": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(title):
    title = title.lower().strip()

    # find matching movies
    matches = [k for k in indices.keys() if title in k]

    if not matches:
        return [], []

    # pick best match (shortest distance / closest length)
    closest_title = min(matches, key=lambda x: abs(len(x) - len(title)))
    idx = indices[closest_title]

    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix)[0]))

    hybrid_scores = []

    for i, score in sim_scores:
        popularity = df.iloc[i]['popularity_norm'] if 'popularity_norm' in df.columns else 0
        hybrid_score = 0.7 * score + 0.3 * popularity
        hybrid_scores.append((i, hybrid_score))

    # sort by hybrid score
    hybrid_scores = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)[1:11]

    movie_indices = [i[0] for i in hybrid_scores]

    names = df['title'].iloc[movie_indices].tolist()
    posters = [fetch_poster(m) for m in names]

    return names, posters


def hybrid_recommend(title, alpha=0.7):
    title = title.lower()
    
    if title not in indices:
        return []
    
    idx = indices[title]
    
    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix)[0]))
    
    hybrid_scores = []
    
    for i, score in sim_scores:
        popularity = df.iloc[i]['popularity_norm']
        

        hybrid_score = alpha * score + (1 - alpha) * popularity
        
        hybrid_scores.append((i, hybrid_score))
    

    hybrid_scores = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    movie_indices = [i[0] for i in hybrid_scores]
    
    return df['title'].iloc[movie_indices].tolist()