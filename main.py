from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
import requests
from datetime import datetime, timezone, timedelta
# from plyer import gps
import os
from random import choice
import webbrowser



class LogIn(Screen):
    def __init__(self,  **kwargs):
        super(LogIn, self).__init__(**kwargs)


    def on_enter(self):
        fl = FloatLayout()
        img = Image(source = 'Data/Image//log in.png')
        fl.add_widget(img)
        bl = BoxLayout(orientation="vertical", size_hint=(.8, .18), pos_hint={'x': .1, 'y': .395}, spacing=8)
        fl.add_widget(Label(
            text = 'Вход',
            font_size=Window.height / 30,
            pos_hint={'x': .020, 'y': .1},
            color = 'black'

        ))
        self.email = TextInput(multiline=False, hint_text='Email', font_size=Window.height / 50, background_normal = '')
        self.password = TextInput(multiline=False, hint_text='Пароль', font_size=Window.height / 50, password = True, background_normal = '')
        bl.add_widget(self.email)
        bl.add_widget(self.password)
        bl.add_widget(Button(
            text = 'ВОЙТИ',
            font_size=Window.height / 40,
            background_normal = '',
            background_color = [.62, .60, .64]
        ))
        bl.add_widget(Button(
            text='ЗАРЕГИСТРИРОВАТЬСЯ',
            font_size=Window.height / 40,
            background_normal="Data/Image//button.png",
            color='black',
            on_press=lambda x:
            set_screen_l('sign_up'),
        ))
        fl.add_widget(Button(
            text = 'Пропустить',
            font_size=Window.height / 60,
            size_hint=(.3, .05),
            pos_hint={'x': .66, 'y': .36},
            background_normal="Data/Image//button.png",
            color='gray',
            on_press=lambda x:
            set_screen_l('menu_window'),
        ))
        fl.add_widget(bl)
        self.add_widget(fl)

class SignUp(Screen):
    def __init__(self,  **kwargs):
        super(SignUp, self).__init__(**kwargs)

    def on_enter(self):
        fl = FloatLayout()
        img = Image(source = 'Data/Image//sign up.png')
        fl.add_widget(img)
        bl = BoxLayout(orientation="vertical", size_hint=(.8, .25), pos_hint={'x': .1, 'y': .33}, spacing=8)
        fl.add_widget(Label(
            text = 'Регистрация',
            font_size=self.height / 35,
            pos_hint={'x': .020, 'y': .11},
            color = 'black'

        ))
        self.name_user = TextInput(multiline=False, hint_text='Имя', font_size=self.height / 50, background_normal = '')
        self.lstname = TextInput(multiline=False, hint_text='Фамилия', font_size=self.height / 50, background_normal = '')
        self.email = TextInput(multiline=False, hint_text='Email', font_size=self.height / 50, background_normal = '')
        self.password = TextInput(multiline=False, hint_text='Пароль', font_size=self.height / 50, password = True, background_normal = '')
        self.ppassword = TextInput(multiline=False, hint_text='Повторите пароль', font_size=self.height / 50, password = True, background_normal = '')
        bl.add_widget(self.name_user)
        bl.add_widget(self.lstname)
        bl.add_widget(self.email)
        bl.add_widget(self.password)
        bl.add_widget(self.ppassword)

        bl.add_widget(Button(
            text='ЗАРЕГИСТРИРОВАТЬСЯ',
            font_size=self.height / 40,
            background_normal="Data/Image//button.png",
            color='black',
            on_press = self.check_inf
        ))
        fl.add_widget(Button(
            on_press=lambda x: set_screen_r('log_in'),
            background_normal="Data/Image//pointer.png",
            background_down="Data/Image//pointer.png",
            size_hint=(.18, .0783),
            pos_hint={'x': .03, 'y': .92},
        ))
        fl.add_widget(bl)

        self.add_widget(fl)


    def check_inf(self, instance):
        if self.password.text!=self.ppassword.text:
            self.ppassword.background_color = [1, .33, .33]
            self.ppassword.text=''
            self.ppassword.hint_text = 'Пароли не совпадают'
        else:
            self.ppassword.background_color = 'white'
            self.user_information()


    def user_information(self):
        user_inf = {'name': self.name_user.text, 'last_name': self.lstname.text, 'email': self.email.text, 'password':self.password.text}
        print(user_inf)
        set_screen_l('menu_window')





