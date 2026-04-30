import streamlit as st
from main import recommend,fetch_poster
import pickle

df=pickle.load(open('df.pkl','rb'))

if "selected_movies" not in st.session_state:
    st.session_state.selected_movies=None

query_params = st.query_params
if "movie" in query_params:
    try:
        st.session_state.selected_movie = int(query_params["movie"])
    except:
        pass

st.markdown("""
<style>
body{
    background-color:#141414;
    color: white;
}
 h1{
     color: #E50914
}
img {
    border-radius: 10px;
    transition: 0.3s;
}
img:hover {
    transform: scale(1.05);
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True
)

st.title("Movie Recommendation System")

#movie_name=st.text_input("Search a movie")

if st.session_state.selected_movies is not None:
    movie=df.iloc[st.session_state.selected_movie]

    st.title(movie['title'])
    st.image(fetch_poster(movie['title']),width=300)

    st.subheader("Overview")
    st.write(movie.get('overview',"No description"))

    st.subheader("Rating")
    st.write(movie.get('vote_average',"N/A"))

    st.subheader("Genres")
    st.write(movie.get('genres',"N/A"))

    if st.button("Back"):
        st.session_state.selected_movie=None
        st.query_params.clear()

else:
    movie_name = st.text_input("Search a movie")
    if st.button("Recommend"):
        names, posters, descriptions, indices_list = recommend(movie_name)

        if not names:
            st.error("Movie not found. Try another name.")
        else:
            st.subheader("Recommended Movies")

            for i in range(0, len(names), 5):
                cols = st.columns(5)
                for j in range(5):
                    if i + j < len(names):
                        idx = i + j

                        with cols[j]:
                            st.markdown(f"""
                            <a href="?movie={indices_list[idx]}" style="text-decoration:none;">
                                <img src="{posters[idx]}" style="width:100%; border-radius:10px;">
                            </a>
                            """, unsafe_allow_html=True)

                            st.caption(names[idx])
                            st.write(descriptions[idx][:100] + "...")
    
    


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
                st.markdown(f"""
                <a href="?movie={trend_indices[idx]}" style="text-decoration:none;">
                    <img src="{fetch_poster(titles[idx])}" style="width:100%; border-radius:10px;">
                </a>
                """, unsafe_allow_html=True)

                st.caption(titles[idx])