from config import *
from header import *

"""
    def echo_process_func(data: bytes) -> str:
        # servidor echo pra teste só
        return data.decode('utf-8')

    if __name__ == "__main__":
        start_server(server_ip, server_port, echo_process_func)
"""

def process_worker_data(data: bytes) -> str:
    '''
    Handles incoming data from workers.
    Accumulates it, and once a round is over, sends results to everyone.
    '''
    try:
        decoded = data.decode().strip()
        sender = threading.current_thread().name

        with round_data_lock:
            worker_data[sender] = int(decoded)

    except Exception as e:
        logging.error(f"Error processing data: {e}")

    return ""


def round_manager():
    '''
    Orchestrates each round: waits 5 seconds, sums inputs, broadcasts.
    '''
    global connections

    while True:
        time.sleep(ROUND_TIMEOUT)

        with round_data_lock:
            if connections:
                result = sum(worker_data.values())
                logging.info(f"Round result: {result} from {len(worker_data)} clients")
            else:
                result = -1
                logging.info(f"Bad round result: no data received from {len(worker_data)} clients")

            for connection in connections.values():
                try:
                    connection.sendall(str(result).encode())
                except Exception as e:
                    logging.error(f"Broadcast error: {e}")
            worker_data.clear()

if __name__ == '__main__':
    threading.Thread(target=round_manager, daemon=True).start()
    start_server(server_ip, server_port, process_func=lambda x: "", timeout=5)
