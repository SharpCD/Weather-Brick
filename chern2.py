from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from datetime import datetime, timezone, timedelta
from kivy.lang import Builder
import kivy.properties as kyprops
import requests
# from plyer import gps
import os
from random import choice
import webbrowser
from kivy.core.text import LabelBase

# LabelBase.register(name = 'Mirava Personal Use Only',  fn_regular='MiravaRegularPersonalUseOnl.ttf')


class Loading(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.login, 1)

    def login(self, *args):
        self.manager.current = 'log_in'
        pass

class LogIn(Screen):
    entry = kyprops.ObjectProperty(None)
    email = kyprops.ObjectProperty(None)
    password = kyprops.ObjectProperty(None)
    entry_btn = kyprops.ObjectProperty(None)
    sign_up_btn = kyprops.ObjectProperty(None)
    def on_enter(self, *args):
        self.entry.font_size = self.height / 28
        self.email.font_size = self.height / 40
        self.password.font_size = self.height / 40
        self.entry_btn.font_size = self.height / 40
        self.sign_up_btn.font_size = self.height / 40

class MenuWindow(Screen):
    btn = kyprops.ObjectProperty(None)
    map_btn = kyprops.ObjectProperty(None)
    img = kyprops.ObjectProperty(None)
    time = kyprops.ObjectProperty(None)
    city = kyprops.ObjectProperty(None)
    sost = kyprops.ObjectProperty(None)
    temp = kyprops.ObjectProperty(None)
    prssr = kyprops.ObjectProperty(None)
    hmdt = kyprops.ObjectProperty(None)
    wnd = kyprops.ObjectProperty(None)
    btn_clothes = kyprops.ObjectProperty(None)
    text_f0 = kyprops.ObjectProperty(None)
    text_f1 = kyprops.ObjectProperty(None)
    text_f2 = kyprops.ObjectProperty(None)
    text_f3 = kyprops.ObjectProperty(None)
    text_f4 = kyprops.ObjectProperty(None)
    text_f5 = kyprops.ObjectProperty(None)
    text_f6 = kyprops.ObjectProperty(None)
    text_f7 = kyprops.ObjectProperty(None)
    text_f8 = kyprops.ObjectProperty(None)
    text_f9 = kyprops.ObjectProperty(None)
    img_f0 = kyprops.ObjectProperty(None)
    img_f1 = kyprops.ObjectProperty(None)
    img_f2 = kyprops.ObjectProperty(None)
    img_f3 = kyprops.ObjectProperty(None)
    img_f4 = kyprops.ObjectProperty(None)
    img_f5 = kyprops.ObjectProperty(None)
    img_f6 = kyprops.ObjectProperty(None)
    img_f7 = kyprops.ObjectProperty(None)
    img_f8 = kyprops.ObjectProperty(None)
    img_f9 = kyprops.ObjectProperty(None)
    text2_f0 = kyprops.ObjectProperty(None)
    text2_f1 = kyprops.ObjectProperty(None)
    text2_f2 = kyprops.ObjectProperty(None)
    text2_f3 = kyprops.ObjectProperty(None)
    text2_f4 = kyprops.ObjectProperty(None)
    text2_f5 = kyprops.ObjectProperty(None)
    text2_f6 = kyprops.ObjectProperty(None)
    text2_f7 = kyprops.ObjectProperty(None)
    text2_f8 = kyprops.ObjectProperty(None)
    text2_f9 = kyprops.ObjectProperty(None)

    def on_enter(self, *args):
       self.weather_at_city(geo)

    def weather_at_city(self, city):
        city = Weather(city)
        city = city.weather()
        self.main = city['main']
        if self.main == 'Rain':
            sound = SoundLoader.load('Data/Sound//rain.mp3')
            sound.play()
        self.city_ti = city['city_ti']
        self.time_city_now = city['time_city_now']
        self.back = city['back']
        self.color = city['color']
        self.sost_w = city['sost']
        self.temp_w = city['temp']
        self.icon = city['icon']
        self.wind = city['wind']
        self.humidity = city['humidity']
        self.pressure = city['pressure']
        self.forecast_city = city['forecast_city']
        self.feels_like = city['feels_like']
        self.lat = city['lat']
        self.lon = city['lon']
        self.img.source = self.back
        self.map_btn.background_normal = city['map']
        self.map_btn.size_hint = (.175, .175 * Window.width / Window.height)
        self.time.text = self.time_city_now
        self.time.font_size = self.height / 22
        self.city.text = self.city_ti
        self.city.font_size = self.height / 42
        self.btn.font_size = self.height / 50
        self.sost.text = self.sost_w
        self.sost.font_size = self.height / 38
        self.temp.text = self.temp_w
        self.temp.font_size = self.height / 10
        self.prssr.text = self.pressure
        self.prssr.font_size = self.height / 53
        self.hmdt.text = self.humidity
        self.hmdt.font_size = self.height / 53
        self.wnd.text = self.wind
        self.wnd.font_size = self.height / 53
        self.btn_clothes.font_size = self.height / 53
        self.text_f0.text = self.forecast_city[0][0]
        self.text_f1.text = self.forecast_city[1][0]
        self.text_f2.text = self.forecast_city[2][0]
        self.text_f3.text = self.forecast_city[3][0]
        self.text_f4.text = self.forecast_city[4][0]
        self.text_f5.text = self.forecast_city[5][0]
        self.text_f6.text = self.forecast_city[6][0]
        self.text_f7.text = self.forecast_city[7][0]
        self.text_f8.text = self.forecast_city[8][0]
        self.text_f9.text = self.forecast_city[9][0]
        self.img_f0.source = self.forecast_city[0][2]
        self.img_f1.source = self.forecast_city[1][2]
        self.img_f2.source = self.forecast_city[2][2]
        self.img_f3.source = self.forecast_city[3][2]
        self.img_f4.source = self.forecast_city[4][2]
        self.img_f5.source = self.forecast_city[5][2]
        self.img_f6.source = self.forecast_city[6][2]
        self.img_f7.source = self.forecast_city[7][2]
        self.img_f8.source = self.forecast_city[8][2]
        self.img_f9.source = self.forecast_city[9][2]
        self.text2_f0.text = self.forecast_city[0][1]
        self.text2_f1.text = self.forecast_city[1][1]
        self.text2_f2.text = self.forecast_city[2][1]
        self.text2_f3.text = self.forecast_city[3][1]
        self.text2_f4.text = self.forecast_city[4][1]
        self.text2_f5.text = self.forecast_city[5][1]
        self.text2_f6.text = self.forecast_city[6][1]
        self.text2_f7.text = self.forecast_city[7][1]
        self.text2_f8.text = self.forecast_city[8][1]
        self.text2_f9.text = self.forecast_city[9][1]
        self.text_f0.font_size = self.height / 55
        self.text_f1.font_size = self.height / 55
        self.text_f2.font_size = self.height / 55
        self.text_f3.font_size = self.height / 55
        self.text_f4.font_size = self.height / 55
        self.text_f5.font_size = self.height / 55
        self.text_f6.font_size = self.height / 55
        self.text_f7.font_size = self.height / 55
        self.text_f8.font_size = self.height / 55
        self.text_f9.font_size = self.height / 55
        self.text2_f0.font_size = self.height / 45
        self.text2_f1.font_size = self.height / 45
        self.text2_f2.font_size = self.height / 45
        self.text2_f3.font_size = self.height / 45
        self.text2_f4.font_size = self.height / 45
        self.text2_f5.font_size = self.height / 45
        self.text2_f6.font_size = self.height / 45
        self.text2_f7.font_size = self.height / 45
        self.text2_f8.font_size = self.height / 45
        self.text2_f9.font_size = self.height / 45


    def get_city(self):
        global geo
        city = self.city.text
        geo = self.city.text
        self.weather_at_city(city)


        # print( sm.get_screen('menu_window').ids.btn.text)



        # self.weather_at_city(city)




