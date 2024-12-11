import socket


def udp_client():
    host = '127.0.0.1'
    port = 6788
    server_address = (host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as skt:
        msg = "atme college"
        skt.sendto(msg.encode(), server_address)

        data, _ = skt.recvfrom(1024)
        print("Client received: " + data.decode())


if __name__ == "__main__":
    udp_client()
