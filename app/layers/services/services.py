# capa de servicio/lógica de negocio

from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import random

# función que devuelve un listado de cards. Cada card representa una imagen de la API de HP.
def getAllImages():
    raw_images = transport.getAllImages()  # Llamamos a la función de transport.py
    cards = [] # Lista de cards vacia

    for img in raw_images:
        alternate_names = img.get("alternate_names", [])  # Obtener nombres alternativos
        selected_name = random.choice(alternate_names) if alternate_names else "No hay nombres alternativos" # Seleccionar un nombre alternativo al azar
        card = translator.fromRequestIntoCard({
            "name": img["name"],
            "gender": img["gender"],
            "house": img.get("house"),
            "alternate_names": selected_name,
            "actor": img.get("actor"),
            "image": img["image"]
        }) # Crear la card con los datos necesarios
        cards.append(card) # Agregar la card a la lista 'cards'

    # 6️) Retornar la lista de cards
    return cards

# función que filtra según el nombre del personaje.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        if name.lower() in card.lower():
            filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su casa.
def filterByHouse(house_name):
    filtered_cards = []

    for card in getAllImages():
        if house_name.lower() in card.lower():
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID
