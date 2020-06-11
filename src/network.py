import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = "192.168.100.62"
        self.PORT = 5569
        self.addr = (self.HOST, self.PORT)

        self.p = self.connect()

    def get_idx(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Could not connect to server", f"Error: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def disconnect(self):
        self.client.close()
