import numpy as np
import pandas as pd
import requests


def nuevo_libro (diccionario, clave):
# Función para añadir un nuevo libro a un diccionario determinado.
# Se pasan como argumentos el diccionario y el código ISBN del libro.
    
    # Se genera la consulta a través de una API en función del valor que se pase como argumento.    
    if type(clave) == int:
        isbn = clave
        h = {"Authorization": "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
        respuesta = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers= h)
    if type(clave) == str:
        title = clave
        h = {"Authorization": "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
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
                 #"Subjects": ", ".join(book_info.get("subjects", [])),
                 #"Binding": book_info.get("binding", ""),
                 "Sinopsis": book_info.get("synopsis", ""),
                 "Lengua original": book_info.get("language", ""),
                 "Edición": book_info.get("edition", ""),
                 "Dimensiones": book_info.get("dimensions", ""),
                 #"MSRP": book_info.get("msrp", ""),
                 #"Image": book_info.get("image", ""),
             })
        elif type(clave) == str:
             diccionario.update({
                 "ISBN": book_info[0].get("isbn13", ""),
                 "Título": book_info[0].get("title", ""),
                 "Autor": ", ".join(book_info[0].get("authors", [])),
                 "Editorial": book_info[0].get("publisher", ""),
                 "Páginas": book_info[0].get("pages", ""),
                 "Fecha de publicación": book_info[0].get("date_published", ""),
                 #"Subjects": ", ".join(book_info[0].get("subjects", [])),
                 #"Binding": book_info[0].get("binding", ""),
                 "Sinopsis": book_info[0].get("synopsis", ""),
                 "Lengua original": book_info[0].get("language", ""),
                 "Edición": book_info[0].get("edition", ""),
                 "Dimensiones": book_info[0].get("dimensions", ""),
                 #"MSRP": book_info[0].get("msrp", ""),
                 #"Image": book_info[0].get("image", ""),
             })
    else:
            print(f"Error de ISBN {isbn}: {respuesta.status_code}")

    return diccionario
    

def nuevo_libro_isbn (diccionario, codigo_isbn):
# Función para añadir un nuevo libro a un diccionario determinado.
# Se pasan como argumentos el diccionario y el código ISBN del libro.
    
    # Se genera la consulta a través de una API en función del valor que se pase como argumento.    
    isbn = codigo_isbn
    h = {"Authorization": "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
    respuesta = requests.get(f"https://api2.isbndb.com/book/{isbn}", headers= h)
   
    # Si la conexión se ha validado, se añaden los datos del libro consultado al diccionario. En caso contrario se lanza un mensaje de error.
    if respuesta.status_code == 200:
            book_info = respuesta.json().get("book", {})
            diccionario.update({
                "ISBN": isbn,
                "Título": book_info.get("title", ""),
                "Autor": ", ".join(book_info.get("authors", [])),
                "Editorial": book_info.get("publisher", ""),
                "Páginas": book_info.get("pages", ""),
                "Fecha de publicación": book_info.get("date_published", ""),
                #"Subjects": ", ".join(book_info.get("subjects", [])),
                #"Binding": book_info.get("binding", ""),
                "Sinopsis": book_info.get("synopsis", ""),
                "Lengua original": book_info.get("language", ""),
                "Edición": book_info.get("edition", ""),
                "Dimensiones": book_info.get("dimensions", ""),
                #"MSRP": book_info.get("msrp", ""),
                #"Image": book_info.get("image", ""),
            })
    else:
            print(f"Error de ISBN {isbn}: {respuesta.status_code}")

    return diccionario


def nuevo_libro_titulo (diccionario, titulo):
# Función para añadir un nuevo libro a un diccionario determinado.
# Se pasan como argumentos el diccionario y el título del libro.
    
    # Se genera la consulta a través de una API en función del valor que se pase como argumento.   
    title = titulo
    h = {"Authorization": "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
    respuesta = requests.get(f"https://api2.isbndb.com/books/{title}?page=1&pageSize=1&column=title&shouldMatchAll=1", headers= h)
   
    # Si la conexión se ha validado, se añaden los datos del libro consultado al diccionario. En caso contrario se lanza un mensaje de error.
    if respuesta.status_code == 200:
            book_info = respuesta.json().get("books", {})
            diccionario.update({
                "ISBN": book_info[0].get("isbn13", ""),
                "Título": book_info[0].get("title", ""),
                "Autor": ", ".join(book_info[0].get("authors", [])),
                "Editorial": book_info[0].get("publisher", ""),
                "Páginas": book_info[0].get("pages", ""),
                "Fecha de publicación": book_info[0].get("date_published", ""),
                #"Subjects": ", ".join(book_info.get("subjects", [])),
                #"Binding": book_info.get("binding", ""),
                "Sinopsis": book_info[0].get("synopsis", ""),
                "Lengua original": book_info[0].get("language", ""),
                "Edición": book_info[0].get("edition", ""),
                "Dimensiones": book_info[0].get("dimensions", ""),
                #"MSRP": book_info.get("msrp", ""),
                #"Image": book_info.get("image", ""),
            })
    else:
            print(f"Error de ISBN {isbn}: {respuesta.status_code}")

    return diccionario