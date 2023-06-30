'''########################################################################################
    Carga de Librerias
'''########################################################################################

import numpy as np
import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

'''########################################################################################
    Funciones del Programa
'''########################################################################################
def mes_a_numero(mes):
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
    mes_lower = mes.lower()
    if mes_lower in meses:
        return meses[mes_lower]
    else:
        return None

def dia_a_numero(dia):
    dias = {
        'lunes': 0,
        'martes': 1,
        'miercoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sabado': 5,
        'domingo': 6
    }
    dia_lower = dia.lower()
    if dia_lower in dias:
        return int(dias[dia_lower])
    else:
        return None
    

def get_recommendations(movie_title, similarity_matrix, movies_df, top_n=5):
    # Obtener el índice de la película de referencia
    indices = movies_df[movies_df['title'] == movie_title].index

    if len(indices) == 0:
        return{"message": 'No se encuentra la Pelicula'} 

    idx = indices[0]  # Obtener el primer índice coincidente

    # Obtener los puntajes de similitud de la película de referencia con todas las demás películas
    similarity_scores = list(enumerate(similarity_matrix[idx]))

    # Ordenar las películas por su puntaje de similitud en orden descendente
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de las películas más similares
    top_indices = [score[0] for score in similarity_scores[1:top_n+1]]

    # Obtener los títulos de las películas más similares
    top_movies = movies_df.iloc[top_indices]['title'].tolist()

    return top_movies

'''########################################################################################
    Codigo principal
'''########################################################################################

app = FastAPI()

movie = pd.read_csv("./Data/movies_clean.csv")
movie_ml = pd.read_csv("./Data/movies_ml.csv")
cast = pd.read_csv("./Data/credits_cast_clean.csv")
crew = pd.read_csv("./Data/credits_crew_clean.csv")


if movie_ml.columns[0] == 'Unnamed: 0':
  movie_ml.drop(columns= 'Unnamed: 0', inplace= True)

if movie.columns[0] == 'Unnamed: 0':
  movie.drop(columns= 'Unnamed: 0', inplace= True)

if cast.columns[0] == 'Unnamed: 0':
  cast.drop(columns= 'Unnamed: 0', inplace= True)

if crew.columns[0] == 'Unnamed: 0':
  crew.drop(columns= 'Unnamed: 0', inplace= True)

movie_ml['genres'].fillna('', inplace=True)

# Elimino una fila que tiene casi todos los campos vacios y fecha en el id_movie
movie.drop(index= 19722, inplace= True)

indice_sin_fecha = movie[movie['release_date'] == '0'].index
movie_date_fix = movie.drop(index= indice_sin_fecha)



# Codigo para el modelo Ml de recomendacion

# Crear la matriz de características utilizando TF-IDF
vectorizer = TfidfVectorizer()
features_matrix = vectorizer.fit_transform(movie_ml['genres'])
    
# Calcular la similitud del coseno entre las películas
similarity_matrix = linear_kernel(features_matrix, features_matrix)

'''########################################################################################
    End Points para la API
'''########################################################################################
# Peliculas estrenadas en el mes    
@app.get("/Mes/{mes}")
def cantidad_filmaciones_mes(mes):
    mes_numero = mes_a_numero(mes)
    mes_print = mes.title()   

    filtro = pd.to_datetime(movie_date_fix['release_date']).dt.month == mes_numero
    total_peli_mes = movie_date_fix[filtro].shape[0]

    return {"data" : f"{total_peli_mes} películas fueron estrenadas en el mes de {mes_print}"}

# Peliculas estrenadas en el dia  
@app.get("/Dia/{dia}")
def cantidad_filmaciones_dia(dia):
    dia_numero = dia_a_numero(dia)
    dia_print = dia.title()

    filtro = pd.to_datetime(movie_date_fix['release_date']).dt.weekday == dia_numero
    total_peli_dia = movie_date_fix[filtro].shape[0]

    return {"data" : f"{total_peli_dia} películas fueron estrenadas en los días {dia_print}"}
    

@app.get("/Titulo/{titulo}")
def score_titulo(titulo):
    title_lower = titulo.lower()

    index_rows = movie_date_fix[movie_date_fix['title'].str.lower() == title_lower].index.tolist()


    if not index_rows:
        return {"message": f"La película {titulo} no está en la lista o fue ingresada incorrectamente"}

    movies = []
    message = ''
    for index_row in index_rows:
        title = movie_date_fix.loc[index_row, 'title']
        year = int(movie_date_fix.loc[index_row, 'release_year'])
        score = float(movie_date_fix.loc[index_row, 'popularity'])
        message += f"La película {title} fue estrenada en el año {year} con un score/popularidad de {score}      "
        movies.append({"title": title, "year":year, "score": score})

    return {"data" : message}



@app.get("/Votos/{titulo}")
def votos_titulo(titulo):
    title_lower = titulo.lower()

    index_rows = movie_date_fix[movie_date_fix['title'].str.lower() == title_lower].index.tolist()

    if not index_rows:
        return {"message": f"La película {titulo} no está en la lista o fue ingresada incorrectamente"}

    movies = []
    message = ''
    for index_row in index_rows:
        title = movie_date_fix.loc[index_row, 'title']
        year = int(movie_date_fix.loc[index_row, 'release_year'])
        if float(movie_date_fix.loc[index_row, 'vote_count']) > 2000:
            vote = float(movie_date_fix.loc[index_row, 'vote_count'])
            vote_average = float(movie_date_fix.loc[index_row, 'vote_average'])
            movies.append({"title": title, "vote":vote, "vote_average": vote_average})
            message += f"La película {title} fue estrenada en el año {year}. La misma cuenta con un total de {vote} valoraciones, con un promedio de {vote_average}   "
        else:
            message += f"La película {title} fue estrenada en el año {year} no cuenta con al menos 2000 valoraciones"
            
    return {"data" : message}



# def get_actor( nombre_actor ): 
#       Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo 
#       devolver el éxito del mismo medido a través del retorno. Además, la cantidad de 
#       películas que en las que ha participado y el promedio de retorno. La definición no 
#       deberá considerar directores.
#       Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones, el mismo ha conseguido un retorno de X con un promedio de X por filmación
@app.get("/Actor/{actor}")
def get_actor(actor):


    actor_lower = actor.lower()

    index_rows = cast[cast['name'].str.lower() == actor_lower].index.tolist()
    id_movie_columns = cast.loc[index_rows, 'id_movie'].astype(object).tolist()
    
    movie['id_movie'] = movie['id_movie'].astype(object)
    filtered_movie = movie[movie['id_movie'].isin(id_movie_columns)]
    filtered_movie['revenue'] = filtered_movie['revenue'].astype(float)
    revenue_total = filtered_movie['revenue'].sum()

    return {"data" : str(revenue_total)}



# def get_director( nombre_director ): 
#       Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo 
#       devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el 
#       nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia 
#       de la misma.
@app.get("/Director/{director}")
def get_director(director):
    return {"data" : str(director)}



@app.get("/Recomendacion/{recomendacion}")
def recomendacion(recomendacion):
    recommendations = get_recommendations(recomendacion, similarity_matrix, movie_ml)
    
    return {"data" : str(recommendations)}