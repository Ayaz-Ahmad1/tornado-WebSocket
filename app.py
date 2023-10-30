import tornado.ioloop
import tornado.web
import tornado.websocket


class ChatHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    usernames = {}

    def open(self):
        print("WebSocket opened")
        self.write_message(f"Welcome, please enter your username : ")

    def on_message(self, message):
        if self not in ChatHandler.usernames:
            # First message should be the username
            ChatHandler.usernames[self] = message
            self.write_message(f"Welcome, {message}!")

            for client, username in ChatHandler.usernames.items():
                if client is not self:
                    client.write_message(f"{message} joined the chat")

        else:
            username = ChatHandler.usernames.get(self, "Unknown User")
            print(f"Received message from {username}: {message}")
            # self.write_message(f"{username} : {message}!")

            for client in ChatHandler.usernames:
                client.write_message(f"{username}: {message}")

    def on_close(self):
        username = ChatHandler.usernames.get(self, "Unknown User")

        for client, client_username in ChatHandler.usernames.items():
            if client is not self:
                client.write_message(f"{username}: has left the chat.")

        try:
            if self in ChatHandler.clients:
                ChatHandler.clients.remove(self)
            if self in ChatHandler.usernames:
                del ChatHandler.usernames[self]
        except Exception as e:
            print(e)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


def make_app():
    return tornado.web.Application([
        (r"/ws", ChatHandler),
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
