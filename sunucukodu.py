import socket
import threading

ho = socket.gethostname()
ip_adress = socket.gethostbyname(ho)
HOST = ip_adress
PORT = 8080

clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message)
            else:
                remove(client)
                break
        except:
            remove(client)
            break

def remove(client):
    if client in clients:
        clients.remove(client)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"[*] Listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

            clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

if __name__ == '__main__':
    start_server()