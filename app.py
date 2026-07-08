import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open("movie_data.pkl", "rb") as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    if title not in movies['title'].values:
        return pd.DataFrame()
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

API_KEY = "e95e519c"

def fetch_poster(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        return data["Poster"]
    else:
        return "https://via.placeholder.com/300x450?text=No+Poster"
# Streamlit UI
# ---------------- LOGIN ----------------

user_history = pd.read_csv("user_history.csv")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='text-align:center;color:#E50914;'>
    🎬 MOVIEFLIX
    </h1>

    <h3 style='text-align:center;'>
    Welcome to MovieFLIX
    </h3>

    <p style='text-align:center;'>
    Login to discover movies recommended just for you.
    </p>
    """, unsafe_allow_html=True)

    username = st.text_input("👤 Username")
    if username == "Select Username":
        st.warning("Please select a username.")
        st.stop()
    password = st.text_input(
            "🔒 Password",
            type="password"
        )

    if st.button("🔐 Login", use_container_width=True):

            user = user_history[
                (user_history["userName"].str.lower() == username.lower()) &
                (user_history["password"] == password)
            ]

            if not user.empty:

                st.session_state.logged_in = True
                st.session_state.user_name = username
                st.session_state.user_id = int(user.iloc[0]["userId"])

                st.rerun()

            else:
                st.error("❌ Invalid Username or Password")

    st.stop()
# ---------------- HOME PAGE ----------------

st.markdown(f"""
<h1 style='text-align:center;color:#E50914;'>
🎬 MOVIEFLIX
</h1>

<h3 style='text-align:center;'>
Welcome, {st.session_state.user_name}! 🍿
</h3>

<p style='text-align:center;'>
Choose a movie and let MovieFLIX recommend similar movies using AI.
</p>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🎥 Select a Movie",
    ["🎬 Select a Movie"] + sorted(movies["title"].tolist())
)

if selected_movie == "🎬 Select a Movie":
    st.warning("Please select a movie.")
    st.stop()

if st.button("🎥 Recommend Movies", use_container_width=True):
    recommendations = get_recommendations(selected_movie)

    st.write("Top 10 recommended movies:")

    for i in range(0, len(recommendations), 5):
        cols = st.columns(5)

        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                poster_url = fetch_poster(movie_title)
                search_url = f"https://www.google.com/search?q={movie_title.replace(' ', '+')}+watch"

                with col:
                    st.markdown("""
<style>

.movie-card{
    background:#1b1b1b;
    border-radius:12px;
    padding:10px;
    transition:all 0.3s ease;
    cursor:pointer;
}

.movie-card:hover{
    transform:translateY(-8px) scale(1.05);
    box-shadow:0px 10px 25px rgba(229,9,20,0.8);
}

.movie-card img{
    width:100%;
    border-radius:12px;
}

.movie-title{
    color:white;
    text-align:center;
    font-weight:bold;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <a href="{search_url}" target="_blank" style="text-decoration:none;">
                            <div class="movie-card">
                                <img src="{poster_url}" style="width:100%; border-radius:12px;">
                                <div class="movie-title">
                                    <b>{movie_title}</b><br>
                                    ⭐ AI Recommended
                                </div>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)



                       