class MenuWindow(Screen, object):

    def __init__(self, city, **kwargs):
        super(MenuWindow, self).__init__(**kwargs)

        self.size = Window.size
        self.weather_at_city(city)

    def weather_at_city(self, city):
        a = Weather(city)
        a = a.weather()
        self.main = a['main']
        self.city_ti = a['city_ti']
        self.time_city_now = a['time_city_now']
        self.back = a['back']
        self.color = a['color']
        self.sost = a['sost']
        self.temp = a['temp']
        self.icon = a['icon']
        self.wind = a['wind']
        self.humidity = a['humidity']
        self.pressure = a['pressure']
        self.forecast_city = a['forecast_city']
        self.feels_like = a['feels_like']
        self.lat = a['lat']
        self.lon = a['lon']
        fl = FloatLayout()
        bl = BoxLayout(orientation="vertical", size_hint=(.35, .15), pos_hint={'x': .325, 'y': .825}, spacing=8)
        if self.main == 'Rain':
            sound = SoundLoader.load('Data/Sound//rain.mp3')
            sound.play()
        bl.add_widget(Label(
            text=self.time_city_now,
            font_size=self.height / 22,

        ))

        self.text_input = TextInput(multiline=False, text=self.city_ti, font_size=self.height / 45)

        bl.add_widget(self.text_input)  # позиция
        self.img = Image(source=self.back)
        fl.add_widget(self.img)
        bl.add_widget(Button(
            text='Узнать погоду',
            font_size=self.height / 42,  # font_size рaзмер шрифта
            on_press=self.get_city,  # on_press нажата
            # background_color цвет RGBA в %
            background_normal="Data/Image//button.png",  # background_normal  делает цвет ярче
        ))  # позиция

        fl.add_widget(bl)
        bl2 = BoxLayout(orientation="vertical", size_hint=(.3, .1), pos_hint={'x': .35, 'y': .60}, spacing=30)
        bl2.add_widget(Label(
            text=self.sost,
            font_size=self.height / 38
        ))
        bl2.add_widget(Label(
            text=self.temp,
            font_size=self.height / 10,
        ))
        fl.add_widget(bl2)
        gl = GridLayout(cols=2, size_hint=(.8, .32), pos_hint={'x': .18, 'y': .147})
        gl.add_widget(Label(
            text=self.pressure,
            font_size=self.height / 50
        ))
        gl.add_widget(Label(
            text=self.humidity,
            font_size=self.height / 50
        ))
        gl.add_widget(Label(
            text=self.wind,
            font_size=self.height / 50
        ))
        fl.add_widget(Button(
            text='Рекомендуемая \nодежда',
            size_hint=(.3, .05),
            pos_hint={'x': .66, 'y': .2048},
            on_press=lambda x:
            set_screen_l('clothes_window'),
            font_size=self.height / 50,
            background_normal="Data/Image//button.png",
            background_down="Data/Image//button.png"
        ))
        fl.add_widget(Button(
            size_hint=(.175, .175 * Window.width / Window.height),
            pos_hint={'x': .78, 'y': .9},
            on_press=lambda x:
            set_screen_l('map'),
            background_normal=a['map'],
            background_down=a['map_press']
        ))
        layout = GridLayout(cols=10, spacing=Window.width / 500, size_hint_x=None)
        layout.bind(minimum_width=layout.setter('width'))
        for i in range(10):
            layout.add_widget(Label(
                text=self.forecast_city[i][0], size_hint_x=None,
                font_size=self.height / 55
            ))
        for i in range(10):
            img = Image(source=self.forecast_city[i][2])
            layout.add_widget(img)
        for i in range(10):
            layout.add_widget(Label(
                text=self.forecast_city[i][1],
                font_size=self.height / 45
            ))

        al = FloatLayout(size_hint=(1, .17))
        sv = ScrollView(size_hint=(None, 1), size=(Window.width, Window.height))
        sv.add_widget(layout)
        al.add_widget(sv)
        fl.add_widget(al)
        fl.add_widget(gl)
        self.add_widget(fl)

    def get_city(self, instance):
        city = self.text_input.text
        self.weather_at_city(city)


