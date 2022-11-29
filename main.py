from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
import kivy.properties as kyprops
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy_garden.xcamera import XCamera
import requests, re, json, os
# from plyer import gps
from hashlib import pbkdf2_hmac
from random import choice
from kivy.input.motionevent import MotionEvent
from kivymd.uix.button import MDFlatButton
from kivymd.uix.fitimage import FitImage

from client import Client
from kivymd.uix.snackbar import Snackbar
from kivy.core.text import LabelBase
from GeoLoc import GeoLoc
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import IconLeftWidget
# LabelBase.register(name = 'Mirava Personal Use Only',  fn_regular='MiravaRegularPersonalUseOnl.ttf')
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class Loading(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.login, 2)

    def login(self, *args):
        self.manager.get_screen('menu_window').weather_at_city(geo)
        self.manager.get_screen('sign_in').enter()
        self.manager.current = 'sign_in'


class SignIn(Screen):

    def enter(self):
        # back = 'Data/Image/loading '+ self.manager.get_screen('menu_window').ids.img.source[11:]
        color =''
        self.entry.font_size = Window.height / 24
        self.email.font_size = Window.height / 50
        self.password.font_size = Window.height / 50
        self.next_btn.font_size = Window.height / 40
        self.previous_btn.font_size = Window.height / 40
        self.log_in_btn.font_size = Window.height / 40
        self.sign_up_btn.font_size = Window.height / 40
        self.frgt_password.font_size = Window.height / 48
        self.skip.font_size = Window.height / 48
        self.back.source = back
        self.card.md_bg_color = color_card
        self.manager.get_screen('sign_up').enter()

    def next(self):
        self.salt = Client(operation='get_salt', email=self.email.text)
        self.salt.start()
        self.salt = self.salt.task()
        if self.salt == 'None':
            Snackbar(
                text="  Введите корректный Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
        else:
            self.manager.get_screen('sign_in').slide.load_next(mode='next')

    def log_in_information(self):
        password = self.manager.get_screen('sign_in').ids.password.text.encode()
        password = pbkdf2_hmac('sha256', password, self.salt.encode('utf-8'), 10000)
        log_in = Client(operation='log_in',
                        email=self.email.text,
                        password=password.hex()
                        )
        log_in.start()
        log_in = log_in.task()
        if log_in == 'null':
            Snackbar(
                text="  Неправильный пароль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
        else:
            self.manager.current = 'menu_window'
            self.manager.transition.direction = 'left'

    def previous(self):
        self.manager.get_screen('sign_in').slide.load_previous()


class SignUp(Screen):

    def enter(self):
        self.frst_name.font_size = Window.height / 50
        self.last_name.font_size = Window.height / 50
        self.next_btn1.font_size = Window.height / 45
        self.next_btn2.font_size = Window.height / 45
        self.next_btn3.font_size = Window.height / 45
        self.sign_in_btn.font_size = Window.height / 45
        self.previous_btn1.font_size = Window.height / 45
        self.previous_btn2.font_size = Window.height / 45
        self.num1.icon_size = f'{Window.height // 25}sp'
        self.num2.icon_size = f'{Window.height // 25}sp'
        self.num3.icon_size = f'{Window.height // 25}sp'
        self.manager.get_screen('email_confirmation').enter()

    def next1(self):
        if len(self.frst_name.text) != 0 and len(self.last_name.text) != 0:
            self.num1.icon = 'checkbox-marked-circle'
            self.manager.get_screen('sign_up').slide.load_next(mode='next')
            self.progressbar1.value = 100
            self.num1.icon_color = '#309AEB'
        elif len(self.frst_name.text) == 0:
            Snackbar(
                text="  Введите имя",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
        elif len(self.last_name.text) == 0:
            Snackbar(
                text="  Введите фамилию",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()

    def next2(self):
        if len(self.email.text) != 0 and len(self.number.text) != 0 and re.fullmatch(regex, self.email.text):
            requests_email = Client(operation='email_in_db', email=self.email.text)
            requests_email.start()
            self.task = requests_email.task()
            if self.task == 'None':
                self.num2.icon = 'checkbox-marked-circle'
                self.num2.icon_color = '#309AEB'
                self.progressbar2.value = 100
                self.manager.get_screen('sign_up').slide.load_next(mode='next')
            else:
                Snackbar(
                    text="На этот Email уже зарегистрирован аккаунт",
                    snackbar_animation_dir='Top',
                    bg_color='#CF5A5D',
                    shadow_color='#CF5A5D',
                    font_size=Window.height // 53,
                    snackbar_x=f"{Window.height // 44}dp",
                    snackbar_y=f"{Window.height // 1.1}dp",
                    size_hint_x=.9,
                    radius=[20, 20, 20, 20]
                ).open()
        elif len(self.email.text) == 0:
            Snackbar(
                text="  Введите Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
        elif not re.fullmatch(regex, self.email.text):
            Snackbar(
                text="  Введите корректный Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()

        elif len(self.number.text) == 0:
            Snackbar(
                text="  Введите номер телефона",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()

    def next3(self):
        if len(self.password.text) != 0 and len(
                self.repeat_password.text) != 0 and self.password.text == self.repeat_password.text:
            self.num3.icon = 'checkbox-marked-circle'
            self.num3.icon_color = '#309AEB'
            self.manager.get_screen('sign_up').slide.load_next(mode='next')
            self.manager.transition.direction = 'left'
            self.manager.current = 'email_confirmation'
        elif len(self.password.text) == 0:
            Snackbar(
                text="  Введите пароль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
        elif self.password.text != self.repeat_password.text:
            Snackbar(
                text="  Пароли не совпадают",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
            self.password.text = ''
            self.repeat_password.text = ''

    def previous1(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'sign_in'

    def previous2(self):
        self.num1.icon = 'numeric-1-circle'
        self.num1.icon_color = 'white'
        self.progressbar1.value = 0
        self.manager.get_screen('sign_up').slide.load_previous()

    def previous3(self):

        self.num2.icon = 'numeric-2-circle'
        self.num2.icon_color = 'white'
        self.progressbar2.value = 0
        self.manager.get_screen('sign_up').slide.load_previous()


class EmailConfirmation(Screen):
    def enter(self):
        self.email_conf.font_size = Window.height / 28
        self.text.font_size = Window.height / 58
        self.send_code.font_size = Window.height / 45
        self.return_to_sign_up.font_size = Window.height / 45

    def on_enter(self, *args):
        code = Client(operation='send_code',
                      email=self.manager.get_screen('sign_up').ids.email.text)
        code.start()
        self.code = code.task()

    def checking_code(self):
        if self.conf_code.text == self.code:
            salt = os.urandom(12).hex()
            password = self.manager.get_screen('sign_up').ids.password.text.encode()
            password = pbkdf2_hmac('sha256', password, salt.encode('utf-8'), 10000, )
            user_inf = Client(operation='user_inf',
                              email=self.manager.get_screen('sign_up').ids.email.text,
                              first_name=self.manager.get_screen('sign_up').ids.frst_name.text,
                              last_name=self.manager.get_screen('sign_up').ids.last_name.text,
                              phone_number=self.manager.get_screen('sign_up').ids.number.text,
                              password=password.hex(),
                              salt=salt
                              )
            user_inf.start()
            self.manager.current = 'sign_in'
            self.manager.transition.direction = 'right'
        else:
            Snackbar(
                text="  Неправильный код",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()


class MenuWindow(Screen):

    def weather_at_city(self, city):
        city = Client(operation='weather', city=city)
        city.start()
        city = json.loads(city.task())
        if city == 'None':
            Snackbar(
                text="  Информация отсутствует",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x=f"{Window.height // 44}dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                size_hint_x=.9,
                radius=[20, 20, 20, 20]
            ).open()
            self.city.text = self.city_ti
        else:
            self.main = city['main']
            if self.main == 'Rain':
                sound = SoundLoader.load('Data/Sound//rain.mp3')
                sound.play()
            self.city_ti = city['city_ti']
            self.time_city_now = city['time_city_now']
            self.back = city['back']
            self.lat.text = str(city['lat'])
            self.lon.text = str(city['lon'])
            self.color = city['color_card']
            self.sost_w = city['sost']
            self.temp_w = city['temp']
            self.icon = city['icon']
            self.wind = city['wind']
            self.humidity = city['humidity']
            self.pressure = city['pressure']
            self.forecast_city = city['forecast_city']
            self.feels_like = city['feels_like']
            self.img.source = self.back
            self.map_btn.background_normal = city['map']
            self.map_btn.background_down = city['map_press']
            self.map_btn.size_hint = (.175, .175 * Window.width / Window.height)
            self.time.text = self.time_city_now
            self.time.font_size = Window.height / 22
            self.city.text = self.city_ti
            self.city.font_size = Window.height / 42
            self.btn.font_size = Window.height / 50
            self.sost.text = self.sost_w
            self.sost.font_size = Window.height / 38
            self.temp.text = self.temp_w
            self.temp.font_size = Window.height / 10
            self.prssr.text = self.pressure
            self.prssr.font_size = Window.height / 53
            self.hmdt.text = self.humidity
            self.hmdt.font_size = Window.height / 53
            self.wnd.text = self.wind
            self.wnd.font_size = Window.height / 53
            self.btn_clothes.font_size = Window.height / 53
            self.menu.icon_size = f'{Window.height // 23}sp'
            global back, color_card
            back = 'Data/Image/loading '+ self.back[11:]
            color_card = city['color_card']


            for i in range(10):
                self.gl.add_widget(MDLabel(
                    size_hint_x= None,
                    halign =  'center',
                    text = self.forecast_city[i][0],
                    font_size = Window.height / 55
                ))
            for i in range(10):
                self.gl.add_widget(Image(
                    source = self.forecast_city[i][2]
                ))
            for i in range(10):
                self.gl.add_widget(MDLabel(
                    size_hint_x= None,
                    halign =  'center',
                    text = self.forecast_city[i][1],
                    font_size = Window.height / 45
                ))
            self.manager.get_screen('library_selection').enter()
            self.manager.get_screen('my_clothes_window').enter()
            self.manager.get_screen('clothes_window').enter()
            self.manager.get_screen('place').enter()

    def get_city(self):
        city = self.city.text
        self.gl.clear_widgets()
        self.manager.get_screen('place').ids.box.clear_widgets()
        self.manager.get_screen('place').ids.fl.clear_widgets()
        self.manager.get_screen('place').ids.search.background_normal ="Data/Image//search.png"
        self.manager.get_screen('place').ids.search.background_down ="Data/Image//search.png"
        self.manager.get_screen('place').ids.text1.text ='Выберете категорию'

        self.weather_at_city(city)

        # print( sm.get_screen('menu_window').ids.btn.text)

        # self.weather_at_city(city)


class LibrarySelection(Screen):
    def enter(self):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{Window.height // 18}sp'
        self.text.font_size = Window.height / 22


class MyClothesWindow(Screen):
    def enter(self):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{Window.height // 18}sp'
        self.camera.icon_size = f'{Window.height // 22}sp'
        self.text.font_size = Window.height / 20


class ClothesWindow(Screen):
    path = 'Data/Image/'

    def enter(self):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{Window.height // 18}sp'
        self.text1.font_size = Window.height / 20
        self.arrow2.icon_size = f'{Window.height // 18}sp'
        self.text2.font_size = Window.height / 20
        self.male.icon_size = f'{Window.height // 2}sp'
        self.female.icon_size = f'{Window.height // 2}sp'

    def next1(self, text):
        self.manager.get_screen('clothes_window').slide.load_next(mode='next')
        self.path += text
        self.gender = text

    def next2(self, text):
        self.manager.get_screen('clothes_window').slide.load_next(mode='next')
        self.path += text + self.manager.get_screen('menu_window').feels_like
        self.path += '//' + choice(os.listdir(self.path))
        self.clothe.background_normal = self.path

    def to_main_window(self):
        self.manager.get_screen('clothes_window').slide.load_previous()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu_window'
        self.path = 'Data/Image/' + self.gender

    def back_to_gender(self):
        self.manager.get_screen('clothes_window').slide.load_previous()
        self.path = 'Data/Image/'


class CameraScreen(Screen):
    def enter(self):
        self.arrow1.icon_size = f'{Window.height // 18}sp'
        self.take_photo.icon_size = f'{Window.height // 12}sp'
        self.image_btn.icon_size = f'{Window.height // 22}sp'

    def on_enter(self, *args):
        self.camera.play = True
    pass


class Place(Screen):
    def enter(self):
        self.back.source = self.manager.get_screen('menu_window').ids.img.source[:-4] + '1.png'
        self.arrow1.icon_size = f'{Window.height // 18}sp'
        self.search.size_hint=  (.2, .2 * Window.width / Window.height)
        self.text1.font_size = Window.height / 20
        zoom = 15

        self.brock.add_widget(FitImage(
            source='Data/Image/Brock.png'
        ))


    def on_enter(self, *args):
        pass
        # self.map.lat = int(sm.get_screen('menu_window').lat)
        # self.map.lon = int(sm.get_screen('menu_window').lon)
    def category(self):
        category_menu = {
            'Кинотеатры': ["Data/Image//cinema.png", 'filmstrip-box'],
            "Парки":["Data/Image//park.png", 'tree'],
            "Кафе":["Data/Image//cafe.png", 'coffee'],
            "Бары":["Data/Image//bar.png", 'beer'],
            "Рестораны": ["Data/Image//restaurant.png", 'silverware-variant'],
            "Отели":["Data/Image//hotel.png", 'bed'],

        }
        category = MDListBottomSheet(
            bg_color = color_card,
            radius_from='top',

            size_hint = (1, 1)

        )
        for item in category_menu.items():
            category.add_item(
                text= item[0],
                callback= lambda x, y = item[0], z = item[1]: self.category_menu_press(y,z),
                icon =  item[1][1],

            )
        category.open()
    def category_menu_press(self, name, path):
        self.fl.clear_widgets()
        self.map = MapView(
            size_hint=(.8, .5),
            pos_hint={'center_x': .5, 'center_y': .4},
            lat=self.manager.get_screen('menu_window').ids.lat.text,
            lon=self.manager.get_screen('menu_window').ids.lon.text,
            zoom=15,
        )
        self.brock.clear_widgets()
        self.box.clear_widgets()
        self.text1.text = name
        self.search.background_normal = path[0]
        self.search.background_down = path[0]
        self.geo = [self.manager.get_screen('menu_window').ids.lat.text, self.manager.get_screen('menu_window').ids.lon.text]
        places = GeoLoc(self.geo, name).location()
        for i in range(len(places)):
            self.map.add_widget(MapMarkerPopup(lat = places[i]['coordinates'][0], lon = places[i]['coordinates'][1]))
            self.box.add_widget(MDExpansionPanel(
                content = Content(places[i]['address'], places[i]['hours']).enter(),
                panel_cls=MDExpansionPanelOneLine(text=places[i]['name']),
            ))

        self.fl.add_widget(self.map)

    def segmented_control(self, widget, pos, *args):
        animation = Animation(pos_hint = {'center_x': pos}, duration= 0.2)
        animation.start(widget)


class Map(Screen):
    pass
    # def enter(self):
    #     # places = GeoLoc(geo, 'кинотеатр').location()
    #     # for i in range (5):
    #     #     name = places["features"][i]["properties"]["CompanyMetaData"]["name"]
    #     #     address = places["features"][i]["properties"]["CompanyMetaData"]["address"].split(', ')
    #     #     del address[0]
    #     #     address = ', '.join(address)
    #     #     try:
    #     #         hours = places["features"][i]["properties"]["CompanyMetaData"]["Hours"]["text"].split('; ')
    #     #         hours = '\n    '.join(hours)
    #     #     except:
    #     #         hours = 'информация отсутствует'
    #     #     try:
    #     #         self.url = places["features"][i]["properties"]["CompanyMetaData"]["url"]
    #     #     except:
    #     #         self.url = ''
    #     #     print(name, address, hours, self.url)
    #     pass


class Content(object):
    dialog1 = None
    dialog2 = None
    def __init__(self, address, schedule):
        self.address = address
        self.schedule = schedule
    def enter(self):
        bl = MDBoxLayout(orientation='vertical', adaptive_height=True)
        item1 = TwoLineIconListItem(text='Адрес', secondary_text=self.address,
                                    on_release=lambda x, y=self.address: self.on_release_1(y))
        item1.add_widget(IconLeftWidget(
            icon="map-marker-path"
        ))
        bl.add_widget(item1)
        item2 = TwoLineIconListItem(text='Расписание', secondary_text=self.schedule,
                                    on_release=lambda x, y=self.schedule: self.on_release_2(y))
        item2.add_widget(IconLeftWidget(
            icon="clock"
        ))
        bl.add_widget(item2)
        return bl
    def on_release_1(self, text):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title = 'Адрес',
                text=text,

            )
        self.dialog1.open()
    def on_release_2(self, text):
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title = 'Расписание',
                text=text,


            )
        self.dialog2.open()
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
        global geo
        geo = requests.get('https://ipinfo.io/json').json()
        geo = geo['loc'].split(',')
        # Clock.schedule_once(lambda x: exec("root.current ='manager'"), 5)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        global sm
        sm_file = Builder.load_file('manager.kv')
        # sm = ScreenManager()
        # sm.add_widget(Loading(name='loading'))
        # sm.add_widget(SignIn(name='sign_in'))
        # sm.add_widget(SignUp(name='sign_up'))
        # sm.add_widget(EmailConfirmation(name='email_confirmation'))
        # sm.add_widget(MenuWindow(name='menu_window'))
        # sm.add_widget(ClothesWindow(name='clothes_window'))
        # sm.add_widget(Map(name='map'))
        # sm.add_widget(Place(name='place'))

        return sm_file


if __name__ == '__main__':
    MainApp().run()
