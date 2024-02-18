from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Response
from typing import Optional
import uvicorn
import queue
import uuid
import asyncio
import time
import json
import os

class Gateway:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_api_route("/", self.http_hello_world)
        self.app.add_api_route("/api", self.http_endpoint, methods=["POST"])
        self.app.add_websocket_route("/ws", self.websocket_endpoint)
        self.active_websocket: Optional[WebSocket] = None
        self.messages_queue = queue.Queue()
    
    async def http_hello_world(self):
        return Response(json.dumps({"success": "Hello, World!"}), status_code=200, media_type="application/json")

    async def http_endpoint(self, request: Request):
        request_id = uuid.uuid4().hex
        body = await request.json()
        send = {
            "id": request_id,
            "type": "internal-to-external",
            "request": {
                    "method": request.method,
                    "url": request.url.path,
                    "headers": dict(request.headers),
                    "body": body
                }
            }
        if self.active_websocket:
            await self.active_websocket.send_json(send)
        else:
            # TODO: Handle this case
            raise Exception("No active WebSocket connection")
        response = await self.wait_response(request_id=request_id, timeout=15)

        return Response(json.dumps(response), status_code=200, media_type="application/json")
    
    async def wait_response(self, request_id, timeout=None):
        start = time.time()
        if timeout is None:
            timeout = 60*5
        while time.time() - start < timeout:
            if not self.messages_queue.empty():
                message = self.messages_queue.get()
                if message["id"] != request_id:
                    self.messages_queue.put_nowait(message)
                else:
                    return message
            await asyncio.sleep(0.1)
        return {
            "status": "408",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "error": "Request timeout"
            }
        }

    async def websocket_endpoint(self, websocket: WebSocket):
        self.active_websocket = websocket # .
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_json()
                data = json.loads(data)
                self.messages_queue.put(data)
        except WebSocketDisconnect:
            print("Client disconnected from WebSocket")
        finally:
            self.active_websocket = None

    def run(self, host, port):
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    gateway = Gateway()
    # os.environ["LAURE_SELF_HOST"] = "127.0.0.1"
    # os.environ["LAURE_SELF_PORT"] = "4200"
    gateway.run(host=os.environ["LAURE_SELF_HOST"], port=os.environ["LAURE_SELF_PORT"])
