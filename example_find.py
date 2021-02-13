import sys
from io import BytesIO
from get_spn import get_spn, get_spn_extended
import requests
from PIL import Image


def open_image(json_response, adding_points=None, spn=None):
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    if spn is None:
        spn_longitude, spn_lattitude = get_spn(json_response)
    else:
        spn_longitude, spn_lattitude = spn

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([spn_longitude, spn_lattitude]),
        "l": "map",
        'pt': ",".join([toponym_longitude, toponym_lattitude, 'pm2dol'])
    }

    if adding_points:
        map_params['pt'] = '~'.join(adding_points)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
    # Создадим картинку
    # и тут же ее покажем встроенным просмотрщиком операционной системы


def find_by_toponym(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    return response.json()
    # Получаем первый топоним из ответа геокодера.


if __name__ == '__main__':
    # Пусть наше приложение предполагает запуск:
    # python search.py Москва, ул. Ак. Королева, 12
    # Тогда запрос к геокодеру формируется следующим образом:
    toponym_to_find = " ".join(sys.argv[1:])

    json_response = find_by_toponym(toponym_to_find)
    open_image(json_response)
