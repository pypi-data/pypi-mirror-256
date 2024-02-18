# Gateway Server or Client

This is client and server code for a gateway between internal and external network. That's to provide a way to communicate between the inside and the outside of network environment.

## Usage

*use README.md from github*

### Gateway

Rceive **http request** with json and **send json with http properties** to the client and **wait response in json** from client.

### WSClient

**modify process_message method** to handle, process and respond to the message received from the gateway.

You can also send json without modification to communicate with any other server (ws server) with the **simple** parameter.

## Example

### Client

#### Send a request

```python
# Exemple of use
from httpSocketGateway import WSClient
import time

class CustomWSClient(WSClient):

    # Override the process_message method
    def process_message(self, message):
        print("You receive", message)

client = CustomWSClient('localhost', 8080, reconnect=True, simple=True)
client.run()
time.sleep(1)
client.send({
        "Hello": "World"
})
time.sleep(30)
client.stop()
```

#### Receive a request

You should override the `process_message` method from `WSClient` class.

```python
from httpSocketGateway import WSClient
import time

class WebSocketClient(WebSocketBaseClient):
    def process_message(self, message):
        print(f"Received: {message}")

client = WebSocketClient("localhost", 8080, simple=True)
client.run()
time.sleep(1)
client.close()
```

**simple** parameter is used to send json without modification to match with the **gateway server**.

With **simple** parameter you can send json to any other server.


### Gateway

**TODO**
