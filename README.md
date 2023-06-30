<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# PROYECTO INDIVIDUAL Nº1

# Machine Learning Operations (MLOps)

<p align="center">
<img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png" height=300>
</p>

¡Bienvenidos al primer proyecto individual de la etapa de labs! En esta ocasión, deberán hacer un trabajo situándose en el rol de un MLOps Engineer.

## Descripción del problema (Contexto y rol a desarrollar)

### Contexto

Tienes tu modelo de recomendación dando unas buenas métricas 😏, y ahora, ¿cómo lo llevas al mundo real? 👀

El ciclo de vida de un proyecto de Machine Learning debe contemplar desde el tratamiento y recolección de los datos (Data Engineer stuff) hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.

### Rol a desarrollar

Empezaste a trabajar como Data Scientist en una start-up que provee servicios de agregación de plataformas de streaming. El mundo es bello y vas a crear tu primer modelo de ML que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha!

Vas a sus datos y te das cuenta de que la madurez de los mismos es poca (ok, es nula 😭): Datos anidados, sin transformar, no hay procesos automatizados para la actualización de nuevas películas o series, entre otras cosas... haciendo tu trabajo imposible 😓.

Debes empezar desde cero, haciendo un trabajo rápido de Data Engineer y tener un MVP (Minimum Viable Product) para las próximas semanas. Tu cabeza va a explotar 🤯, pero al menos sabes cuál es, conceptualmente, el camino que debes seguir ❗. Así que te espantas los miedos y te pones manos a la obra 💪.

-Mi primera accion tomada, es leer muy bien lo solicitado, y revisar la info asignada, con ayuda de un cuaderno tomo apuntes de lo que tengo que hacer, y lo mas importante de lo que no se hacer para buscar informacion y tener un primer contacto con las herramientas que necesito implementar. En este punto ya estoy pensando en los tiempos, como administrarlos, veo que tengo muchos caminos a elegir, y vuelan las ideas, pero lo importantes es aterrizar las mas importantes, creo que ese fue el desafio mayor que me toco hacer ya que uno siempre pienza en lo mejor, y quiere hacerlo de esa forma pero me di cuenta, luego de unos dias trabajando en el ETL de que los tiempos no me iban a permitir hacer mucho asi, que apure el paso y pase a desarrollar las etapas siguientes. Mi aprendizaje con este proyecto fue administrar tiempos y acotar trabajos, la busqueda de finalizar etapas, tratando de hacerlo lo mas simple posible, espero este dentro de los parametros solicitados, gracias.

### Transformaciones

...En este repositorio pueden encontrar una carpeta ETL con el codigo realizado en colab para el ETL de los archivos, se entregaron 2, luego genere los que crei necesarios.
Dejo los links a mi drive donde pueden encotrar los arvhivos creados, no todos termine usando en el deploy
https://drive.google.com/drive/folders/1BZ4Ma7g-FteeMNqKfwv59lS1MwfQSSp7?usp=sharing

https://drive.google.com/drive/folders/1wJT9qWogB6xSFG1ja3n1Guqkl6wg4ncR?usp=sharing

Dicionario de significado y guia de desarrollo del ETL
https://docs.google.com/spreadsheets/d/178thzs98-XP9D93N-KAYcDXUdKp8Z0u5/edit?usp=sharing&ouid=109596950351203936528&rtpof=true&sd=true

### Desarrollo API
Con respecto a la API la eleccion fue FastAPI, por la facilidad de trabajo

### Deployment

El deployment se realizo en Render con la guia de este tutorial https://github.com/HX-FNegrete/render-fastapi-tutorial


### Análisis exploratorio de los datos

La informacion fue mucha, y el tiempo limitado, con el poco tiempo que tenia me limite a presentar de forma grafica la mayor cantidad de informacion y que sea facil de entender con la ayuda de la herramienta SweetViz , las presentaciones pueden encontrarlas en el colab dentro de la carpeta EDA de este repositorio

### Sistema de recomendación

El Sistema de recomendacio que se termino eligiendo fue TF-IDF, y similitud del coseno para la eleccion de las recomendaciones, fue clave la eleccion correcta y optima de herramientas por los pocos recursos disponibles con render

### Video

https://youtu.be/KBWBvUn4rtE

