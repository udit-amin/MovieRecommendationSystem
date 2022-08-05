import streamlit as st
import requests

url = "https://online-movie-database.p.rapidapi.com/title/get-details"

headers = {
	"X-RapidAPI-Host": "online-movie-database.p.rapidapi.com",
	"X-RapidAPI-Key": "57af18c6abmsh1c18d495e14117ep18d665jsndd40f049163f"
}

st.title('Movie Recommender')
st.image("images.png")
st.header ("Find Based on Genre")
genre = str(st.selectbox("Select Genre", options=['Action', 'Adventure' , 'Animation' , 'Childrens' , 'Comedy' , 'Crime' , 'Documentary' , 'Drama' , 'Fantasy' , 'Film-Noir' , 'Horror' , 'Musical' , 'Mystery' , 'Romance' , 'Sci-Fi' , 'Thriller' , 'War' , 'Western']))
if st.button('Find Movies'):
    response2 = requests.get(f"http://127.0.0.1:8000/new_user/{genre}").json()
    respList2 = list(response2)
    for i in range(10):
        querystring = {"tconst":"tt" + str(respList2[i])}

        response2 = requests.request("GET", url, headers=headers, params=querystring).json()
        try:
            imgUrl = response2.get("image").get("url")
            title = response2.get("title")
            st.image(imgUrl, width = 200)
            st.write(title+"\n")
        except:
            st.write("Unable to get Poster :(")

st.header("\n\nOR\n\n")

st.header ("Find Movies similar to your All-Time Favourites!")
mov = str(st.text_input("Enter Movie Name"))


if st.button("Find Movies!"):
    st.write(f"Showing Result for {mov}: ")
    response = requests.get(f"http://127.0.0.1:8000/search_result/{mov}").json()
    respList = list(response)
    for i in range(10):

        querystring = {"tconst":"tt" + str(respList[i])}

        response1 = requests.request("GET", url, headers=headers, params=querystring).json()
        try:
            imgUrl = response1.get("image").get("url")
            title = response1.get("title")
            st.image(imgUrl, width = 200)
            st.write(title+"\n")
        except:
            st.write("Unable to get Poster :(")
        