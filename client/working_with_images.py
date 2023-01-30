import os, json
from client import Client


class WorkingWithImages():
    def __init__(self):

        self.style = ['casual', 'classic', 'sport']
        self.feels_like = ['chilly', 'cold', 'heat', 'medium', 'very cold', 'very cold+', 'very heat', 'warm']


    def remove_iamges(self):
        for style in self.style:
            for feels_like in self.feels_like:
                list_img = os.listdir(f"Data/Image/my library/{style}/{feels_like}")
                for file in list_img:
                    os.remove((f"Data/Image/my library/{style}/{feels_like}/{file}"))

    def add_images(self, email):
        images = Client(operation = 'send_images', email = email)
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
                with open(f'Data/Image/my library/{img_inf["style"]}/{img_inf["feels_like"]}/{img_inf["filename"]}', 'wb') as file:
                    file.write(img_file)
                done +=1

        except:
            pass

# a = WorkingWithImages().add_images('kuchuk758@mail.ru')
# b = WorkingWithImages().remove_iamges()
# #
