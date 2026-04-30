import streamlit as st
from main import recommend,fetch_poster
import pickle

df=pickle.load(open('df.pkl','rb'))

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie=None

if "expanded_desc" not in st.session_state:
    st.session_state.expanded_desc = {}

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

st.markdown("""
<style>
 @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
*{
            font-family:'Montserrat', sans-serif !important;
            }
body, .stApp{
    background-color: #111318 !important;
    color: #E8E8E8 !important;
}
 h1{
    color: #FF2B4E !important;
    letter-spacing: 2px;
    font-weight: 700 !important;
    text-transform: uppercase;
}
h2, h3 {
    color: #F0A500 !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
}
.stSubheader {
    border-left: 3px solid #F0A500;
    padding-left: 8px;
}
.stTextInput > div > div > input {
    background-color: #1E2028 !important;
    color: #E8E8E8 !important;
    border: 1px solid #2E3140 !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #FF2B4E !important;
    box-shadow: 0 0 0 2px rgba(255,43,78,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #FF2B4E, #C0003C) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    transition: opacity 0.2s ease, transform 0.1s ease !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: scale(0.97) !important;
}
img {
    border-radius: 10px;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
img:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 24px rgba(255, 43, 78, 0.35);
    cursor: pointer;
}
.movie-title {
    text-align: center;
    font-weight: 600;
    margin-top: 6px;
    color: #3dc1db;
}
.stCaption {
    color: #A0A0B0 !important;
    font-size: 0.78rem !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True
)

st.title("Movie Recommendation System")

#movie_name=st.text_input("Search a movie")

if st.session_state.selected_movie is not None:
    movie=df.iloc[st.session_state.selected_movie]

    st.title(movie['title'])
    st.image(fetch_poster(movie['title']),width=300)

    st.subheader("Overview")
    st.write(movie.get('overview',"No description"))

    st.subheader("Rating")
    st.write(movie.get('vote_average',"N/A"))

    st.subheader("Genres")
    st.write(movie.get('genres',"N/A"))

    if st.button("⬅ Back"):
        st.session_state.selected_movie=None
        

else:
    movie_name = st.text_input("Search a movie")
    if st.button("Recommend"):
        names, posters, descriptions, indices_list = recommend(movie_name)

        if not names:
            st.error("Movie not found. Try another name.")
            st.session_state.recommendations = None
        else:
            st.session_state.recommendations = {
                "names": names,
                "posters": posters,
                "descriptions": descriptions,
                "indices_list": indices_list,
            }
            st.session_state.expanded_desc = {}
    if st.session_state.recommendations is not None:
        rec = st.session_state.recommendations
        names = rec["names"]
        posters = rec["posters"]
        descriptions = rec["descriptions"]
        indices_list = rec["indices_list"]
            
        st.subheader("Recommended Movies")
        for i in range(0, len(names), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(names):
                        idx = i + j
                        movie_key = f"rec_{indices_list[idx]}"

                        with cols[j]:
                            st.image(posters[idx], use_container_width=True)
                            st.caption(names[idx])

                            desc = descriptions[idx]
                            is_expanded = st.session_state.expanded_desc.get(movie_key, False)

                            if is_expanded:
                                st.write(desc)
                                if st.button("View Less ▲", key=f"less_{movie_key}"):
                                    st.session_state.expanded_desc[movie_key] = False
                                    st.rerun()
                            else:
                                st.write(desc[:50] + "...")
                                if st.button("View More ▼", key=f"more_{movie_key}"):
                                    st.session_state.expanded_desc[movie_key] = True
                                    st.rerun()
    
    
st.subheader("Trending Movies")
trending = df[
        (df['vote_count'] > 500) &
        (df['vote_average'] > 6)
    ].sort_values(by='popularity', ascending=False).head(10)

titles = trending['title'].tolist()
trend_indices = trending.index.tolist()

for i in range(0, len(titles), 5):
    cols = st.columns(5)
    for j in range(5):
        if i + j < len(titles):
            idx = i + j

            with cols[j]:
                st.image(fetch_poster(titles[idx]), use_container_width=True)
                st.caption(titles[idx])