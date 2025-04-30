import numpy as np
import pandas as pd
import requests as req

# Función para añadir un nuevo libro a un diccionario determinado.
# Se pasan como argumentos el diccionario y el código ISBN del libro.
def nuevo_libro (diccionario, codigo_isbn):

    # Se genera la consulta a través de una API
    isbn = codigo_isbn
    h = {'Authorization': "61066_f9ba2c2c66284291bfbe3153a53fdb85"} # ...............................Borrar API en entrega final!!!
    response = req.get(f"https://api2.isbndb.com/book/{isbn}", headers= h)

    # Si la conexión se ha validado, se añaden los datos del libro consultado al diccionario. En caso contrario se lanza un mensaje de error.
    if response.status_code == 200:
            book_info = response.json().get('book', {})
            diccionario.update({
                'ISBN': isbn,
                'Title': book_info.get('title', ''),
                'Author': ', '.join(book_info.get('authors', [])),
                'Publisher': book_info.get('publisher', ''),
                'Pages': book_info.get('pages', ''),
                'Date Published': book_info.get('date_published', ''),
                'Subjects': ', '.join(book_info.get('subjects', [])),
                'Binding': book_info.get('binding', ''),
                'Synopsis': book_info.get('synopsis', ''),
                'Language': book_info.get('language', ''),
                'Edition': book_info.get('edition', ''),
                'Dimensions': book_info.get('dimensions', ''),
                'MSRP': book_info.get('msrp', ''),
                'Image': book_info.get('image', ''),
                'Status': 'Success'
            })
    else:
            print(f"Error de ISBN {isbn}: {response.status_code}")

    return diccionario
