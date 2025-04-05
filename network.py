import socket
import pickle

SERVER = "10.0.0.3"
PORT = 4000


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.address = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        """
        connects to the server
        """
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(e)

    def send(self, data):
        """
        send info to the server and get in return
        :param data: the info to send
        :return: the info that the server sent back
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

