import requests
from datetime import datetime, timezone, timedelta

class Weather(object):
    def __init__(self, city):
        self.city = city

    def weather(self):
        try:
            city = self.city
            # получаем данные с сайта
            key = '7bfb9951dd9ef554feb6223cf9c27328'
            url = 'https://api.openweathermap.org/data/2.5/weather'
            if type(city) is list:
                param = {'APPID': key, 'lat': city[0], 'lon': city[1], 'units': 'metric', 'lang': 'ru'}
                mas = requests.get(url, params=param)
                weather = mas.json()
                url1 = 'https://api.openweathermap.org/data/2.5/forecast'
                param = {'APPID': key, 'lat': city[0], 'lon': city[1], 'cnt': 10, 'units': 'metric', 'lang': 'ru'}
                mas = requests.get(url1, params=param)
                forecast = mas.json()
            else:
                param = {'APPID': key, 'q': city, 'units': 'metric', 'lang': 'ru'}
                mas = requests.get(url, params=param)
                weather = mas.json()
                url1 = 'https://api.openweathermap.org/data/2.5/forecast'
                param = {'APPID': key, 'q': city, 'cnt': 10, 'units': 'metric', 'lang': 'ru'}
                mas = requests.get(url1, params=param)
                forecast = mas.json()
            # погода в данный момент времени
            city_ti = '{}, {}'.format(str(weather['name']), str(weather['sys']['country']))
            time_zone = weather['timezone'] / 3600
            time_city = timezone(timedelta(hours=time_zone))
            time_city_now = str(datetime.now(time_city))[11:16]
            sost = f'{str(weather["weather"][0]["description"]).capitalize()}'
            temp = '{}°C'.format(round(weather['main']['temp']))
            icon = 'Data/Image/heart.png'
            wind = 'Скорость ветра \n{} м/с'.format(weather['wind']['speed'])
            humidity = 'Влажность \n{}%'.format(str(weather['main']['humidity']))
            pressure = 'Давление \n{} мм рт. ст.'.format(int(weather['main']['pressure'] * 0.750062))
            clouds = weather['clouds']['all']
            main = str(weather['weather'][0]['main'])
            feels_like = round(weather['main']['feels_like'])
            if feels_like <= -30:
                feels_like_txt = 'very cold+'
            elif -30 < feels_like <= -20:
                feels_like_txt = 'very cold'
            elif -20 < feels_like <= -10:
                feels_like_txt = 'cold'
            elif -10 < feels_like <= 0:
                feels_like_txt = 'chilly'
            elif 0 < feels_like <= 10:
                feels_like_txt = 'medium'
            elif 10 < feels_like <= 20:
                feels_like_txt = 'warm'
            elif 20 < feels_like <= 30:
                feels_like_txt = 'heat'
            elif 30 < feels_like:
                feels_like_txt = 'very heat'
            # цвет кнопок и задний фон
            if 85 <= clouds <= 100:
                back = 'Data/Image/clouds.png'
                map = 'Data/Image//map1.png'
                map_press = 'Data/Image//map1_press.png'
                color_card = '#9A9CA0'
            elif 6 <= int(time_city_now[0:2]) <= 10:
                back = 'Data/Image/morning.png'
                map = 'Data/Image//map1.png'
                map_press = 'Data/Image//map1_press.png'
                color_card = '#C4BFC4'
            elif 0 <= int(time_city_now[0:2]) <= 5:
                back = 'Data/Image/night.png'
                map = 'Data/Image//map1.png'
                map_press = 'Data/Image//map1_press.png'
                color_card = '#333462'
            elif 17 <= int(time_city_now[0:2]) <= 23:
                back = 'Data/Image/midnight.png'
                map = 'Data/Image//map.png'
                map_press = 'Data/Image//map_press.png'
                color_card = '#2E4365'
            elif 11 <= int(time_city_now[0:2]) <= 16:
                back = 'Data/Image//afternoon.png'
                map = 'Data/Image//map1.png'
                map_press = 'Data/Image//map1_press.png'
                color_card = '#455FC4'
            # предсказание погоды 3ч
            forecast_city = []
            for i in range(10):
                forecast_time = str(datetime.strptime(forecast['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S').replace(
                    tzinfo=timezone(timedelta(hours=0))).astimezone(tz=time_city))
                forecast_time = '{}.{}\n{}'.format(forecast_time[8:10], forecast_time[5:7], forecast_time[11:16])
                forecast_city += [[forecast_time, '{}°C'.format(round(forecast['list'][i]['main']['temp'])),
                                    'Data/Image/{}.png'.format(forecast['list'][i]['weather'][0]['icon'])]]

            self.a = {'city_ti': city_ti, 'time_city_now': time_city_now, 'sost': sost, 'icon': icon, 'temp': temp,
                      'wind': wind,
                      'humidity': humidity,
                      'pressure': pressure, 'color_card': color_card, 'back': back, 'forecast_city': forecast_city, 'main': main,
                       'feels_like': feels_like_txt, 'map': map, 'map_press': map_press,
                      'lat': weather['coord']['lat'], 'lon': weather['coord']['lon']}
            return self.a
        except:
            return 'None'
