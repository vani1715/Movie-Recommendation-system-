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
trending=df.sort_values(by='vote_average',ascending=False).head(10)

for i in range(0,10,5):
    cols=st.columns(5)
    for j in range(5):
        with cols[j]:
            st.caption(trending.iloc[i+j]['title'])