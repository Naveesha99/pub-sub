import socket
import threading

clients = []
subscribers = []

def handle_client(client_socket, addr):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print(f"Received from {addr}: {msg}")
            for client in clients:
                if client != client_socket and client in subscribers:
                    client.send(msg.encode())
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print("Server listening on", host, ":", port)

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected by', addr)
        clients.append(client_socket)
        client_type = client_socket.recv(1024).decode()
        if client_type == "SUBSCRIBER":
            subscribers.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