class ClothesWinwow(Screen):
    def __init__(self, **kw):
        super(ClothesWinwow, self).__init__(**kw)

    def on_enter(self):
        self.back = sm.get_screen('menu_window').back[:-4] + '1.png'
        self.back2 = sm.get_screen('menu_window').back[:-4] + '2.png'
        fl = FloatLayout()
        img = Image(source=self.back)
        fl.add_widget(img)
        fl.add_widget(Label(
            text='Выберете пол',
            font_size=self.height / 20,
            pos_hint={'x': .02, 'y': .4}
        ))
        bl = BoxLayout(size_hint=(1, .6), pos_hint={'x': 0, 'y': .15})
        bl.add_widget(Button(
            on_press=self.man,
            background_normal='Data/Image/man.png',
            background_down='Data/Image/man_press.png'
        ))
        bl.add_widget(Button(
            on_press=self.woman,
            background_normal='Data/Image/woman.png',
            background_down='Data/Image/woman_press.png'
        ))
        fl.add_widget(bl)
        self.add_widget(fl)

    def man(self, instance):
        self.way = 'Data/Image//man'
        self.style()

    def woman(self, instance):
        self.way = 'Data/Image//woman'
        self.style()

    def style(self):
        fl = FloatLayout()
        img = Image(source=self.back2)
        fl.add_widget(img)
        fl.add_widget(Label(
            text='Выберете стиль',
            font_size=self.height / 20,
            pos_hint={'x': .02, 'y': .4}
        ))
        bl = BoxLayout(orientation='vertical', size_hint=(.5, .5), pos_hint={'x': .25, 'y': .25})
        bl.add_widget(Button(
            text='classic',
            on_press=self.classic,
            background_normal="Data/Image//button.png",
        ))
        bl.add_widget(Button(
            text='casual',
            on_press=self.casual,
            background_normal="Data/Image//button.png",
        ))
        bl.add_widget(Button(
            text='sport',
            on_press=self.sport,
            background_normal="Data/Image//button.png",
        ))
        fl.add_widget(bl)
        self.add_widget(fl)

    def classic(self, instance):
        self.way += '/classic//'
        self.clothe_img()

    def casual(self, instance):
        self.way += '/casual//'
        self.clothe_img()

    def sport(self, instance):
        self.way += '/sport//'
        self.clothe_img()

    def clothe_img(self):
        self.way += sm.get_screen('menu_window').feels_like
        fl = FloatLayout()
        fl.add_widget(Button(
            on_press=lambda x: set_screen_r('menu_window'),
            background_normal=self.way + '//' + choice(os.listdir(self.way))
        ))
        self.add_widget(fl)


