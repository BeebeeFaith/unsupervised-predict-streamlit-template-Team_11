"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""


# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import pickle


from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import requests

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model


######################
#Load model
movies_dict = pickle.load(open('/Users/fbarde/Desktop/+Explore AI/Movie_recommendation_system-main/Streamlit_config/movies_dicti.pkl' , 'rb' ))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('/Users/fbarde/Desktop/+Explore AI/Movie_recommendation_system-main/Streamlit_config/similarity_matrix.pkl' , 'rb'))


##########################
 #Page Title
st.set_page_config(page_title="CENTAURI", page_icon='frog')

########## main body container ####################
#page background

page_bg_img ="""
<style>
      .stApp {
  background-image: url("https://images.unsplash.com/photo-1604147706283-d7119b5b822c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=80");
  background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


######################


# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview","About"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    
    #------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("AI Powered Search Engine ")
        
        def crew(movie_id):
            response = requests.get(
                "https://api.themoviedb.org/3/movie/{0}/credits?api_key=4158f8d4403c843543d3dc953f225d77&language=en-US".format(
                    movie_id))
            data = response.json()
            crew_name = []
            final_cast = []
            k = 0
            for i in data["cast"]:
                if(k!=6):
                    crew_name.append(i['name'])
                    final_cast.append("https://image.tmdb.org/t/p/w500/" + i['profile_path'])
                    k+=1
                else:
                    break
            return crew_name , final_cast
    
    
    
        def date(movie_id):
            response = requests.get(
                "https://api.themoviedb.org/3/movie/{}?api_key=4158f8d4403c843543d3dc953f225d77&language=en-US".format(
                    movie_id))
            data = response.json()
            return data['release_date']
        
    
        def genres(movie_id):
            response = requests.get(
                "https://api.themoviedb.org/3/movie/{}?api_key=4158f8d4403c843543d3dc953f225d77&language=en-US".format(
                    movie_id))
            data = response.json()
            return data['genres']
        
        def overview(movie_id):
            response = requests.get(
                "https://api.themoviedb.org/3/movie/{}?api_key=4158f8d4403c843543d3dc953f225d77&language=en-US".format(
                    movie_id))
            data = response.json()
            return data['overview']
        def poster(movie_id):
            response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=4158f8d4403c843543d3dc953f225d77&language=en-US".format(movie_id))
            data = response.json()
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        
        def recommend(movie):
            movie_index = movies[movies['title'] == movie].index[0]
            cosine_angles = similarity[movie_index]
            recommended_movies = sorted(list(enumerate(cosine_angles)), reverse=True, key=lambda x: x[1])[0:7]
        
        
            final = []
            final_posters = []
            final_name , final_cast = crew(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
            gen = genres(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
            overview_final = overview(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
            rel_date = date(movies.iloc[movies[movies['title'] == movie].index[0]].movie_id)
            for i in recommended_movies:
        
                final.append(movies.iloc[i[0]].title)
                final_posters.append(poster(movies.iloc[i[0]].movie_id))
            return final_name , final_cast , rel_date , gen , overview_final , final , final_posters
        
        
        
            st.title('Movie Recommendation System')
        
        selected_movie = st.selectbox(
            'Which Movie Do you like?',
             movies['title'].values)
        
        
        
        def process(genre):
            final = []
            for i in genre:
                final.append(i['name'])
        
            return final
        
        if st.button('Search'):
            name , cast , rel_date , gen , overview_final , ans , posters = recommend(selected_movie)
        
            st.header(selected_movie)
            col_1 , col_2 = st.columns(2)
        
        
            with col_1:
                st.image(posters[0] , width=  325 , use_column_width= 325)
        
            with col_2:
                st.write("Title : {} ".format(ans[0]))
        
                st.write("Overview : {} ".format(overview_final))
                gen = process(gen)
                gen = " , ".join(gen)
                st.write("Genres : {}".format(gen))
                st.write("Release Date {} : {} ".format(" " , rel_date))
        
        
            st.title("Top Casts")
        
            c1 , c2 , c3 = st.columns(3)
            with c1:
                st.image(cast[0] , width=  225 , use_column_width= 225)
                st.caption(name[0])
            with c2:
                st.image(cast[1] , width=  225 , use_column_width= 225)
                st.caption(name[1])
            with c3:
                st.image(cast[2], width=  225 , use_column_width= 225)
                st.caption(name[2])
        
        
            c1 , c2 ,c3 = st.columns(3)
            with c1:
                st.image(cast[3], width=  225 , use_column_width= 225)
                st.caption(name[3])
        
            with c2:
                st.image(cast[4], width=  225 , use_column_width= 225)
                st.caption(name[4])
        
            with c3:
                st.image(cast[5], width=225, use_column_width=225)
                st.caption(name[5])
        
        
            st.title("")
        
            st.title("   Similar Movies You May Like")
        
            c1, c2, c3 = st.columns(3)
            with c1:
                st.image(posters[1], width=225, use_column_width=225)
                st.write(ans[1])
            with c2:
                st.image( posters[2], width=225, use_column_width=225)
                st.write(ans[2])
            with c3:
                st.image(posters[3], width=225, use_column_width=225)
                st.write(ans[3])
        
            c1, c2, c3 = st.columns(3)
            with c1:
                st.image(posters[4], width=225, use_column_width=225)
                st.write(ans[4])
        
            with c2:
                st.image(posters[5], width=225, use_column_width=225)
                st.write(ans[5])
        
            with c3:
                st.image(posters[6], width=225, use_column_width=225)
                st.write(ans[6])
    
    
    
    
    
    #--------------------------------------------------------------
    if page_selection == "About":
        st.info(
            "Discover Alpha Centauri Analytica :frog:"
        )
        st.markdown(
            """
                                    Welcome to Centauri! 
            
            We provide an AI-driven Recommendation System that uses machine learning and deep learning algorithms to recommend the best movie in real-time to you.
"""
) 
        st.info("Meet The Team!")
        from PIL import Image
        with st.container():
            image = Image.open("/Users/fbarde/Downloads/cent2.png")
            st.image(image, use_column_width=True) 


if __name__ == '__main__':
    main()
