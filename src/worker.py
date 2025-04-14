import socket
import threading

messages_by_port = {}
weights_by_port = {}
operator_port = 12344
operator_id = '0.0.0.0' # <-- substitute for the central's IP
buffer_size = 30

def training():
    pass

def new_weigths(weights):
    pass

def handle_client(client_socket, client_address, port):
    while True:
        message = client_socket.recv(buffer_size).decode('utf-8')

        if message == 'PLEASE, EXIT NOW OR DIE!!':
            break

        print(f"[Recebido da {client_address} na porta {port}]: {message}")

        if port in messages_by_port:
            messages_by_port[port].append(message)
        else:
            messages_by_port[port] = [message]
    
        if len(messages_by_port[port]) % 10 == 0:
            # aqui a gente treinaria o modelo para atualizar os pesos
            print(f"tenho {len(messages_by_port[port])} armazenadas") #debug
            training()
            send_to_operator(port)
    
    client_socket.close()

def send_to_operator(port):
    operator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    operator_socket.connect((operator_id, operator_port))

    operator_socket.send(f"finge que foram enviados pesos referentes a {port}.".encode('utf-8'))
    response = operator_socket.recv(1024).decode('utf-8')
    print(f"[Operador enviou pesos atualizados]: {response}")
    # aqui a gente atulizaria os pesos com aqueles enviados pelo operador
    new_weigths(response)

    messages_by_port[port] = []
    operator_socket.close()

def start_server_for_port(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)

    # pra cada porta possivel, escuta
    while True:
        client_socket, client_address = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address, port)).start()

def listen_on_ports(ports):
    # pra cada porta listada faz thread
    for port in ports:
        if port != operator_port: 
            thread = threading.Thread(target=start_server_for_port, args=(port,))
            thread.start()

def start_rapsberry(ports_to_listen):
    #ports_to_listen = [12346, 12347, 12348]
    listen_on_ports(ports_to_listen)

start_rapsberry([12346])
