import socket
import threading

responses = {}
counter = 0
port = 12344

def consensus():
    return 0

def handle_client(client_socket, client_address):
    global counter
    message = client_socket.recv(1024).decode('utf-8')

    ##### isso aqui é só temporário, pra exemplificar
    # o que se poderia fazer. Na teoria, a gente faria aqui
    # as contas do consenso. Usaria-se o message pra isso
    counter += 1
    #####################
    
    responses[client_address] = message    # <-- Aqui poderíamos armazenar os pesos enviados pelo cliente
    print(f"[{client_address} enviou]: {message}")
    
    # enviaria aqui o resultado dos cálculos
    new_weights = consensus()
    client_socket.send(f"{counter}º peso registrado (maquina {client_address}): '{new_weights}'".encode('utf-8'))
    
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    print("[Servidor iniciado!]")

    while True:
        client_socket, client_address = server.accept()
        print(f"[{client_address} conectou]")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


start_server()

