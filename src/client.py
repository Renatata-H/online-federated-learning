from config import *
from header import *

"""
def echo_client(ip: str, port: int, message: str) -> None:
    '''
    Sends a message to the echo server and prints the response.
    
    :param str ip: IP address of the server.
    :param int port: Port number of the server.
    :param str message: The message to be sent to the server.
    '''
    try:
        connection = connect_to(ip, port)
    
        connection.sendall(message.encode())
        logging.info(f"Sent message: {message}")
        print(f"Sent message: {message}")
        
        data = connection.recv(1024)
        logging.info(f"Received echoed message: {data.decode('utf-8')}")
        print(f"Received echoed message: {data.decode('utf-8')}")
    
    except (ValueError, socket.error) as e:
        logging.error(f"Error during client communication: {e}")
    
    finally:
        connection.close()

if __name__ == "__main__":
    message = "Hello, Echo Server!"
    echo_client(server_ip, server_port, message)
"""

message_buffer = []
received_responses = []
lock = threading.Lock()

server_connection = None

def send_to_server(message: str):
    '''
    Sends data to server via persistent connection
    '''
    global server_connection
    try:
        server_connection.sendall(str(message).encode())
        response = server_connection.recv(buffer_size)
        result = response.decode().strip()
        received_responses.append(result)
        print(f"[Worker] Received result from server: {result}")

    except Exception as e:
        print(f"[Worker] Error communicating with server!!: {e}")

def process_attack(data: bytes):
    '''
    Called for every message received from attacker
    '''
    message = data.decode().strip()

    with lock:
        message_buffer.append(int(message))
        print(message_buffer)

        if len(message_buffer) >= MESSAGE_BUFFER_SIZE:
            #send_to_server("1")
            send_to_server(sum(message_buffer))
            message_buffer.clear()

    return ""

def maintain_connection_to_server():
    '''
    Establishes and stores a long-lived connection to the server
    '''
    global server_connection
    while True:
        try:
            server_connection = connect_to(server_ip, server_port)
            print(f"[Worker] Connected to server at {server_ip}:{server_port}")
            break
        except Exception as e:
            print(f"[Worker] Failed to connect to server: {e}. Retrying in 2s...")
            time.sleep(2)

if __name__ == "__main__":
    maintain_connection_to_server()
    print(f"[Worker] Listening for attackers on port {worker_port}...")
    start_server("0.0.0.0", worker_port, process_attack)