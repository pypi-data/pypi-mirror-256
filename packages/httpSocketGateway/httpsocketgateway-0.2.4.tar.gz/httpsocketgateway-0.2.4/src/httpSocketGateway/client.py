import json
import _thread as thread
import time
from websocket._app import WebSocketApp

class WebSocketClient:
    def __init__(self, url, reconnect=True, simple=False):
        self.url = url
        self.reconnect = reconnect
        self.simple = simple
    
    def run(self):
        self.ws = WebSocketApp(self.url,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.thread = thread.start_new_thread(self.ws.run_forever, ())
        time.sleep(0.1)

    def on_message(self, ws, message):
        message = json.loads(message)
        response = self.process_message(message)
        if self.simple:
            self.send_json(json.dumps(response))
            return
        status_code = 500
        if response is None or "error" in response:
            response = {
                "error": "An error occurred"
                }
        else:
            status_code = 200
            
        response = {
            "id": message["id"],
            "type": "external-to-internal",
            "response": {
                "status": status_code,
                "headers": {
                    "Content-Type": "application/json"
                    },
                    "body": {**response}
                }
        }
        self.send_json(json.dumps(response))
    
    def process_message(self, message):
        print(f"Message received: {message}")
        raise NotImplementedError("You must implement this method process_message")
        return {"success": "Hello World"}

    def on_error(self, ws, error):
        print(f"Error occurred: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")
        if self.reconnect:
            self.run()

    def on_open(self, ws):
        print("Connection established")

    def send_json(self, data):
        json_data = json.dumps(data)
        self.ws.send(json_data)

    def close(self):
        self.reconnect = False
        self.ws.close()
    
    def is_connected(self):
        if self.ws.sock is None:
            return False
        return self.ws.sock.connected
    
    def is_closed(self):
        if self.ws.sock is None:
            return True
        return not self.ws.sock.connected

# Exemple of use
if __name__ == "__main__":
    client = WebSocketClient("ws://127.0.0.1:4200/ws")
    client.run()
    try:
        time.sleep(60)
    except KeyboardInterrupt:
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")
