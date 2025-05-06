import numpy as np
import pandas as pd
import requests


def titulo_rect (titulo):
# Función que elimina el título original de la columna de títulos de libros. 
    if "(" in titulo:
        pos = titulo.index("(")
        titulo_uni = titulo[:pos]
        titulo_fin = titulo_uni.strip()
    else:
        titulo_fin = titulo
    titulo_fin = titulo_fin.upper()
    return titulo_fin

def sales_rect (sales, lista):
# Función que elimina símbolos de la columna sales. 
    for simbol in lista:
        if simbol in sales:
            pos = sales.index(simbol)
            sales_uni = sales[:pos]
            sales_fin = sales_uni.strip()
            sales = sales_fin
        else:
            sales_fin = sales
    return sales_fin

def serie_extr (titulo):
# Función que extrae la serie de la columna que contiene el título. 
    if "(" in titulo:
        pos = titulo.index("(")
        serie_uni = titulo[pos:]
        serie_uni = serie_uni.replace("(","")
        serie_uni = serie_uni.replace(")","")
        serie_uni = serie_uni.replace(",","")
        serie_fin = serie_uni.strip()
    else:
        serie_fin = None
    return serie_fin
    
def nuevo_libro (diccionario, clave):
# Función para añadir un nuevo libro a un diccionario determinado.
# Se pasan como argumentos el diccionario y el código ISBN del libro.
    
    # Se genera la consulta a través de una API en función del valor que se pase como argumento.    
    h = {"Authorization": "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
    if type(clave) == int:
        isbn = clave
        respuesta = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers= h)
    if type(clave) == str:
        title = clave
        respuesta = requests.get(f"https://api2.isbndb.com/books/{title}?page=1&pageSize=1&column=title&shouldMatchAll=1", headers= h)

    # Si la conexión se ha validado, se añaden los datos del libro consultado al diccionario. En caso contrario se lanza un mensaje de error.
    if respuesta.status_code == 200:
        book_info = respuesta.json().get("book", {})
        if type(clave) == int:
             diccionario.update({
                 "ISBN": book_info.get("isbn13", ""),
                 "Título": book_info.get("title", ""),
                 "Autor": ", ".join(book_info.get("authors", [])),
                 "Editorial": book_info.get("publisher", ""),
                 "Páginas": book_info.get("pages", ""),
                 "Fecha de publicación": book_info.get("date_published", ""),
                 "Género": ", ".join(book_info.get("subjects", [])),
                 "Formato": book_info.get("binding", ""),
                 "Sinopsis": book_info.get("synopsis", ""),
                 "Lengua original": book_info.get("language", ""),
                 "Edición": book_info.get("edition", ""),
                 "Dimensiones": book_info.get("dimensions", ""),
                 "Precio": book_info.get("msrp", ""),
                 #"Image": book_info.get("image", ""),
             })
        elif type(clave) == str:
            book_info = respuesta.json().get("books", {})
            diccionario.update({
                "ISBN": book_info[0].get("isbn13", ""),
                "Título": book_info[0].get("title", ""),
                "Autor": ", ".join(book_info[0].get("authors", [])),
                "Editorial": book_info[0].get("publisher", ""),
                "Páginas": book_info[0].get("pages", ""),
                "Fecha de publicación": book_info[0].get("date_published", ""),
                "Género": ", ".join(book_info[0].get("subjects", [])),
                "Formato": book_info[0].get("binding", ""),
                "Sinopsis": book_info[0].get("synopsis", ""),
                "Lengua original": book_info[0].get("language", ""),
                "Edición": book_info[0].get("edition", ""),
                "Dimensiones": book_info[0].get("dimensions", ""),
                "Precio": book_info[0].get("msrp", ""),
                #"Image": book_info.get("image", ""),
            })
    else:
            print(f"Error: {respuesta.status_code}")
            if respuesta.status_code == 429:
                print(clave)
                return diccionario            
    return diccionario

