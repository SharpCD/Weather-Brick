import time

from kivy.graphics import Rectangle, Color, Line, Bezier, Ellipse, Triangle
from kivy.uix.screenmanager import NoTransition
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.button import MDFillRoundFlatButton, MDIconButton
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
import requests, re, json, os
from plyer import gps
from hashlib import pbkdf2_hmac
from kivymd.uix.fitimage import FitImage
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.menu import MDDropdownMenu
from client import Client
from working_with_images import WorkingWithImages
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.expansionpanel import MDExpansionPanelOneLine, MDExpansionPanel
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import IconLeftWidget, OneLineIconListItem
from kivy.animation import Animation
from kivymd.uix.dialog import MDDialog
from kivymd.uix.hero import MDHeroFrom
from kivy.utils import platform
from time import strftime
from os import getcwd, mkdir
from os.path import exists
from threading import Thread
from kivy.metrics import dp

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
password_re = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z]).*$"
gender_fldr = ['man', 'woman']
style_fldr = ['casual', 'classic', 'sport']
feels_like_fldr = ['chilly', 'cold', 'heat', 'medium', 'very cold', 'very cold+', 'very heat', 'warm']


class Loading(MDScreen):
    def on_enter(self, *args):
        Clock.schedule_once(self.login, 4)

    def login(self, *args):
        self.manager.transition = NoTransition()
        if exists(f'{getcwd()}/Data/Image/my library'):
            pass
        else:
            mkdir(f'{getcwd()}/Data/Image/my library')
            for dir1 in style_fldr:
                mkdir(f'{getcwd()}/Data/Image/my library/{dir1}')
                for dir2 in feels_like_fldr:
                    mkdir(f'{getcwd()}/Data/Image/my library/{dir1}/{dir2}')
        self.manager.get_screen('menu_window').weather_at_city(geo)
        self.manager.get_screen('sign_in').enter()
        try:
            with open('registration.bin', 'rb') as file:
                inf = file.read().decode()
            if inf == 'yes' or inf == 'skip':
                self.manager.current = 'menu_window'
        except:
            self.manager.current = 'sign_in'


