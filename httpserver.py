#! /usr/bin/env python3

import socket

def readline(client_socket: socket.socket) -> str:
    buffer = b""
    while True:
        byte = client_socket.recv(1)
        if not byte:
            break

        buffer += byte
        if byte == b"\n":
            break
    return buffer.decode("utf-8").strip()


def handle_connection(client_socket: socket.socket):
    

    request_line = readline(client_socket)

    print(f"Received: {request_line}")
    request_line_split = request_line.split(" ")
    metoda = request_line_split[0]
    cesta = request_line_split[1]
    verze = request_line_split[2]
    
    print(f"Metoda: {metoda}\nCesta: {cesta}\nVerze: {verze}")
    client_socket.send(b"HTTP/1.1 200 OK\n\nahoj")
    client_socket.close()


# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
port = 8000

# bind the socket to a specific address and port
server.bind((server_ip, port))


# listen for incoming connections
server.listen(0)
print(f"Listening on {server_ip}:{port}")

while True:
    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    handle_connection(client_socket)
