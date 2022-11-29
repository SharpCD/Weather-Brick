import socket, threading, json
from send_email import SendEmail
from users_inf_db import DataBase
from weather import Weather


class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print ("Новое подключение: ", self.clientAddress)

    def run(self):
        print("Подключение с клиента : ", self.clientAddress)
        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = json.loads(data.decode('UTF-8'))
            print(f'Операция: {msg["operation"]}\nДанные: {msg}')
            if msg['operation'] == 'email_in_db':
                email_in_db = DataBase(msg['email'])
                email_in_db =str(email_in_db.check_email())
                self.csocket.send(bytes(email_in_db, 'UTF-8'))
                print('Отключение')
                break
            elif msg['operation'] == 'get_salt':
                salt = msg
                salt = DataBase(salt['email']).get_salt()
                self.csocket.send(bytes(salt, 'UTF-8'))
                break
            elif msg['operation'] == 'log_in':
                log_in = msg
                log_in = DataBase(log_in).log_in()
                self.csocket.send(bytes(json.dumps(log_in), 'UTF-8'))
                break
            elif msg['operation'] == 'weather':
                weather_inf = msg['city']
                weather_inf = Weather(weather_inf).weather()
                self.csocket.send(bytes(json.dumps(weather_inf), 'UTF-8'))
                break
            elif msg['operation'] == 'send_code':
                message = SendEmail(msg['email']).send_email()
                self.csocket.send(bytes(message,'UTF-8'))
                print('Сообщение для подтверждения аккаунта отправлено')
            elif msg['operation'] == 'user_inf':
                user_inf = msg
                del user_inf['operation']
                user_inf = DataBase(user_inf).adding_user_inf()
                print('Запись была добавлена')
                break

class Server():
    LOCALHOST = '192.168.1.7'
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
