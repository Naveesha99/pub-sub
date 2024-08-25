import socket
import json
import sys

def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    role = sys.argv[3]
    topic = sys.argv[4]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    if role == 'PUBLISHER':
        while True:
            message = input("Enter message: ")
            data = {'type': 'publish', 'topic': topic, 'data': message}
            client_socket.sendall(json.dumps(data).encode())
    elif role == 'SUBSCRIBER':
        data = {'type': 'subscribe', 'topic': topic}
        client_socket.sendall(json.dumps(data).encode())
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = json.loads(data.decode())
            if message['type'] == 'message':
                print(f"Received message on topic {message['topic']}: {message['data']}")

    client_socket.close()

if __name__ == '__main__':
    main()
