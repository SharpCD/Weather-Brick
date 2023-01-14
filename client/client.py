import socket, json, struct
from threading import Thread
class Client(Thread):

    def __init__(self, **user_inf):
        SERVER = '178.172.212.130'
        PORT = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        Thread.__init__(self)
        self.user_inf = user_inf
    def run(self):
        t1 = Thread(target=self.task2)
        t2 = Thread(target=self.task)


        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def task(self):
        in_data = b''
        while True:
            data = self.client.recv(4096)
            if data[-5:] == b'<END>':
                in_data += data[:-5]
                try:
                    return in_data.decode()
                except:
                    return in_data
            else:
                in_data += data

    def task2(self):
        if self.user_inf['operation'] != 'adding_image':
            self.user_inf = json.dumps(self.user_inf)
            self.client.sendall(bytes(self.user_inf, 'UTF-8'))
            print('Отправлено на сервер:', self.user_inf)
        else:
            file = self.user_inf.pop('file')
            self.client.sendall(bytes(json.dumps(self.user_inf), 'UTF-8'))
            self.client.sendall(file+b'<END>')

            print('Отправлено на сервер:', self.user_inf)