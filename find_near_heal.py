import requests
import sys
from example_find import open_image, find_by_toponym
from get_spn import get_spn_extended


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


def set_point_for_org(org):
    ll = org['geometry']['coordinates']
    style = 'pm2'
    size = 'l'

    if 'TwentyFourHours' in org['properties']['CompanyMetaData']['Hours']['Availabilities'][0].keys():
        work_hours = True
    elif 'Intervals' in org['properties']['CompanyMetaData']['Hours']['Availabilities'][0].keys():
        work_hours = False
    else:
        work_hours = None

    if work_hours:
        color = 'dg'
    elif work_hours is not None:
        color = 'db'
    else:
        color = 'gr'

    return str(ll[0]) + ',' + str(ll[1]) + ',' + style + color + size


if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])
    json_response = find_by_toponym(toponym_to_find)

    heal_response = find_near_heal(get_ll(json_response)).json()
    toponym_to_find = heal_response['features'][0]['properties']['CompanyMetaData']['address']

    adding_points = list()
    for healers in heal_response['features'][1:]:
        adding_points.append(set_point_for_org(healers))

    json_response = find_by_toponym(toponym_to_find)
    spn = get_spn_extended(heal_response['properties']['ResponseMetaData']['SearchResponse']['boundedBy'])

    open_image(json_response, adding_points, spn)
