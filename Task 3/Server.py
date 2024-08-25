import socket
import threading
import json

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # {client_id: (socket, topic)}
        self.topics = {}  # {topic: [client_id]}

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, addr = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def handle_client(self, client_socket):
        client_id = id(client_socket)
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                if message['type'] == 'publish':
                    topic = message['topic']
                    self.broadcast(topic, message['data'])
                elif message['type'] == 'subscribe':
                    topic = message['topic']
                    self.subscribe(client_id, client_socket, topic)
                elif message['type'] == 'unsubscribe':
                    topic = message['topic']
                    self.unsubscribe(client_id, topic)
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        self.close_client(client_id)

    def broadcast(self, topic, message):
        for client_id in self.topics.get(topic, []):
            client_socket, _ = self.clients[client_id]
            try:
                client_socket.sendall(json.dumps({'type': 'message', 'topic': topic, 'data': message}).encode())
            except Exception as e:
                print(f"Error broadcasting message: {e}")

    def subscribe(self, client_id, client_socket, topic):
        self.clients[client_id] = (client_socket, topic)
        self.topics.setdefault(topic, []).append(client_id)

    def unsubscribe(self, client_id, topic):
        if client_id in self.topics.get(topic, []):
            self.topics[topic].remove(client_id)
        if client_id in self.clients:
            del self.clients[client_id]

    def close_client(self, client_id):
        if client_id in self.clients:
            client_socket, topic = self.clients[client_id]
            client_socket.close()
            del self.clients[client_id]
            if topic in self.topics:
                self.topics[topic].remove(client_id)

if __name__ == '__main__':
    server = Server('127.0.0.1', 5000)
    server.start()
