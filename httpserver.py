#! /usr/bin/env python3

import socket

def readline(client_socket: socket.socket) -> str:
    buffer = b""
    while True:
        byte = client_socket.recv(1)
        if not byte:
            break

        buffer += byte
        # print(f"Bajt:{byte}")
        if byte == b"\n":

            break
    return buffer.decode("utf-8")


def handle_connection(client_socket: socket.socket):
    radky=[]
    while True:
        request_line = readline(client_socket).strip()
        if request_line == "":
            # print("mame vse.")
            break
        radky.append(request_line)
        # print("radka:"+request_line)
    
                
    status_code = "500 proste chyba"
    # print(f"Received: {request_line}")
    prvni_radka = radky[0].split(" ")
    if len(prvni_radka)!=3:
        pass    
    metoda = prvni_radka[0]
    cesta = prvni_radka[1]
    verze = prvni_radka[2]
    odpoved = f"metoda: {metoda}\ncesta: {cesta}\nverze: {verze}\n" 
    odpovidani(status_code, odpoved)



def odpovidani(status_code, odpoved):

    content_type = "text/plain; charset=UTF-8"
    # print(f"Metoda: {metoda}\nCesta: {cesta}\nVerze: {verze}")
    client_socket.send(f"HTTP/1.1 {status_code}\r\nContent-Type: {content_type}\r\nContent-Length: {len(odpoved)}\r\n\r\n{odpoved}\r\n".encode("utf-8"))
    client_socket.close()
    

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "0.0.0.0"
port = 8000

# bind the socket to a specific address and port
server.bind((server_ip, port))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# listen for incoming connections
server.listen(0)
print(f"Listening on {server_ip}:{port}")
try:
    while True:
        # accept incoming connections
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        handle_connection(client_socket)

finally: 
    server.close()