class ClothesWindow(Screen):

    back = kyprops.ObjectProperty(None)
    arrow1 = kyprops.ObjectProperty(None)
    text1 = kyprops.ObjectProperty(None)
    arrow2 = kyprops.ObjectProperty(None)
    text2 = kyprops.ObjectProperty(None)
    male = kyprops.ObjectProperty(None)
    female = kyprops.ObjectProperty(None)
    slide = kyprops.ObjectProperty(None)
    clothe = kyprops.ObjectProperty(None)
    path = 'Data/Image/'
    def on_enter(self, *args):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{self.height//18}sp'
        self.text1.font_size = self.height / 20
        self.arrow2.icon_size = f'{self.height // 18}sp'
        self.text2.font_size = self.height / 20
        self.male.icon_size = f'{self.height//2}sp'
        self.female.icon_size = f'{self.height // 2}sp'


    def next1(self, text):
        self.manager.get_screen('clothes_window').slide.load_next(mode='next')
        self.path+=text
        self.gender = text

    def next2(self, text):

        self.manager.get_screen('clothes_window').slide.load_next(mode='next')
        self.path+=text + self.manager.get_screen('menu_window').feels_like
        self.path+= '//' + choice(os.listdir(self.path))
        self.clothe.background_normal = self.path

    def to_main_window(self):
        self.manager.get_screen('clothes_window').slide.load_previous()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_window'
        self.path = 'Data/Image/' + self.gender

    def back_to_gender(self):
        self.manager.get_screen('clothes_window').slide.load_previous()
        self.path = 'Data/Image/'



class Map(Screen):
    pass

class Place(Screen):
    back = kyprops.ObjectProperty(None)
    arrow1 = kyprops.ObjectProperty(None)
    text1 = kyprops.ObjectProperty(None)
    def on_enter(self, *args):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{self.height // 18}sp'
        self.text1.font_size = self.height / 20
class Weather(object):
    def __init__(self, city):
        self.city = city

    def weather(self):
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
            color = [[.44, .45, .47, 1], [.38, .39, .42, 1]]
            back = 'Data/Image/clouds.png'
            map = 'Data/Image//map1.png'
            map_press = 'Data/Image//map1_press.png'
        elif 6 <= int(time_city_now[0:2]) <= 10:
            color = [[.56, .61, .74, 1], [.55, .50, .48, 1]]
            back = 'Data/Image/morning.png'
            map = 'Data/Image//map1.png'
            map_press = 'Data/Image//map1_press.png'
        elif 0 <= int(time_city_now[0:2]) <= 5:
            color = [[.27, .29, .57, 1], [.31, .30, .53, 1]]
            back = 'Data/Image/night.png'
            map = 'Data/Image//map1.png'
            map_press = 'Data/Image//map1_press.png'
        elif 17 <= int(time_city_now[0:2]) <= 23:
            color = [[.27, .36, .49, 1], [.41, .39, .32, 1]]
            back = 'Data/Image/midnight.png'
            map = 'Data/Image//map.png'
            map_press = 'Data/Image//map_press.png'
        elif 11 <= int(time_city_now[0:2]) <= 16:
            color = [[.28, .38, .75, 1], [.36, .46, .69, 1]]
            back = 'Data/Image//afternoon.png'
            map = 'Data/Image//map1.png'
            map_press = 'Data/Image//map1_press.png'
        # предсказание погоды 3ч
        forecast_city = {}
        for i in range(10):
            forecast_time = str(datetime.strptime(forecast['list'][i]['dt_txt'], '%Y-%m-%d %H:%M:%S').replace(
                tzinfo=timezone(timedelta(hours=0))).astimezone(tz=time_city))
            forecast_time = '{}.{}\n{}'.format(forecast_time[8:10], forecast_time[5:7], forecast_time[11:16])
            forecast_city[i] = [forecast_time, '{}°C'.format(round(forecast['list'][i]['main']['temp'])),
                                'Data/Image/{}.png'.format(forecast['list'][i]['weather'][0]['icon'])]

        self.a = {'city_ti': city_ti, 'time_city_now': time_city_now, 'sost': sost, 'icon': icon, 'temp': temp,
                  'wind': wind,
                  'humidity': humidity,
                  'pressure': pressure, 'color': color, 'back': back, 'forecast_city': forecast_city, 'main': main,
                   'feels_like': feels_like_txt, 'map': map, 'map_press': map_press,
                  'lat': weather['coord']['lat'], 'lon': weather['coord']['lon']}

        return self.a
# try:
#     def print_locations(**kwargs):
#         print('lat: {lat}, lon: {lon}'.format(**kwargs))
#
#
#     gps.configure(on_location=print_locations)
#     gps.start()
#     gps.stop()
# except:

Window.size = (416 // 1, 901 // 1)



class MainApp(MDApp):

    def on_start(self):
        global  geo
        geo = requests.get('https://ipinfo.io/json').json()
        geo = geo['loc'].split(',')
        # Clock.schedule_once(lambda x: exec("root.current ='manager'"), 5)


    def build(self):
        self.theme_cls.theme_style = "Dark"
        global sm
        sm_file = Builder.load_file('manager.kv')
        sm = ScreenManager()
        sm.add_widget(Loading(name='loading'))
        sm.add_widget(LogIn(name='log_in'))
        sm.add_widget(MenuWindow(name='menu_window'))
        sm.add_widget(ClothesWindow(name='clothes_window'))
        sm.add_widget(Map(name='map'))
        sm.add_widget(Place(name='place'))

        return sm_file



if __name__ == '__main__':
    MainApp().run()
