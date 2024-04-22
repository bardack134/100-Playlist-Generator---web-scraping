#le pedimos al usuiario que ingrese la fecha en la cual le gustaria obtner las canciones mas populares
from datetime import datetime
import pprint
from bs4 import BeautifulSoup
import requests
from constansts import CLIENT_ID, CLIENT_SECRET, USER_NAME
import spotipy
from spotipy.oauth2 import SpotifyOAuth



date=input('Please enter the desired date in the format YYYY-MM-DD to obtain the top most popular songs on that date: ')


#funcion que usaremos para validar la fecha ingresada por el user, recibe la fecha como parametro y el formato en que deberia estar la fecha
def validate_date(date: str, format_str: str) -> bool:
    

    try:
        
    #convertmios la cadena de texto que representa la fecha en un formato datetime, para  manipular la data mas facilmente y hacer validaciones
        date_as_time = datetime.strptime(date, format_str)
    
    
    #si ocurre un error, es porque la fecha ingresada por el user esta mal escrita y devuelve false    
    except ValueError:
        
        return False
    
# no ocurrio ningun error y se pudo crear el objetodatetime, comparamos ahora si la fecha es futura
    if date_as_time < datetime.now():
        
        #si es correcto devolvemos la fecha
        return date
    
    else:
        
        print("Date format is correct, but it is in the future")
        return False
    

while  validate_date(date, "%Y-%m-%d") ==False:
    print("Invalid date. Please try again.")
    print()
    date=input('Please enter the desired date in the format YYYY-MM-DD to obtain the top most popular songs on that date: ')
    

#url de la cual vamos hacer web scraping y obtener el top de las 10 canciones mas populares para la fecha que el usuario ingresara
URL=f"https://www.billboard.com/charts/hot-100/{date}"


#hacemos un get request para obtener la informacion de nuestra pag web
response=requests.get(URL)


#informacion de nuestra pag web
web_html=response.text


#Creando objeto beautiful soup
soup=BeautifulSoup(web_html, 'html.parser')


#usando el metodo select, encuentro todas las etiquetas "h3" (que tiene el nombre de las canciones) especificando sus etiquetas padres
h3_tags=soup.css.select("li > ul > li > h3")#encuentra las etiquestas h3 que esta dentro de un li, ya a su vez dentro de un ul..etc


#creo una lista donde guardare el titulo de las canciones
songs_names=[song.get_text().strip('\n\t') for song in h3_tags ]
# songs_names=[]

# for song in h3_tags:
#     songs_names.append(song.get_text().strip('\n\t'))

pprint.pp(songs_names)


#usamos la libreria Spotipy para autenticar nuestro proyecto python usando nuestro "CLIENT_ID_, CLIENT_SECRET", 
#informacion detallada mirar la documentacion "https://spotipy.readthedocs.io/en/2.22.1/"


#necesitamos obtener el id de usuario autenticado
# necesitamos el redirect_url que especificamos en nuestra app en spotify Dashboar "http://localhost/"
#solicitar permiso para modificar listas 


#Crea una instancia de la clase Spotify de spotipy
sp = spotipy.Spotify(
    
    auth_manager=SpotifyOAuth(
        
        #permiso para crear playlist
        scope="playlist-modify-private",
        
        
        #URI de redireccionamiento a la que se enviará el token de acceso después de que el usuario haya autorizado la aplicación
        redirect_uri="http://localhost/",
        
        
        #datos que se encuentran en la  plataforma de desarrolladores de Spotify
        client_id=CLIENT_ID,       
        client_secret=CLIENT_SECRET,
        
        
        #  el nombre de usuario real de Spotify.
        username=USER_NAME
        
        
    )
)

# Obtener el ID de usuario actual, devuelve información sobre el usuario actualmente autenticado, incluido su ID de usuario.  
user_id = sp.current_user()["id"]


#TODO:buscamos las canciones  almacenadas en la lista "songs_names" en Spotify

# Inicializa una lista vacía llamada song_uris que se utilizará para almacenar los URIs de las canciones encontradas en Spotify.
song_uris = []


#Divide la fecha ingresada por el usuario en sus partes componentes y extrae el año (el primer elemento después de dividir la cadena en función del guión -).
year = str(date).split("-")[0]


#Itera sobre cada nombre de canción en la lista song_names
for song in songs_names:
    
    # Utiliza el método search de la instancia sp para buscar canciones en Spotify que coincidan con el nombre de la canción y el año especificado. Esto devuelve un objeto JSON con los resultados de la búsqueda.
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    
    
    print(result)
    
    
    try:
        #  Extrae el URI de la primera canción encontrada en los resultados de la búsqueda. Este URI se agrega a la lista song_uris.
        uri = result["tracks"]["items"][0]["uri"]
        
        
        song_uris.append(uri)
        
    except IndexError:
        
        #  Si no se encuentra ninguna canción,  imprime un mensaje indicando que la canción no existe en Spotify.
        print(f"{song} doesn't exist in Spotify. Skipped.")
        
pprint.pp(song_uris)


#creaando playlist de canciones, recibe 3 parametros usuario, fecha ingresada para el nombre del playlisyt, y publico false
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)


# print(playlist)
# gregamos las canciones en la lista song_uris, a la lista de reproducción recién creada en Spotify, identificada por su ID playlist["id"].
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)