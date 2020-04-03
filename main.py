import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

from params_to_geocode import get_size
import requests
from PIL import Image


def get_object_data():
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    return response


def get_map_part_from_object(response):

    json_response = response.json()

    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    toponym_coodrinates = toponym["Point"]["pos"]

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    toponymx = toponym["boundedBy"]["Envelope"]

    delta = get_size(toponymx["lowerCorner"], toponymx["upperCorner"])

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(delta),
        "l": "map",
        "pt": "{},{},org".format(toponym_longitude, toponym_lattitude)
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response


response = get_object_data()

if not response:
    print('error')

response = get_map_part_from_object(response)

Image.open(BytesIO(response.content)).show()
