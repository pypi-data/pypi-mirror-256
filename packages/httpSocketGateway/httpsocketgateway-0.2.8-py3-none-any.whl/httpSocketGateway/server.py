from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, Response, UploadFile, File
from typing import Optional
import uvicorn
import queue
import uuid
import asyncio
import time
import json
import os
from fastapi.responses import FileResponse, JSONResponse
import re

class Gateway:
    def __init__(self):
        self.app = FastAPI()
        self.app.add_api_route("/", self.http_hello_world)
        self.app.add_api_route("/api", self.http_endpoint, methods=["POST"])
        self.app.add_api_route("/download/{file_id}", self.download_file, methods=["GET"])
        self.app.add_websocket_route("/ws", self.websocket_endpoint)
        self.active_websocket: Optional[WebSocket] = None
        self.messages_queue = queue.Queue()
        # test if the directory exists
        if not os.path.exists("data/records"):
            os.makedirs("data/records")
    
    def __del__(self):
        pass
    
    async def http_hello_world(self):
        return JSONResponse(content={"success": "Hello, World!"}, status_code=200, media_type="application/json")

    async def http_endpoint(self, request: Request, file: Optional[UploadFile] = File(None)):

        # generate unique id
        request_id = uuid.uuid4().hex
        print(request_id)

        # save file
        # if file exists
        if file is not None:
            with open(f"data/records/{request_id}.wav", "wb") as buffer:
                buffer.write(file.file.read())
            print("file saved")
        body = await request.json()
        send = {
            "id": request_id,
            "type": "internal-to-external",
            "request": {
                    "method": request.method,
                    "url": request.url.path,
                    "headers": dict(request.headers),
                    "body": body
                },
                "file": file is not None,
            }
        if self.active_websocket:
            await self.active_websocket.send_json(send)
        else:
            # TODO: Handle this case
            raise Exception("No active WebSocket connection")
        response = await self.wait_response(request_id=request_id, timeout=15)
        return JSONResponse(content=response, status_code=200, media_type="application/json")
    
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
                if data["type"] == "external-to-internal":
                    self.messages_queue.put(data)
        except WebSocketDisconnect:
            print("Client disconnected from WebSocket")
        finally:
            self.active_websocket = None
    
    async def download_file(self, file_id: str):
        # check if the file_id is valid
        if re.match(r"^\w+$", file_id) is None:
            return JSONResponse(content={"error": "Invalid file ID"}, status_code=400, media_type="application/json")
        return FileResponse(f"data/records/{file_id}.wav")

    def run(self, host, port):
        uvicorn.run(self.app, host=host, port=port)

if __name__ == "__main__":
    gateway = Gateway()
    # os.environ["LAURE_SELF_HOST"] = "127.0.0.1"
    # os.environ["LAURE_SELF_PORT"] = "4200"
    gateway.run(host=os.environ["LAURE_SELF_HOST"], port=os.environ["LAURE_SELF_PORT"])

