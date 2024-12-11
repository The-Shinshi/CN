import socket


def tcp_client():
    host = '127.0.0.1'
    port = 4000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print("Enter the filename:")
        filename = input()
        sock.sendall(filename.encode())
        data = sock.recv(1024).decode()
        while data:
            print(data)
            data = sock.recv(1024).decode()


if __name__ == "__main__":
    tcp_client()
