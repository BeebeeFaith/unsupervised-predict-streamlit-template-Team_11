import streamlit as st
import pickle
import pandas as pd
import requests




##########################
 #Page Title
st.set_page_config(page_title="FROG", page_icon='frog')

########## main body container ####################
#page background

page_bg_img ="""
<style>
      .stApp {
  background-image: url("https://images.unsplash.com/photo-1543955946-8d33e764d8f2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1740&q=80");
  background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)




###################################################

#Side bar










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



movies_dict = pickle.load(open('/Users/fbarde/Desktop/+Explore AI/Movie_recommendation_system-main/Streamlit_config/movies_dicti.pkl' , 'rb' ))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('/Users/fbarde/Desktop/+Explore AI/Movie_recommendation_system-main/Streamlit_config/similarity_matrix.pkl' , 'rb'))
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



#########################################
def main():
    
    
    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Search Engine","About"]



