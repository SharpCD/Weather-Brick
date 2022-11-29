import socket
from threading import Thread
import json
class Client(Thread):

    def __init__(self, **user_inf):
        SERVER = '192.168.1.7'
        PORT = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        Thread.__init__(self)
        self.user_inf = json.dumps(user_inf)
    def run(self):
        t1 = Thread(target=self.task2)
        t2 = Thread(target=self.task)

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    def task(self):
        in_data =  self.client.recv(4096)
        print("От сервера:" ,in_data.decode())
        return in_data.decode()

    def task2(self):
        self.client.sendall(bytes(self.user_inf,'UTF-8'))
        print('Отправлено на сервер:',self.user_inf)


