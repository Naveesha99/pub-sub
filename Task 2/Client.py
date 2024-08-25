import socket
import sys

def client(host, port, client_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(client_type.encode())
        if client_type == "PUBLISHER":
            while True:
                msg = input("Enter message: ")
                s.sendall(msg.encode())
        elif client_type == "SUBSCRIBER":
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print(msg.decode())

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <publisher|subscriber>")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    client_type = sys.argv[3]
    client(host, port, client_type)
