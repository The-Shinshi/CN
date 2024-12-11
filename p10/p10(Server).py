import socket


def udp_server():
    host = '127.0.0.1'
    port = 6788

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as skt:
        skt.bind((host, port))
        print("Server is started and waiting for connection...")

        while True:
            data, addr = skt.recvfrom(1024)
            message = data.decode().split(" ")
            send_msg = (message[1].upper() + " from server to client").encode()
            skt.sendto(send_msg, addr)


if __name__ == "__main__":
    udp_server()