class Map(Screen):

    def __init__(self, **kwargs):
        super(Map, self).__init__(**kwargs)

    def on_enter(self):
        self.back = sm.get_screen('menu_window').back[:-4] + '1.png'
        self.build = 'Data/Image//build.png'
        self.geo = {'lat': sm.get_screen('menu_window').lat, 'lon': sm.get_screen('menu_window').lon}
        fl = FloatLayout()
        gl = GridLayout(cols=2, size_hint=(.8, .32), pos_hint={'x': .18, 'y': .32}, spacing=Window.height // 10)
        img = Image(source=self.back)
        fl.add_widget(img)
        img = Image(source=self.build)
        fl.add_widget(img)
        fl.add_widget(Label(
            text='Выберете категорию',
            font_size=self.height / 25,
            pos_hint={'x': .02, 'y': .4}
        ))
        gl.add_widget(Button(
            text='Кинотеатр',
            on_press=self.cinema,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42
        ))
        gl.add_widget(Button(
            text='Парк',
            on_press=self.park,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42

        ))
        gl.add_widget(Button(
            text='Кафе',
            on_press=self.cafe,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42

        ))
        gl.add_widget(Button(
            text='Бар',
            on_press=self.bar,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42

        ))
        gl.add_widget(Button(
            text='Ресторан',
            on_press=self.restaurant,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42

        ))
        gl.add_widget(Button(
            text='Отель',
            on_press=self.hotel,
            background_normal="Data/Image//button.png",
            font_size=self.height / 42

        ))
        fl.add_widget(Button(
            on_press=lambda x: set_screen_r('menu_window'),
            background_normal="Data/Image//pointer.png",
            background_down="Data/Image//pointer.png",
            size_hint=(.18, .0783),
            pos_hint={'x': .03, 'y': .92},

        ))
        fl.add_widget(gl)
        self.add_widget(fl)

    def cinema(self, instance):
        geo_place = GeoLoc(self.geo, 'кинотеатр')
        self.place = geo_place.location()
        self.build_img = "Data/Image//cinema.png"
        set_screen_l('place')

    def park(self, instance):
        geo_place = GeoLoc(self.geo, 'парк')
        self.place = geo_place.location()
        self.build_img = "Data/Image//park.png"
        set_screen_l('place')

    def cafe(self, instance):
        geo_place = GeoLoc(self.geo, 'кафе')
        self.place = geo_place.location()
        self.build_img = "Data/Image//cafe.png"
        set_screen_l('place')

    def bar(self, instance):
        geo_place = GeoLoc(self.geo, 'бар')
        self.place = geo_place.location()
        self.build_img = "Data/Image//bar.png"
        set_screen_l('place')

    def restaurant(self, instance):
        geo_place = GeoLoc(self.geo, 'ресторан')
        self.place = geo_place.location()
        self.build_img = "Data/Image//restaurant.png"
        set_screen_l('place')

    def hotel(self, instance):
        geo_place = GeoLoc(self.geo, 'отель')
        self.place = geo_place.location()
        self.build_img = "Data/Image//hotel.png"
        set_screen_l('place')


class Place(Screen):

    def __init__(self, **kw):
        super(Place, self).__init__(**kw)
        self.numb = 0

    def on_enter(self):
        self.back = sm.get_screen('menu_window').back[:-4] + '1.png'
        self.build_img = sm.get_screen('map').build_img
        if self.numb == 5:
            self.numb = 4
        elif self.numb == -6:
            self.numb = -5
        fl = FloatLayout()
        img = Image(source=self.back)
        fl.add_widget(img)
        img = Image(source=self.build_img, pos_hint={'x': .005, 'y': .42})
        fl.add_widget(img)
        place = sm.get_screen('map').place
        bl = BoxLayout(orientation='horizontal', size_hint=(.9, .07), pos_hint={'x': .05, 'y': .25})
        bl.add_widget(Button(
            on_press=self.minus,
            background_normal="Data/Image//pointer1.png"

        ))
        bl.add_widget(Button(
            on_press=self.plus,
            background_normal="Data/Image//pointer2.png"
        ))
        name = place["features"][self.numb]["properties"]["CompanyMetaData"]["name"].split()
        address = place["features"][self.numb]["properties"]["CompanyMetaData"]["address"].split(', ')
        del address[0]
        address = '\n    '.join(address)
        try:
            hours = place["features"][self.numb]["properties"]["CompanyMetaData"]["Hours"]["text"].split('; ')
            hours = '\n    '.join(hours)
        except:
            hours = 'информация отсутствует'
        try:
            self.url = place["features"][self.numb]["properties"]["CompanyMetaData"]["url"]
        except:
            self.url = ''
        place_inf = f'Адрес:\n    {address}\nРасписание:\n    {hours}'
        fl.add_widget(Label(
            text=place_inf,
            font_size=self.height / 50,
        ))
        fl.add_widget(bl)
        bl = BoxLayout(orientation='vertical', size_hint=(.35, .15), pos_hint={'x': .325, 'y': .7})
        for i in range(len(name)):
            bl.add_widget(Label(
                text=name[i],
                font_size=self.height / 22
            ))
        fl.add_widget(bl)
        if self.url !='':
            fl.add_widget(Button(
                text = 'Перейти на сайт',
                on_press = self.link,
                font_size=self.height / 30,
                background_normal="Data/Image//button.png",
                background_down="Data/Image//button.png",
                size_hint=(.2, .2),
                pos_hint={'x': .4, 'y': .008},
            ))
        fl.add_widget(Button(
            on_press=lambda x: set_screen_r('map'),
            background_normal="Data/Image//pointer.png",
            background_down="Data/Image//pointer.png",
            size_hint=(.18, .0783),
            pos_hint={'x': .03, 'y': .92},

        ))
        self.add_widget(fl)

    def plus(self, instance):
        self.numb += 1
        self.on_enter()

    def minus(self, instance):
        self.numb -= 1
        self.on_enter()

    def link(self, instance):
        webbrowser.open(self.url)


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


class GeoLoc(object):
    def __init__(self, geoloc, place):
        self.geoloc = geoloc
        self.place = place

    def location(self):
        key = '2d3a7435-6798-428d-908b-31d615333bba'
        url = 'https://search-maps.yandex.ru/v1/'
        param = {'apikey': key, 'text': self.place, 'lang': 'ru_RU', 'll': f'{self.geoloc["lon"]},{self.geoloc["lat"]}',
                 'spn': '0.552069,0.400552',
                 'results': 5, }
        mas = requests.get(url, params=param).json()
        return mas


def set_screen_r(name_screen):
    sm.transition.direction = 'right'
    sm.current = name_screen

def set_screen_l(name_screen):
    sm.transition.direction = 'left'
    sm.current = name_screen


# try:
#     def print_locations(**kwargs):
#         print('lat: {lat}, lon: {lon}'.format(**kwargs))
#
#
#     gps.configure(on_location=print_locations)
#     gps.start()
#     gps.stop()
# except:
geo = requests.get('https://ipinfo.io/json').json()
geo = geo['loc'].split(',')
Window.size = (416 // 1, 901 // 1)



class MainApp(App):

    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(LogIn(name='log_in'))
        sm.add_widget(SignUp(name='sign_up'))
        sm.add_widget(MenuWindow(name='menu_window', city=geo))
        sm.add_widget(ClothesWinwow(name='clothes_window'))
        sm.add_widget(Map(name='map'))
        sm.add_widget(Place(name='place'))
        return sm


if __name__ == '__main__':
    MainApp().run()
