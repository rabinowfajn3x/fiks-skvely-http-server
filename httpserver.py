#! /usr/bin/env python3

import socket
import os

koncovky = {".html":"text/html",".css":"text/css",".txt":"text/plain","":"application/octet-stream",".jpg":"image/jpeg",".png":"image/png",".ico":"image/x-icon"}


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
    try:
        radky=[]
        while True:
            request_line = readline(client_socket).strip()
            if request_line == "":
                # print("mame vse.")
                break
            radky.append(request_line)
            # print("radka:"+request_line)
        
                    
        status_code = "200 OK"
        # print(f"Received: {request_line}")
        prvni_radka = radky[0].split(" ")
        if len(prvni_radka)!=3:
            pass    
        metoda = prvni_radka[0]
        if metoda != "GET":
            raise Exception
        
        if prvni_radka[1] == "/":
            prvni_radka[1]="/index.html"
        
        cesta = os.path.join("folder",prvni_radka[1][1:])
        print(cesta)
        if "../" in cesta:
            status_code = "403 Forbidden"
            odpoved = b"<h1>Forbidden!</h1>"
            odpovidani(status_code, odpoved,"text/html")
            return 

        verze = prvni_radka[2]
        
        trash, extension = os.path.splitext(cesta)
        content_type = koncovky[extension]
        try:
            with open(cesta,"rb") as soubor:
                odpoved = soubor.read()
                
        except FileNotFoundError:
            with open("errors/404.html","rb") as soubor:
                odpoved = soubor.read()
            status_code="404 Not Found"
            content_type="text/html"
 

    except Exception as e:
        status_code="500 :("
        with open("errors/500.html","rb") as soubor:
            odpoved = soubor.read()
 
        content_type="text/html"
        print(f"exception je {e}")

    odpovidani(status_code,odpoved,content_type)

    # odpoved = f"metoda: {metoda}\ncesta: {cesta}\nverze: {verze}\n" 



def odpovidani(status_code, odpoved,content_type):

    # print(f"Metoda: {metoda}\nCesta: {cesta}\nVerze: {verze}")
    client_socket.send(f"HTTP/1.1 {status_code}\r\nContent-Type: {content_type}\r\nContent-Length: {len(odpoved)}\r\n\r\n".encode("utf-8"))

    client_socket.send(odpoved)

    client_socket.send("\r\n".encode("utf-8"))

    client_socket.close()

    

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "0.0.0.0"
port = 8000

# bind the socket to a specific address and port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind((server_ip, port))

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
    server.shutdown(socket.SHUT_RDWR)
    server.close()
