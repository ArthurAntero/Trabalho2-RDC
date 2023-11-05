import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(5)

clients = {}
enderecos = {}

def lidar_cliente(client):
    username = client.recv(1024).decode()
    client.send(bytes(f"Você está logado como {username}!", "utf8"))
    msg = f"{username} entrou no chat!"
    enviar_msg(bytes(msg, "utf8"))
    clients[client] = username
    while True:
        msg = client.recv(1024)
        if msg != bytes("{quit}", "utf8"):
            decoded_msg = msg.decode().split(":")
            sender, recipient, message = decoded_msg
            
            if recipient == '':
                enviar_msg(bytes(f"{sender}: {message}", "utf8"))


            elif len(decoded_msg) == 3:
                if recipient in [clients[client] for client in clients]:
                    for client_socket, client_name in clients.items():
                        if client_name == recipient or client_name == sender:
                            client_socket.send(bytes(f"{sender} diz para {recipient}: {message}", "utf8"))
                else:
                    client.send(bytes(f"Usuário {recipient} não encontrado.", "utf8"))
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            enviar_msg(bytes(f"{username} saiu do chat.", "utf8"))
            break

def enviar_msg(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, "utf8") + msg)

while True:
    client, client_address = server.accept()
    enderecos[client] = client_address
    threading.Thread(target=lidar_cliente, args=(client,)).start()