import socket, json, struct
import time
from threading import Thread
class Client():

    def __init__(self, **user_inf):
        SERVER = '178.172.212.130' #178.172.212.130
        PORT = 8080
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.user_inf = user_inf

    # def start(self):
    #     print('gfg')
    #
    def task(self):
        # in_data = b''
        # image = []
        # data = b''
        # while data!=b'<DONE>':
        #     data = self.client.recv(4096)
        #     # print(data)
        #     if data[-5:] == b'<END>':
        #         in_data += data[:-5]
        #         # print(in_data)
        #         try:
        #             image+=[in_data.decode()]
        #         except:
        #             image += [in_data]
        #         in_data = b''
        #     else:
        #         in_data += data
        # for i in range(len(image)):
        #     print(image[i])
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
        elif self.user_inf['operation'] == 'adding_image':
            file = self.user_inf.pop('file')
            self.client.send(bytes(json.dumps(self.user_inf), 'UTF-8'))
            time.sleep(0.01)
            self.client.sendall(file+b'<END>')

            print('Отправлено на сервер:', self.user_inf)
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