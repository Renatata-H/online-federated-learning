from config import *
from header import *

def send_random_numbers(ip: str):
    try:
        conn = connect_to(ip, worker_port)
        print(f"[Attacker] Connected to {ip}:{worker_port}")

        while True:
            value = str(random.randint(1, 100))
            conn.sendall(value.encode())
            time.sleep(0.1)

    except Exception as e:
        print(f"[Attacker] Failed to send to {ip}: {e}")

if __name__ == "__main__":
    for worker in workers_names:
        #thread = threading.Thread(target=send_random_numbers, args=(resolve_domain_to_ip(worker),), daemon=True)
        thread = threading.Thread(target=send_random_numbers, args=('0.0.0.0',), daemon=True)
        thread.start()

    while True:
        time.sleep(10)