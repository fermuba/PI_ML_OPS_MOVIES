import numpy as np
import pandas as pd
from fastapi import FastAPI

app = FastAPI()

movie = pd.read_csv("./Data/movies_clean.csv")

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
    
# def cantidad_filmaciones_mes( Mes ): 
#       Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas 
#       que fueron estrenadas en el mes consultado en la totalidad del dataset.
#       -Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X
@app.get("/Mes/{mes}")
def cantidad_filmaciones_mes(mes):
    mes_numero = mes_a_numero(mes)
    mes_print = mes.title()

    indice_sin_fecha = movie[movie['release_date'] == '0'].index
    movie_date_fix = movie.drop(index= indice_sin_fecha)

    filtro = pd.to_datetime(movie_date_fix['release_date']).dt.month == mes_numero
    total_peli_mes = movie_date_fix[filtro].shape[0]

    return {"data" : f"{total_peli_mes} cantidad de películas fueron estrenadas en el mes de {mes_print}"}

    
# def cantidad_filmaciones_dia( Dia ): 
#       Se ingresa un día en idioma Español. Debe devolver la cantidad de películas 
#       que fueron estrenadas en día consultado en la totalidad del dataset.
#       Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X
@app.get("/Dia/{dia}")
def cantidad_filmaciones_dia(dia):
    return {"data" : str(dia)}
    


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
    return {"data" : str(recomendacion)}