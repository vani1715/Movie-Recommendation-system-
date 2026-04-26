import os
import pickle
import requests
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()
API_KEY=os.getenv("API_KEY")

API_BASE="http://www.omdbapi.com/"
#API_IMG_500=
if not API_KEY:
    raise RuntimeError("API_KEY missing.put it in .env as API_KEY=xxxx")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

base_dir = os.path.dirname(os.path.abspath(__file__))

df = pickle.load(open(os.path.join(base_dir, "df.pkl"), "rb"))
tfidf_matrix = pickle.load(open(os.path.join(base_dir, "tfidf_matrix.pkl"), "rb"))
indices = pickle.load(open(os.path.join(base_dir, "indices.pkl"), "rb"))


def fetch_poster(title):
    try:
        url = f"{API_BASE}?t={title}&apikey={API_KEY}"
        data = requests.get(url).json()
        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"


def recommend(title):
    title = title.lower()

    if title not in indices:
        return [], []

    idx = indices[title]

    sim_scores = list(enumerate(cosine_similarity(tfidf_matrix[idx], tfidf_matrix)[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]

    movie_indices = [i[0] for i in sim_scores]

    names = df['title'].iloc[movie_indices].tolist()
    posters = [fetch_poster(m) for m in names]

    return names, posters