import socket

def main():
    if len(args := input("Enter server IP and port (e.g., 127.0.0.1 65432): ").split()) != 2:
        print("Usage: Enter server IP and port separated by a space")
        return

    hostname, port = args[0], int(args[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((hostname, port))
            print("Connected to the server")

            while True:
                text = input("Enter message: ")

                if text.lower() == "terminate":
                    print("Terminating connection...")
                    break

                s.sendall(text.encode())

        except socket.gaierror:
            print("Server not found")
        except ConnectionRefusedError:
            print("Connection refused by the server")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
