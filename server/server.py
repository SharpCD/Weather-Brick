import socket, threading, json, struct
import time

from send_email import SendEmail
from users_inf_db import DataBase
from weather import Weather
from GeoLoc import GeoLoc
from geo_cod import GeoCod
from image_db import DataBaseImg
from tempfile import TemporaryFile


class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print ("Новое подключение: ", self.clientAddress)


    def run(self):
        def send_msg(msg):
            # Каждое сообщение будет иметь префикс в 4 байта блинной(network byte order)
            msg = struct.pack('>I', len(msg)) + msg
            self.csocket.sendall(msg)
        print("Подключение с клиента : ", self.clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode('UTF-8')
            try:
                msg= json.loads(msg)
                print(f'Операция: {msg["operation"]}\nДанные: {msg}')
            except:
                pass
            if msg['operation'] == 'email_in_db':
                email_in_db = DataBase(msg['email'])
                email_in_db =str(email_in_db.check_email())
                self.csocket.send(bytes(email_in_db, 'UTF-8')+b'<END>')
                print('Отключение')
                break
            elif msg['operation'] == 'get_salt':
                salt = msg
                salt = DataBase(salt['email']).get_salt()
                self.csocket.send(bytes(salt, 'UTF-8')+b'<END>')
                break
            elif msg['operation'] == 'log_in':
                log_in = msg
                log_in = DataBase(log_in).log_in()
                self.csocket.send(bytes(json.dumps(log_in), 'UTF-8')+b'<END>')
                break
            elif msg['operation'] == 'weather':
                weather_inf = msg['city']
                weather_inf = bytes(json.dumps(Weather(weather_inf).weather()), "UTF-8")
                self.csocket.send(weather_inf+b'<END>')
                break
            elif msg['operation'] == 'send_code':
                message = SendEmail(msg['email']).send_email()
                self.csocket.send(bytes(json.dumps(message),'UTF-8')+b'<END>')
                print('Сообщение для подтверждения аккаунта отправлено')
                break
            elif msg['operation'] == 'user_inf':
                user_inf = msg
                del user_inf['operation']
                user_inf = DataBase(user_inf).adding_user_inf()
                print('Запись была добавлена')
                break
            elif msg['operation'] == 'geo_loc':
                geo_loc = msg
                del geo_loc['operation']
                geo_loc = GeoLoc(geo_loc['geo'], geo_loc['name']).location()
                self.csocket.send(bytes(json.dumps(geo_loc), 'UTF-8')+b'<END>')
                break
            elif msg['operation'] == 'geo_cod':
                geo_cod = msg
                del geo_cod['operation']
                geo_cod = GeoCod(geo_cod['start_lon'], geo_cod['start_lat'], geo_cod['end_lon'], geo_cod['end_lat']).geo_cod()
                self.csocket.send(bytes(json.dumps(geo_cod), 'UTF-8')+b'<END>')
                break
            elif msg['operation']=='adding_image':
                file_bytes = b''
                done = False
                file = TemporaryFile()
                while not done:
                    data = self.csocket.recv(4096)
                    if data[-5:]==b'<END>':
                        file_bytes += data
                        done = True
                    else:
                        file_bytes+=data
                file.write(file_bytes)
                file.seek(0)
                DataBaseImg(msg, file.read()).adding_image()
                print('Изображение добавлено')
                break
            elif msg['operation'] == 'send_images':
                inf = msg
                files, count = DataBaseImg(None, None).count(inf['email'])
                self.csocket.send(bytes(str(count), 'UTF-8')+b'<END>')
                self.csocket.send(bytes('fgfgfg', 'UTF-8') + b'<END>')
                for file in files:
                    time.sleep(0.01)
                    img_inf, img_file = DataBaseImg(None, None).send_images(file)
                    self.csocket.send(bytes(json.dumps(img_inf), 'UTF-8')+b'<END>')
                    time.sleep(0.01)
                    self.csocket.sendall(img_file)
                break

class Server():
    LOCALHOST = '93.85.88.9'
    PORT = 8080
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Сервер работает")
    while True:
        server.listen(5)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == '__main__':
    Server()