class SignIn(MDScreen):

    def enter(self):
        # back = 'Data/Image/loading '+ self.manager.get_screen('menu_window').ids.img.source[11:]
        color = ''
        # self.back.source = back
        # self.card.md_bg_color = color_card
        self.manager.get_screen('sign_up').enter()

    def next(self):
        self.salt = Client(operation='get_salt', email=self.email.text).task2()
        if self.salt == 'None':
            Snackbar(
                text="  Введите корректный Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        else:
            self.manager.get_screen('sign_in').slide.load_next(mode='next')

    def log_in_information(self):
        password = self.manager.get_screen('sign_in').ids.password.text.encode()
        password = pbkdf2_hmac('sha256', password, self.salt.encode('utf-8'), 10000)
        log_in = Client(operation='log_in',
                        email=self.email.text,
                        password=password.hex()
                        ).task2()
        log_in = json.loads(log_in)
        if log_in == None:
            Snackbar(
                text="  Неправильный пароль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        else:
            with open('user information.bin', 'wb') as file:
                for key, value in log_in.items():
                    file.write(f'{key}:{value}\n'.encode())
            with open('registration.bin', 'wb') as file:
                file.write('yes'.encode())
            self.manager.get_screen('sign_in').slide.load_previous()
            self.email.text = ''
            self.password.text = ''
            self.manager.current = 'menu_window'

    def previous(self):
        self.manager.get_screen('sign_in').slide.load_previous()

    def skip_btn(self):
        with open('registration.bin', 'wb') as file:
            file.write('skip'.encode())
        self.manager.current = 'menu_window'


class SignUp(MDScreen):

    def enter(self):
        pass

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
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        elif len(self.last_name.text) == 0:
            Snackbar(
                text="  Введите фамилию",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

    def next2(self):
        if len(self.email.text) != 0 and len(self.number.text) != 0 and re.fullmatch(regex, self.email.text):
            requests_email = Client(operation='email_in_db', email=self.email.text).task2()
            if requests_email == 'None':
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
                    snackbar_x="10dp",
                    snackbar_y=f"{Window.height // 1.1}dp",
                    radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()
        elif len(self.email.text) == 0:
            Snackbar(
                text="  Введите Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        elif not re.fullmatch(regex, self.email.text):
            Snackbar(
                text="  Введите корректный Email",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

        elif len(self.number.text) == 0:
            Snackbar(
                text="  Введите номер телефона",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

    def next3(self):
        if not re.fullmatch(password_re, self.password.text):
            Snackbar(
                text="  Cлабый пароль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
        elif len(self.password.text) != 0 and len(
                self.repeat_password.text) != 0 and self.password.text == self.repeat_password.text:
            self.num3.icon = 'checkbox-marked-circle'
            self.num3.icon_color = '#309AEB'
            self.manager.get_screen('sign_up').slide.load_next(mode='next')
            self.manager.get_screen('email_confirmation').enter()
            self.manager.current = 'email_confirmation'
        elif len(self.password.text) == 0:
            Snackbar(
                text="  Введите пароль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

            self.password.text = ''
            self.repeat_password.text = ''
        elif self.password.text != self.repeat_password.text:
            Snackbar(
                text="  Пароли не совпадают",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
            self.password.text = ''
            self.repeat_password.text = ''

    def previous1(self):
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


class EmailConfirmation(MDScreen):
    def enter(self):
        pass

    def on_enter(self, *args):
        code = Client(operation='send_code',
                      email=self.manager.get_screen('sign_up').ids.email.text).task2()
        self.code = json.loads(code)

    def checking_code(self):
        if self.conf_code.text == self.code['code']:
            salt = self.code['salt']
            password = self.manager.get_screen('sign_up').ids.password.text.encode()
            password = pbkdf2_hmac('sha256', password, salt.encode('utf-8'), 10000, )
            user_inf = Client(operation='user_inf',
                              email=self.manager.get_screen('sign_up').ids.email.text,
                              first_name=self.manager.get_screen('sign_up').ids.frst_name.text,
                              last_name=self.manager.get_screen('sign_up').ids.last_name.text,
                              phone_number=self.manager.get_screen('sign_up').ids.number.text,
                              password=password.hex(),
                              salt=salt
                              ).task2()
            self.manager.current = 'sign_in'
        else:
            Snackbar(
                text="  Неправильный код",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()


class MenuWindow(MDScreen):

    def weather_at_city(self, city):
        city = Client(operation='weather', city=city).task2()
        # city.start()
        # city = json.loads(city.task())
        city = json.loads(city)
        self.main = city['main']
        if self.main == 'Rain':
            sound = SoundLoader.load('Data/Sound//rain.mp3')
            sound.play()
        self.city_ti = city['city_ti']
        self.time_city_now = city['time_city_now']
        self.geo = geo
        dir = city["dir"]
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
        self.feels_like_temp.text = city['feels_like_temp']
        self.time.text = self.time_city_now
        self.city.text = self.city_ti
        self.sost.text = self.sost_w
        self.temp.text = self.temp_w
        self.prssr.text = self.pressure
        self.prssr_img.source = f'Data/Image/{dir}/pressure.png'
        self.hmdt.text = self.humidity
        self.hmdt_img.source = f'Data/Image/{dir}/humidity.png'
        self.wnd.text = self.wind
        self.wnd_img.source = f'Data/Image/{dir}/wind.png'
        self.temperature_img.source = f'Data/Image/{dir}/temperature.png'
        global back, color_card
        back = f'Data/Image/{dir}/background.png'
        self.back.source = back
        color_card = city['color_card']
        self.gl.clear_widgets()
        for i in range(10):
            self.gl.add_widget(MDLabel(
                size_hint_x=None,
                halign='center',
                text=self.forecast_city[i][0],
                font_size=Window.height // 55
            ))
        for i in range(10):
            self.gl.add_widget(Image(
                source=self.forecast_city[i][2]
            ))
        for i in range(10):
            self.gl.add_widget(MDLabel(
                size_hint_x=None,
                halign='center',
                text=self.forecast_city[i][1],
                font_size=Window.height // 55
            ))
        self.manager.get_screen('my_clothes_window').enter()
        self.manager.get_screen('clothes_window').enter()
        self.manager.get_screen('place').enter()

    def on_enter(self, *args):
        with open('registration.bin', 'rb') as file:
            inf = file.read().decode()
        user_inf = {}
        if inf == 'yes':
            with open("user information.bin", 'rb') as file:
                for line in file:
                    key, *value = line.decode().split(':')
                    user_inf[key] = value[0][:-1]
            self.user.text = f'{user_inf["first_name"]} {user_inf["last_name"]}'
            self.login_logout.text = 'Выйти'
            self.login_logout.icon = 'logout'
            self.email.text = user_inf['email']
            self.email.icon = 'email'
            self.image_synchronization.text = 'Синхронизация'
            self.image_synchronization.icon = 'folder-image'
        else:
            self.user.text = 'вы еще не вошли в аккаунт'
            self.login_logout.text = 'Войти'
            self.login_logout.icon = 'login'
            self.email.text = ''
            self.email.icon = ''
            self.image_synchronization.text = ''
            self.image_synchronization.icon = ''

    def login_logout_press(self):
        with open('registration.bin', 'rb') as file:
            inf = file.read().decode()
        self.nav_drawer.status = 'closed'
        if inf == 'yes':
            with open('registration.bin', 'wb') as file:
                file.write('skip'.encode())
            WorkingWithImages().remove_iamges()
            self.manager.current = 'sign_in'
            file1 = open('user information.bin', 'wb')
            file1.close()
        else:
            self.manager.current = 'sign_in'

    def image_synchronization_press(self):
        if self.image_synchronization.text != '':
            self.manager.current = 'uploading_images'
            t1 = Thread(target=self.manager.get_screen('uploading_images').uploading)
            t1.start()

    def get_city(self):
        city = self.city.text
        self.manager.get_screen('place').ids.box.clear_widgets()
        self.manager.get_screen('place').ids.fl.clear_widgets()
        self.manager.get_screen('place').ids.search.background_normal = "Data/Image//search.png"
        self.manager.get_screen('place').ids.search.background_down = "Data/Image//search.png"
        self.manager.get_screen('place').ids.text1.text = 'Выберете категорию'
        self.manager.get_screen('place').ids.slide.size_hint = (.9, .5)
        self.manager.get_screen('place').ids.slide.pos_hint = {'center_x': .5, 'center_y': .35}
        self.manager.get_screen('my_clothes_window').ids.box.clear_widgets()
        self.manager.get_screen('clothes_window').ids.box.clear_widgets()
        try:
            self.weather_at_city(city)
        except:
            Snackbar(
                text="  Информация отсутствует",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()
            self.city.text = self.city_ti

        # print( sm.get_screen('menu_window').ids.btn.text)

        # self.weather_at_city(city)


class MyClothesWindow(MDScreen):

    def enter(self):
        self.back.source = back
        self.add_images()

    def drp_down(self):
        menu_items = [
            {
                "text": "classic",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="classic": self.menu_callback(x),
            },
            {
                "text": "casual",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="casual": self.menu_callback(x),
            },
            {
                "text": "sport",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="sport": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_down,
            items=menu_items,
            width_mult=3,
            max_height=self.height // 6

        )
        self.menu.open()

    def menu_callback(self, style):
        self.drop_down.text = style
        self.menu.dismiss()
        self.box.clear_widgets()
        self.add_images()

    def add_images(self):
        style = self.drop_down.text
        feels_like = self.manager.get_screen('menu_window').feels_like
        self.blank.text = ''
        if style == 'Стиль':
            images_path = []
            for style in style_fldr:
                images = os.listdir(f"Data/Image/my library/{style}/{feels_like}")
                for image in images:
                    images_path += [f"Data/Image/my library/{style}/{feels_like}/{image}"]

            if len(images_path) != 0:
                for i in range(len(images_path)):
                    hero_item = HeroItem(
                        text=f"Item {i + 1}", tag=f"tag_{i}", manager=self.manager,
                        source=images_path[i],
                        screen='clothes_image')
                    # if not i % 2:
                    #     hero_item.md_bg_color = "lightgrey"
                    self.box.add_widget(hero_item)
            else:
                self.blank.text = 'В вашей библиотеке отсутствуют изображения одежды, подхожящие для данных погодных условий.'
        else:
            images_path = f"Data/Image/my library/{style}/{feels_like}"
            images_list = os.listdir(images_path)
            if len(images_list) != 0:
                for i in range(len(images_list)):
                    hero_item = HeroItem(
                        text=f"Item {i + 1}", tag=f"tag_{i}", manager=self.manager,
                        source=f"{images_path}/{images_list[i]}",
                        screen='clothes_image')
                    # if not i % 2:
                    #     hero_item.md_bg_color = "lightgrey"
                    self.box.add_widget(hero_item)
            else:
                self.blank.text = 'В вашей библиотеке отсутствуют изображения одежды, подхожящие для данных погодных условий.'


class ClothesImage(MDScreen):
    def enter(self, source):
        self.back.source = source


class ClothesWindow(MDScreen):
    def enter(self):
        self.back.source = back
        self.add_images()

    def drp_down(self):
        menu_items = [
            {
                "text": "classic",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="classic": self.menu_callback(x),
            },
            {
                "text": "casual",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="casual": self.menu_callback(x),
            },
            {
                "text": "sport",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="sport": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_down,
            items=menu_items,
            width_mult=3,
            max_height=self.height // 6

        )
        self.menu.open()

    def menu_callback(self, style):
        self.drop_down.text = style
        self.menu.dismiss()
        self.box.clear_widgets()
        self.add_images()

    def add_images(self):
        style = self.drop_down.text
        if self.gender.icon == 'gender-male':
            gender = 'man'
        else:
            gender = 'woman'
        feels_like = self.manager.get_screen('menu_window').feels_like
        self.blank.text = ''
        if style == 'Стиль':
            images_path = []
            for style in style_fldr:
                images = os.listdir(f"Data/Image/{gender}/{style}/{feels_like}")
                for image in images:
                    images_path += [f"Data/Image/{gender}/{style}/{feels_like}/{image}"]

            if len(images_path) != 0:
                for i in range(len(images_path)):
                    hero_item = HeroItem(
                        text=f"Item {i + 1}", tag=f"tag_{i}", manager=self.manager,
                        source=images_path[i],
                        screen='clothes_image2')
                    if not i % 2:
                        hero_item.md_bg_color = "lightgrey"
                    self.box.add_widget(hero_item)
            else:
                self.blank.text = 'В вашей библиотеке отсутствуют изображения одежды, подхожящие для данных погодных условий.'
        else:
            images_path = f"Data/Image/{gender}/{style}/{feels_like}"
            images_list = os.listdir(images_path)
            if len(images_list) != 0:
                for i in range(len(images_list)):
                    hero_item = HeroItem(
                        text=f"Item {i + 1}", tag=f"tag_{i}", manager=self.manager,
                        source=f"{images_path}/{images_list[i]}",
                        screen='clothes_image2')
                    if not i % 2:
                        hero_item.md_bg_color = "lightgrey"
                    self.box.add_widget(hero_item)
            else:
                self.blank.text = 'В вашей библиотеке отсутствуют изображения одежды, подхожящие для данных погодных условий.'


class ClothesImage2(MDScreen):
    def enter(self, source):
        self.back.source = source


class CameraScreen(MDScreen):
    def enter(self):
        pass

    def on_enter(self, *args):
        self.camera.play = True

    # def enter(self):
    #     pass
    # def on_enter(self, *args):
    #     self.capture = cv2.VideoCapture(0)
    #     Clock.schedule_interval(self.load_video, 1 / 30)

    # def load_video(self, *args):
    #     ret, frame = self.capture.read()
    #     self.image_frame = frame
    #     buffer = cv2.flip(frame, 0).tobytes()
    #     texture = Texture.create(size = (frame.shape[1], frame.shape[0]), colorfmt ='bgr')
    #     texture.blit_buffer(buffer, colorfmt = 'bgr', bufferfmt = 'ubyte')
    #     self.image.texture = texture
    def drp_down(self):
        menu_items = [
            {
                "text": "classic",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="classic": self.menu_callback(x),
            },
            {
                "text": "casual",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="casual": self.menu_callback(x),
            },
            {
                "text": "sport",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="sport": self.menu_callback(x),
            }
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_down,
            items=menu_items,
            width_mult=3,
            max_height=self.height // 6

        )
        self.menu.open()

    def menu_callback(self, style):
        self.drop_down.text = style
        self.menu.dismiss()

    def take_photo_function(self, *args):
        if self.drop_down.text == 'Выберите стиль':
            Snackbar(
                text="  Выберите стиль",
                snackbar_animation_dir='Top',
                bg_color='#CF5A5D',
                shadow_color='#CF5A5D',
                font_size=Window.height // 44,
                snackbar_x="10dp",
                snackbar_y=f"{Window.height // 1.1}dp",
                radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

        else:
            feels_like = self.manager.get_screen('menu_window').feels_like
            name = f'PNG_{strftime("%Y%m%d_%H%M%S")}.png'
            # path = f'Data/Image/my library/{self.drop_down.text}/{feels_like}/{name}'
            path = f'{getcwd()}/Data/Image/my library/{self.drop_down.text}/{feels_like}/{name}'
            # cv2.imwrite(f'Data/Image/my library/{self.drop_down.text}/{feels_like}/{name}', self.image_frame)
            self.camera.export_to_png(path)
            with open(path, 'rb') as img:
                img = img.read()
            send = Client(operation='adding_image', filename=name, feels_like=feels_like, style=self.drop_down.text,
                          file=img, email=self.manager.get_screen('menu_window').ids.email.text).task2()
        # send = send.task()


class Place(MDScreen):
    def enter(self):
        self.back.source = back
        self.brock.add_widget(FitImage(
            source='Data/Image/Brock.png'
        ))

    def on_enter(self, *args):
        pass
        # self.map.lat = int(sm.get_screen('menu_window').lat)
        # self.map.lon = int(sm.get_screen('menu_window').lon)

    def a(self, *args):
        pass

    def category(self):
        category_menu = {
            'Кинотеатры': ["Data/Image//cinema.png", 'filmstrip-box'],
            "Парки": ["Data/Image//park.png", 'tree'],
            "Кафе": ["Data/Image//cafe.png", 'coffee'],
            "Бары": ["Data/Image//bar.png", 'beer'],
            "Рестораны": ["Data/Image//restaurant.png", 'silverware-variant'],
            "Отели": ["Data/Image//hotel.png", 'bed'],

        }
        category = MDListBottomSheet(
            bg_color=color_card,
            radius_from='top',
            size_hint=(1, 1)

        )
        for item in category_menu.items():
            category.add_item(
                text=item[0],
                callback=lambda x, y=item[0], z=item[1]: self.category_menu_press(y, z),
                icon=item[1][1],

            )
        category.open()

    def category_menu_press(self, name, path):
        self.fl.clear_widgets()
        self.map = MapView(
            size_hint=(1, 1),
            pos_hint={'center_x': .5, 'center_y': .5},
            lat=self.manager.get_screen('menu_window').ids.lat.text,
            lon=self.manager.get_screen('menu_window').ids.lon.text,
            zoom=15,
        )
        self.brock.clear_widgets()
        self.box.clear_widgets()
        self.text1.text = name
        self.search.background_normal = path[0]
        self.search.background_down = path[0]
        self.geo = [self.manager.get_screen('menu_window').ids.lat.text,
                    self.manager.get_screen('menu_window').ids.lon.text]
        places = Client(operation='geo_loc', geo=self.geo, name=name).task2()
        places = json.loads(places)
        for i in range(len(places)):
            lat = places[i]['coordinates'][0]
            lon = places[i]['coordinates'][1]
            self.marker = (MapMarkerPopup(lat=lat, lon=lon, ))
            self.marker.add_widget(MDFillRoundFlatButton(text=places[i]['name'], text_color="white",
                                                         md_bg_color='#E74C3C', halign='center', ))
            panel = (MDExpansionPanel(
                content=Content(places[i]['address'], places[i]['hours']).enter(),
                panel_cls=MDExpansionPanelOneLine(text=places[i]['name']),
            ))
            item = OneLineIconListItem(text='Построить маршрут',
                                       on_release=lambda x, y=lat, z=lon: self.item_press(y, z))
            item.add_widget(IconLeftWidget(
                icon="map-marker-path"
            ))
            panel.content.add_widget(item)
            self.box.add_widget(panel)
            self.map.add_widget(MapMarkerPopup(lat=self.geo[0], lon=self.geo[1], source='Data/Image/dist.png'))
            self.map.add_widget(self.marker)

        self.fl.add_widget(self.map)
        self.size_btn = MDIconButton(icon='arrow-expand', pos_hint={'center_x': .9, 'center_y': .9},
                                     theme_icon_color="Custom", icon_color='gray',
                                     icon_size=self.height // 25, on_release=lambda x: self.map_size())
        self.fl.add_widget(self.size_btn)
        self.fl2 = MDFloatLayout()
        self.map.add_widget(self.fl2)

    def map_size(self):
        if self.size_btn.icon == 'arrow-expand':
            self.slide.size_hint = (1, 1)
            self.slide.pos_hint = {'center_x': .5, 'center_y': .5}
            self.size_btn.icon = 'arrow-collapse'
        else:
            self.slide.size_hint = (.9, .5)
            self.slide.pos_hint = {'center_x': .5, 'center_y': .35}
            self.size_btn.icon = 'arrow-expand'

    def route(self, start_lon, start_lat, end_lon, end_lat):
        self.fl2.canvas.clear()
        self.fl2.canvas.add(Color(.45, .70, .83))
        self.list_of_lines = []
        self.route_points = []
        self.res1 = Client(operation='geo_cod', start_lon=start_lon, start_lat=start_lat, end_lon=end_lon,
                           end_lat=end_lat).task2()
        self.res1 = json.loads(self.res1)['cod']
        for i in range(0, len(self.res1) - 1, 2):
            self.points_lat = self.res1[i]
            self.points_lon = self.res1[i + 1]

            self.points_pop = MapMarkerPopup(lat=self.points_lat, lon=self.points_lon,
                                             source='Data/Image/waypoints.png')
            self.route_points.append(self.points_pop)

            self.map.add_widget(self.points_pop)
        for j in range(0, len(self.route_points) - 1, 1):
            self.lines = Line(
                points=(self.route_points[j].pos[0], self.route_points[j].pos[1], self.route_points[j + 1].pos[0],
                        self.route_points[j + 1].pos[1]), width=self.height // 350)
            self.list_of_lines.append(self.lines)
            self.fl2.canvas.add(self.lines)
        Clock.schedule_interval(self.update_route_lines, 1 / 100)

    def update_route_lines(self, *args):

        for j in range(1, len(self.route_points), 1):
            self.list_of_lines[j - 1].points = [self.route_points[j - 1].pos[0], self.route_points[j - 1].pos[1],
                                                self.route_points[j].pos[0], self.route_points[j].pos[1]]

    def segmented_control(self, widget, pos, *args):
        animation = Animation(pos_hint={'center_x': pos}, duration=0.2)
        animation.start(widget)

    def item_press(self, lat, lon):
        self.route(self.geo[1], self.geo[0], lon, lat)
        self.segmented_control(self.switching, 0.675)
        self.slide.load_next(mode='next')


class HeroItem(MDHeroFrom):
    text = StringProperty()
    source = StringProperty()
    manager = ObjectProperty()
    screen = StringProperty()

    def on_release(self):
        self.manager.get_screen(self.screen).enter(self.source)
        self.manager.current = self.screen


class NavBar(MDFloatLayout):
    pass


class UploadingImages(MDScreen):
    def on_enter(self, *args):
        self.back.source = back
        self.progress.start()

    def uploading(self):
        answer = self.add_images(self.manager.get_screen('menu_window').ids.email.text)
        print(answer)
        if answer == 'done':
            self.set_screen()
        else:
            self.error()

    def add_images(self, email):
        images = Client(operation='send_images', email=email)
        count = int(images.task2())
        print(count)
        done = 0
        try:
            for i in range(count):
                img_inf = images.task()
                img_inf = json.loads(img_inf)
                print(img_inf)
                img_file = images.task()
                # print(img_file)
                with open(f'Data/Image/my library/{img_inf["style"]}/{img_inf["feels_like"]}/{img_inf["filename"]}',
                          'wb') as file:
                    file.write(img_file)
                done += 1
                self.inf.text = f'Загружено {done} из {count}'
            return 'done'
        except:
            return 'error'

    @mainthread
    def set_screen(self):
        Snackbar(
            text="  Успешная синхронизация",
            snackbar_animation_dir='Top',
            bg_color='#5EBA7D',
            shadow_color='#5EBA7D',
            font_size=Window.height // 44,
            snackbar_x="10dp",
            snackbar_y=f"{Window.height // 1.1}dp",
            radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
            size_hint_x=(
                                Window.width - (dp(10) * 2)
                        ) / Window.width
        ).open()
        time.sleep(3)
        self.manager.current = 'menu_window'

    @mainthread
    def error(self):
        self.progress.stop()
        Snackbar(
            text=" Ошибка при синхронизации",
            snackbar_animation_dir='Top',
            bg_color='#CF5A5D',
            shadow_color='#CF5A5D',
            font_size=Window.height // 44,
            snackbar_x="10dp",
            snackbar_y=f"{Window.height // 1.1}dp",
            radius=[self.height // 60, self.height // 60, self.height // 60, self.height // 65],
            size_hint_x=(
                                Window.width - (dp(10) * 2)
                        ) / Window.width
        ).open()
        self.manager.current = 'menu_window'


class Content(object):
    dialog1 = None
    dialog2 = None

    def __init__(self, address, schedule):
        self.address = address
        self.schedule = schedule

    def enter(self):
        bl = MDBoxLayout(orientation='vertical', adaptive_height=True)
        item = TwoLineIconListItem(text='Адрес', secondary_text=self.address,
                                   on_release=lambda x, y=self.address: self.on_release_1(y))
        item.add_widget(IconLeftWidget(
            icon="map-marker-radius"
        ))
        bl.add_widget(item)
        item = TwoLineIconListItem(text='Расписание', secondary_text=self.schedule,
                                   on_release=lambda x, y=self.schedule: self.on_release_2(y))
        item.add_widget(IconLeftWidget(
            icon="clock"
        ))
        bl.add_widget(item)
        return bl

    def on_release_1(self, text):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title='Адрес',
                text=text,

            )
        self.dialog1.open()

    def on_release_2(self, text):
        if not self.dialog2:
            self.dialog2 = MDDialog(
                title='Расписание',
                text=text,

            )
        self.dialog2.open()


Window.size = (416 / 0.9, 901 / 0.9)


class MainApp(MDApp):
    def on_start(self):
        global geo
        if platform == 'android':
            def print_locations(**geo):
                return [geo['lat'], geo['lon']]

            geo = gps.configure(on_location=print_locations)
            gps.start()
            gps.stop()
        else:
            geo = requests.get('https://ipinfo.io/json').json()
            geo = geo['loc'].split(',')

    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ])
            from android.storage import primary_external_storage_path
            global primary_ext_storage
            primary_ext_storage = primary_external_storage_path()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        sm_file = Builder.load_file('manager.kv')
        return sm_file

    def anim(self, pos, *args):
        animation = Animation(pos_hint={'center_y': pos}, duration=0.2)
        animation.start(self.root.bar)

    def change_color(self, instance):
        if instance in self.root.ids.values():
            current_id = list(self.root.ids.keys())[list(self.root.ids.values()).index(instance)]
            for i in range(5):
                if f'nav_icon{i + 1}' == current_id:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 'gray'
                else:
                    self.root.ids[f'nav_icon{i + 1}'].text_color = 1, 1, 1, 1


if __name__ == '__main__':
    MainApp().run()
