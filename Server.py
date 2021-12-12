from Socket import Socket
import threading
from commandHandler import commandHandler


class Server(Socket):
    def __init__(self):
        super(Server, self).__init__()

        self.users = []

    def set_up(self):
        self.bind(("127.0.0.1", 1234))

        self.listen(5)
        print("Server is listening")

        self.accept_sockets()

    def listen_socket(self, listened_socket=None):
        handler = commandHandler()
        listened_socket.send("Your connected.".encode("utf-8"))

        while True:

            data = listened_socket.recv(2048)
            response = handler.handle(data.decode("utf-8"))
            listened_socket.send(response.encode("utf-8"))

    def accept_sockets(self):
        while True:
            user_socket, address = self.accept()      # Blocked function
            print(f"User {address} connected")

            self.users.append(user_socket)
            listen_accepted_user = threading.Thread(
                target=self.listen_socket,
                args=(user_socket,)
            )

            listen_accepted_user.start()


if __name__ == '__main__':
    server = Server()
    server.set_up()
