from fastapi import FastAPI, Form
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

df = pd.read_csv('df.csv')
movies = pd.read_csv('movies.csv')
links = pd.read_csv('links.csv')

# Model
csr_data = csr_matrix(df.values)
df.reset_index(inplace=True)

knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)

mov = movies['title']

def get_movie_recommendation(movie_name):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = df[df['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = df.iloc[val[0]]['movieId']
            idx = links[links['movieId'] == movie_idx].index
            recommend_frame.append(str(links.iloc[idx]['imdbId'].values[0]).zfill(7))
        return recommend_frame
    else:
        return "No movies found. Please check your input"



GenreMovies = pd.read_csv('GenreMovies.csv')
GenreRating = pd.read_csv('GenreRating.csv')
def getGenreRec(Genre_str : str):
    m = GenreMovies[GenreMovies[Genre_str] == 1]
    r = pd.merge(GenreRating, m, how='inner', on='movieId')
    ids = list(r[r['rating'] == 5]['movieId'].value_counts().head(10).index)
    imId = []
    for i in ids:
        imId.append(str(links[links['movieId'] == i]['imdbId'].values[0]).zfill(7))
    return imId

#API
app = FastAPI()

@app.post('/')
def main():
    return {'Welcome to Movie Reccomendation System!'}


@app.get('/search_result/{mov}')
async def get_reccomendations(mov):
    return get_movie_recommendation(mov)

@app.get('/new_user/{genre}')
async def getGenre(genre):
    return getGenreRec(genre)


