import ipaddress, socket, re, logging, threading, signal, time, random

from queue import Queue
from config import logname, global_logname, buffer_size

REGEX_IP_VERIFIER = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
round_data_lock = threading.Lock()
connections = {}
worker_data = {}

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(logname)#,  
        #logging.StreamHandler()  
    ]
)


def valid_ip4_address(ip: str) -> bool:
    '''
    Validates IPv4 address as valid

    :param str ip: the IPv4 to be verified
    :return: True if the address is valid, False if otherwise
    :rtype: bool
    '''

    if (re.search(REGEX_IP_VERIFIER, ip)):
        return True
    return False 


def resolve_domain_to_ip(domain: str) -> str:
    '''
    Resolves a domain name to its address.

    :param str domain: the domain name to be resolved 
    :return: the resolved address
    :rtype: str
    :raises socket.gaierror: if the domain name cannot be resolved.
    '''

    try:
        ip = socket.gethostbyname(domain)
        return ip

    except socket.gaierror:
        logging.error(f"Could not resolve {domain} into address")
        raise ValueError(f"Could not resolve domain name: {domain}")


def set_logs(logname: str, global_logname: str) -> None:
    '''
    Appends the log to the global log file and cleans the log file.

    :param str logname: name of the log file
    :param str global_logname: name of the global log file
    :raises ValueError: if the names provided are not valid
    '''
    if ((type(logname) != str) or (type(global_logname) != str)):
        logging.error(f"Invalid file name")
        raise ValueError("Name of log file needs to be valid.")

    with open(logname, 'r') as src, open(global_logname, 'a') as dst:
        dst.write(src.read())

    open(logname, 'w').close()

    return


def connect_to(ip: str, port: int, timeout: int = 5) -> socket.socket:
    '''
    Connects to server listening on the specified IP and port.

    :param str ip: the IPv4 address of the server.
    :param int port: the port number where the server is listening (49152–65535).
    :return: a connected socket object (TCP, IPv4) with a timeout.
    :rtype: socket.socket
    :raises ValueError: if the IP is not a valid IPv4 address or port is out of range.
    :raises socket.error: if a socket-level error occurs during connection.
    '''

    if ((type(port) != int) or (49152 > port) or (65335 < port)):
        logging.error(f"Tried to access invalid port: {port}")
        raise ValueError("Server port needs to be an integer between 49152 and 65535 (inclusive).")

    if ((type(ip) != str) or (not valid_ip4_address(ip))):
        logging.error(f"Tried to access invalid IP address: {ip}")
        raise ValueError("Server IP needs to be a string of a valid IPv4 address.")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout) 
        s.connect((ip, port))
    
        logging.info(f"Connected successfully to {ip}:{port}")

        return s  

    except socket.timeout:
        logging.warning(f"Connection to {ip}:{port} timed out after {timeout} seconds.")
        raise

    except socket.error as e:
        logging.error(f"Socket error occurred while connecting to {ip}:{port}: {e}")
        raise


def handle_client(connection: socket.socket, address: tuple, process_func, timeout: int = 5) -> None:
    '''
    Handles communication with a connected client.
    This function includes a placeholder where to pass a custom function for processing data.

    :param socket connection: socket object of the connection with the client.
    :param tuple address: address of the client (IP, Port).
    :param function process_func: function that will process the received data.
    :param int timeout: the timeout in seconds for socket operations. default is 5 seconds.
    :raises socket.timeout: if the socket operation times out.
    :raises socket.error: if any socket-level error occurs during communication.
    '''

    logging.info(f"Handling client at {address}")
    thread_name = threading.current_thread().name
    connections[thread_name] = connection

    try:
        #connection.settimeout(timeout)
        while True:
            data = connection.recv(buffer_size)
            
            if not data:
                logging.info(f"Client at {address} disconnected.")
                break

            process_func(data)
            #response = process_func(data)
            #connection.sendall(response.encode())

    except socket.timeout:
        logging.warning(f"Socket timed out while communicating with {address}.")

    except socket.error as e:
        logging.error(f"Socket error occurred while handling client {address}: {e}")

    finally:
        connection.close()
        logging.info(f"Connection closed with {address}")
        with round_data_lock:
            if thread_name in connections:
                del connections[thread_name]


def start_server(ip: str, port: int, process_func, timeout: int = 5) -> None:
    '''
    Starts a server that listens for client connections on the specified IP and port.

    :param str ip: The IP address of the server (use '0.0.0.0' to listen on all interfaces).
    :param int port: The port number where the server will listen (49152–65535).
    :param function process_func: function that will process the received data.
    :param int timeout: The timeout in seconds for socket operations. default is 5 seconds.
    :raises ValueError: if the IP is not a valid IPv4 address or port is out of range.
    :raises socket.error: if a socket-level error occurs during connection.
    '''

    if ((type(port) != int) or (49152 > port) or (65335 < port)):
        logging.error(f"Tried to access invalid port: {port}")
        raise ValueError("Server port needs to be an integer between 49152 and 65535 (inclusive).")

    if ((type(ip) != str) or (not valid_ip4_address(ip))):
        logging.error(f"Tried to access invalid IP address: {ip}")
        raise ValueError("Server IP needs to be a string of a valid IPv4 address.")

    shutdown_event = threading.Event()
    active_threads = []

    handler = lambda sig, frame: (logging.info("Shutting down server..."), shutdown_event.set())
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen()

        info_prompt = f"Server listening on {ip}:{port}..."
        logging.info(info_prompt)
        print(info_prompt)

        while not shutdown_event.is_set():
            try:
                server.settimeout(0.5)
                connection, address = server.accept()
                thread = threading.Thread(target=handle_client, args=(connection, address, process_func, timeout), daemon=True)
                thread.start()
                active_threads.append(thread)
            
            except socket.timeout:
                continue

            except socket.error as e:
                logging.error(f"Socket error: {e}")
                break

            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

        logging.info("Server is waiting for active threads to finish...")

        for thread in active_threads:
            thread.join() 

        logging.info("Server has shut down.")
        set_logs(logname, global_logname)


