import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Function to download file from Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    # Handle large files with confirmation token
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# File setup
file_id = "1g1JFvCauvlYcF35mqbonBiBYQxn-Kxd3"  # Replace this with your actual file ID
filename = "similarity.pkl"

if not os.path.exists(filename):
    st.write("Downloading similarity matrix...")
    download_file_from_google_drive(file_id, filename)

# Load the similarity matrix
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

st.title("Movie Recommender System")
st.write("Similarity matrix loaded!")


# Your recommendation logic can go here...

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e48b26e8ff594e53767e26fba259d833&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w780/" + data['poster_path']

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


st.title('Movie Recommender System ')

selected_movie_name=st.selectbox(
    'Select a movie to recommend',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])