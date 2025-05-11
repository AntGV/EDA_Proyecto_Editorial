import matplotlib.pyplot as plt
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

class BubbleChart:
    def __init__(self, area, bubble_spacing=0):
        """
        Setup for bubble collapse.

        Parameters
        ----------
        area : array-like
            Area of the bubbles.
        bubble_spacing : float, default: 0
            Minimal spacing between bubbles after collapsing.

        Notes
        -----
        If "area" is sorted, the results might look weird.
        """
        area = np.asarray(area)
        r = np.sqrt(area / np.pi)

        self.bubble_spacing = bubble_spacing
        self.bubbles = np.ones((len(area), 4))
        self.bubbles[:, 2] = r
        self.bubbles[:, 3] = area
        self.maxstep = 2 * self.bubbles[:, 2].max() + self.bubble_spacing
        self.step_dist = self.maxstep / 2

        # calculate initial grid layout for bubbles
        length = np.ceil(np.sqrt(len(self.bubbles)))
        grid = np.arange(length) * self.maxstep
        gx, gy = np.meshgrid(grid, grid)
        self.bubbles[:, 0] = gx.flatten()[:len(self.bubbles)]
        self.bubbles[:, 1] = gy.flatten()[:len(self.bubbles)]

        self.com = self.center_of_mass()

    def center_of_mass(self):
        return np.average(
            self.bubbles[:, :2], axis=0, weights=self.bubbles[:, 3]
        )

    def center_distance(self, bubble, bubbles):
        return np.hypot(bubble[0] - bubbles[:, 0],
                        bubble[1] - bubbles[:, 1])

    def outline_distance(self, bubble, bubbles):
        center_distance = self.center_distance(bubble, bubbles)
        return center_distance - bubble[2] - \
            bubbles[:, 2] - self.bubble_spacing

    def check_collisions(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return len(distance[distance < 0])

    def collides_with(self, bubble, bubbles):
        distance = self.outline_distance(bubble, bubbles)
        return np.argmin(distance, keepdims=True)

    def collapse(self, n_iterations=50):
        """
        Move bubbles to the center of mass.

        Parameters
        ----------
        n_iterations : int, default: 50
            Number of moves to perform.
        """
        for _i in range(n_iterations):
            moves = 0
            for i in range(len(self.bubbles)):
                rest_bub = np.delete(self.bubbles, i, 0)
                # try to move directly towards the center of mass
                # direction vector from bubble to the center of mass
                dir_vec = self.com - self.bubbles[i, :2]

                # shorten direction vector to have length of 1
                dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))

                # calculate new bubble position
                new_point = self.bubbles[i, :2] + dir_vec * self.step_dist
                new_bubble = np.append(new_point, self.bubbles[i, 2:4])

                # check whether new bubble collides with other bubbles
                if not self.check_collisions(new_bubble, rest_bub):
                    self.bubbles[i, :] = new_bubble
                    self.com = self.center_of_mass()
                    moves += 1
                else:
                    # try to move around a bubble that you collide with
                    # find colliding bubble
                    for colliding in self.collides_with(new_bubble, rest_bub):
                        # calculate direction vector
                        dir_vec = rest_bub[colliding, :2] - self.bubbles[i, :2]
                        dir_vec = dir_vec / np.sqrt(dir_vec.dot(dir_vec))
                        # calculate orthogonal vector
                        orth = np.array([dir_vec[1], -dir_vec[0]])
                        # test which direction to go
                        new_point1 = (self.bubbles[i, :2] + orth *
                                      self.step_dist)
                        new_point2 = (self.bubbles[i, :2] - orth *
                                      self.step_dist)
                        dist1 = self.center_distance(
                            self.com, np.array([new_point1]))
                        dist2 = self.center_distance(
                            self.com, np.array([new_point2]))
                        new_point = new_point1 if dist1 < dist2 else new_point2
                        new_bubble = np.append(new_point, self.bubbles[i, 2:4])
                        if not self.check_collisions(new_bubble, rest_bub):
                            self.bubbles[i, :] = new_bubble
                            self.com = self.center_of_mass()

            if moves / len(self.bubbles) < 0.1:
                self.step_dist = self.step_dist / 2

    def plot(self, ax, labels, colors):
        """
        Draw the bubble plot.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
        labels : list
            Labels of the bubbles.
        colors : list
            Colors of the bubbles.
        """
        for i in range(len(self.bubbles)):
            circ = plt.Circle(
                self.bubbles[i, :2], self.bubbles[i, 2], color=colors[i])
            ax.add_patch(circ)
            ax.text(*self.bubbles[i, :2], labels[i],
                    horizontalalignment='center', verticalalignment='center')
