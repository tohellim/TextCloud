from Socket import Socket
from threading import Thread


class Client(Socket):
    def __init__(self):
        super(Client, self).__init__()

    def set_up(self):
        self.connect(
            ("127.0.0.1", 1234)
        )

        listen_thread = Thread(target=self.listen_socket)
        listen_thread.start()

    def listen_socket(self, listened_socket=None):
        while True:
            data = self.recv(2048)     # Receive (Получить)
            print(data.decode("utf-8"))
            self.send(input(":::").encode("utf-8"))


if __name__ == "__main__":
    client = Client()
    client.set_up()
