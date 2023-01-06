import requests
from pprint import pprint
class GeoLoc(object):
    def __init__(self, geoloc, place):
        self.geoloc = geoloc
        self.place = place

    def location(self):
        mas = []
        key = '2d3a7435-6798-428d-908b-31d615333bba'
        url = 'https://search-maps.yandex.ru/v1/'
        param = {'apikey': key, 'text': self.place, 'lang': 'ru_RU', 'll': f'{self.geoloc[1]},{self.geoloc[0]}',
                 'spn': '0.652069,0.600552', 'rspn': 1,
                 'results': 5, }
        places = requests.get(url, params=param).json()
        count = 5
        if places['properties']['ResponseMetaData']['SearchResponse']['found'] < 5:
            count = places['properties']['ResponseMetaData']['SearchResponse']['found']
        for i in range(count):
            name = places["features"][i]["properties"]["CompanyMetaData"]["name"]
            address = places["features"][i]["properties"]["CompanyMetaData"]["address"].split(', ')
            coordinates = places["features"][i]["geometry"]["coordinates"]
            coordinates = [coordinates[1], coordinates[0]]

            del address[0]
            address = ', '.join(address)
            try:
                hours = places["features"][i]["properties"]["CompanyMetaData"]["Hours"]["text"].split('; ')
                hours = ',\n'.join(hours)
            except:
                hours = 'информация отсутствует'
            try:
                url = places["features"][i]["properties"]["CompanyMetaData"]["url"]
            except:
                url = ''
            mas += [{'name': name, 'address': address, 'hours': hours, 'url': url, 'coordinates':coordinates }]
        return mas
