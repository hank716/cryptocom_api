import websocket
import json
import threading
import time

class WebSocketClient:
    def __init__(self, ws_url):
        self.ws_url = ws_url
        self.messages = []
        self.connected = False

    def on_message(self, ws, message):
        self.messages.append(json.loads(message))

    def on_open(self, ws):
        self.connected = True

    def on_error(self, ws, error):
        print("WebSocket error:", error)

    def on_close(self, ws, close_status_code, close_msg):
        self.connected = False

    def subscribe(self, topic):
        ws_app = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        def run():
            ws_app.run_forever()

        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

        time.sleep(2)
        sub_msg = {
            "method": "subscribe",
            "params": {"channels": [topic]},
            "id": 1
        }
        if self.connected:
            ws_app.send(json.dumps(sub_msg))

        return self
