import requests
import sys
from example_find import open_image, find_by_toponym


def find_near_heal(address_ll):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    return response


def get_ll(json_response):
    position = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]['Point']['pos']
    return position.replace(' ', ',')


if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    json_response = find_by_toponym(toponym_to_find)

    heal_response = find_near_heal(get_ll(json_response)).json()
    toponym_to_find = heal_response['features'][0]['properties']['CompanyMetaData']['address']
    open_image(find_by_toponym(toponym_to_find))
