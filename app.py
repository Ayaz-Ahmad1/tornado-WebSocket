import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ProgressWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        for i in range(1, 101):
            time.sleep(0.1)  # Simulate a 10-second task
            self.write_message(str(i))
        self.close()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/progress_ws", ProgressWebSocket),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
