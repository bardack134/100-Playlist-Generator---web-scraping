#le pedimos al usuiario que ingrese la fecha en la cual le gustaria obtner las canciones mas populares
from datetime import datetime
from bs4 import BeautifulSoup
import requests


date=input('Please enter the desired date in the format YYYY-MM-DD to obtain the top most popular songs on that date: ')


#funcion que usaremos para validar la fecha ingresada por el user
def validate_date(date: str, format_str: str) -> bool:
    
    global date_input_str #global constant for date_text to be keyed in by user
    
    
    date_input_str = date   
    
    
    try:
        
    #convertmios la cadena de texto que representa la fecha en un formato datetime, para  manipular la data mas facilmente y hacer validaciones
        date_as_time = datetime.strptime(date, format_str)
        
    except ValueError:
        
        return False
    
# check if date is in the past
    if date_as_time < datetime.now():
        
        return True
    
    else:
        
        print("Date format is correct, but it is in the future")
        return False
    

while not validate_date(date, "%Y-%m-%d"):
    print("Invalid date. Please try again.")
    print()
    date=input('Please enter the desired date in the format YYYY-MM-DD to obtain the top most popular songs on that date: ')
    

#url de la cual vamos hacer web scraping y obtener el top de las 10 canciones mas populares para la fecha que el usuario ingresara
URL=f"https://www.billboard.com/charts/hot-100/{date_input_str}"


#hacemos un get request para obtener la informacion de nuestra pag web
response=requests.get(URL)


#informacion de nuestra pag web
web_html=response.text


#Creando objeto beautiful soup
soup=BeautifulSoup(web_html, 'html.parser')

print(soup.prettify())