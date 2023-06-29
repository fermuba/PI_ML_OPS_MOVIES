import numpy as np
import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

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
        return{"message": 'No se encuentra la Pelicula'}  # No se encontraron películas coincidentes

    idx = indices[0]  # Obtener el primer índice coincidente

    #return idx

    # Obtener los puntajes de similitud de la película de referencia con todas las demás películas
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    #return similarity_scores

    # Ordenar las películas por su puntaje de similitud en orden descendente
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    #return combined_df.genres.head()


    # Obtener los índices de las películas más similares
    top_indices = [score[0] for score in similarity_scores[1:top_n+1]]

    # Obtener los títulos de las películas más similares
    top_movies = movies_df.iloc[top_indices]['title'].tolist()

    return top_movies



#########################################################################################
app = FastAPI()

movie = pd.read_csv("./Data/movies_clean.csv")
movie_ml = pd.read_csv("./Data/movies_ml.csv")

if movie_ml.columns[0] == 'Unnamed: 0':
  movie_ml.drop(columns= 'Unnamed: 0', inplace= True)

if movie.columns[0] == 'Unnamed: 0':
  movie.drop(columns= 'Unnamed: 0', inplace= True)

movie_ml['genres'].fillna('', inplace=True)

indice_sin_fecha = movie[movie['release_date'] == '0'].index
movie_date_fix = movie.drop(index= indice_sin_fecha)
#movie_date_fix = pd.to_datetime(movie_date_fix['release_date'])

### #######################  CODIGO PARA MODELO ML


# Crear la matriz de características utilizando TF-IDF
vectorizer = TfidfVectorizer()
features_matrix = vectorizer.fit_transform(movie_ml['genres'])
    
# Calcular la similitud del coseno entre las películas
similarity_matrix = linear_kernel(features_matrix, features_matrix)






    
@app.get("/Mes/{mes}")
def cantidad_filmaciones_mes(mes):
    mes_numero = mes_a_numero(mes)
    mes_print = mes.title()   

    filtro = pd.to_datetime(movie_date_fix['release_date']).dt.month == mes_numero
    total_peli_mes = movie_date_fix[filtro].shape[0]

    return {"data" : f"{total_peli_mes} películas fueron estrenadas en el mes de {mes_print}"}

    
@app.get("/Dia/{dia}")
def cantidad_filmaciones_dia(dia):
    dia_numero = dia_a_numero(dia)
    dia_print = dia.title()

    filtro = pd.to_datetime(movie_date_fix['release_date']).dt.weekday == dia_numero
    total_peli_dia = movie_date_fix[filtro].shape[0]

    return {"data" : f"{total_peli_dia} películas fueron estrenadas en los días {dia_print}"}
    


# def score_titulo( titulo_de_la_filmación ): 
#       Se ingresa el título de una filmación esperando como respuesta el título, 
#       el año de estreno y el score.
#       Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X
@app.get("/Titulo/{titulo}")
def score_titulo(titulo):
    return {"data" : str(titulo)}



# def votos_titulo( votos_de_la_filmación ): 
#       Se ingresa el título de una filmación esperando como respuesta el título, 
#       la cantidad de votos y el valor promedio de las votaciones. La misma variable 
#       deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar 
#       con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve 
#       ningun valor.
#       Ejemplo de retorno: La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, con un promedio de X
@app.get("/Votos/{votos}")
def votos_titulo(votos):
    return {"data" : int(votos)}



# def get_actor( nombre_actor ): 
#       Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo 
#       devolver el éxito del mismo medido a través del retorno. Además, la cantidad de 
#       películas que en las que ha participado y el promedio de retorno. La definición no 
#       deberá considerar directores.
#       Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones, el mismo ha conseguido un retorno de X con un promedio de X por filmación
@app.get("/Actor/{actor}")
def get_actor(actor):
    return {"data" : str(actor)}



# def get_director( nombre_director ): 
#       Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo 
#       devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el 
#       nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia 
#       de la misma.
@app.get("/Director/{director}")
def get_director(director):
    return {"data" : str(director)}



# def recomendacion( titulo ): 
#       Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.
@app.get("/Recomendacion/{recomendacion}")
def recomendacion(recomendacion):
    # Ejemplo de uso: Obtener las 5 películas más similares a 'Toy Story'

    recommendations = get_recommendations(recomendacion, similarity_matrix, movie_ml)
    
    #print(recommendations)
    return {"data" : str(recommendations)}