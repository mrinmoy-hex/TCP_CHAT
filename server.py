import threading
import socket

HOST = "127.0.0.1"                          # local host
PORT = 6555 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}


def broadcast(message):
    for client in clients:
        client.send(message)
        
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            nickname = clients.pop(client)
            client.close()
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            
            break
        
        
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        clients[client] = nickname
        
        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        
        client.send("Connected to the server!".encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,), daemon=True)
        thread.start()
        
        
receive()