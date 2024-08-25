import socket
import threading

def handle_client(client_socket):
    with client_socket:
        print("New client connected")
        try:
            while message := client_socket.recv(1024).decode():
                print(f"Received: {message}")
        except ConnectionResetError:
            print("Client disconnected")

def main():
    port = int(input("Enter the port to listen on: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen()
        print(f"Server is listening on port {port}")

        while True:
            client_socket, _ = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    main()
