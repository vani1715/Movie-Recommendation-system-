import streamlit as st
from main import recommend
import pickle

df=pickle.load(open('df.pkl','rb'))

st.markdown("""
<style>
body{
    background-color:#141414;
    color: white;
}
 h1{
     color: #E50914
}
</style>
""", unsafe_allow_html=True
)

st.title("Movie Recommendation System")

movie_name=st.text_input("Searh a movie")

if st.button("Recommend"):
    names,posters=recommend(movie_name)

    if not names:
        st.error("Movie not found. Try another name.")
    else:
        st.subheader("Recommended Movies")
        for i in range(0,10,5):
            cols=st.columns(5)
            for j in range(5):
                with cols[j]:
                    st.image(posters[i+j])
                    st.caption(names[i+j])


st.subheader("Trending Movies")
trending = df[(df['vote_count'] > 1000) & (df['vote_average'] > 6)].sort_values(by='popularity', ascending=False).head(10)

titles=trending['title'].tolist()

for i in range(0,len(titles),5):
    cols=st.columns(5)
    for j in range(5):
        if i+j<len(titles):
            with cols[j]:
                poster=fetch_poster(titles[i+j])
                st.image(poster)
                st.caption(titles[i+j])