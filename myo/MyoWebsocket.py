from websocket import create_connection
import threading


class MyoWebsocket(threading.Thread):
    def __init__(self, messageListener, appId):
        threading.Thread.__init__(self)
        self.messageListener = messageListener
        self.ws = create_connection("ws://127.0.0.1:10138/myo/3?appid=" + appId)
        self.running = True

    def close(self):
        self.running = False

    def send(self, message):
        self.ws.send(message)

    def run(self):
        while self.running:
            self.messageListener.onMessage(self.ws.recv())
        self.ws.close()
