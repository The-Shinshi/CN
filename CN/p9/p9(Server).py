import socket


def tcp_server():
    host = '127.0.0.1'
    port = 4000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sersock:
        sersock.bind((host, port))
        sersock.listen(1)
        print("Server ready for Connection")
        conn, addr = sersock.accept()

        with conn:
            print("Connection is Successful and waiting for chatting")
            filename = conn.recv(1024).decode()

            try:
                with open(filename, 'r') as file:
                    for line in file:
                        conn.sendall(line.encode())
            except FileNotFoundError:
                conn.sendall(f"File {filename} not found.".encode())


if __name__ == "__main__":
    tcp_server()
