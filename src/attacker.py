import socket
import threading

buffer_size = 30
total_amount_of_attacks = 100

def start_client(raspberry_port, raspberry_name, i):
    '''
    Given the raspberry name and port, sends i messages

    Parameters:
        @raspberry_ip (string): the raspberry which is to be atacked
        @raspberry_port (int): the specific port of said raspberry
        @raspberry_name (string): said raspberry's name
        @i (int): number of messages to send
    '''
    raspberry_ip = socket.gethostbyname(raspberry_name)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)
    client.connect((raspberry_ip, raspberry_port))
    
    while i > 0:
        message = f'Attack number {total_amount_of_attacks-i+1} on {raspberry_name}'
        client.send(message.encode('utf-8'))
    
        # para encher o buffer
        j = buffer_size-len(message)
        print(j, len(message), raspberry_name, 'Mensagem:', message,"!!")

        while j > 0:
            client.send(" ".encode('utf-8'))
            j -= 1

        i = i-1
    
    client.send('PLEASE, EXIT NOW OR DIE!!'.encode('utf-8'))
    j = buffer_size-len('PLEASE, EXIT NOW OR DIE!!')
    while j > 0:
        client.send(" ".encode('utf-8'))
        j -= 1

    client.close()

#def an_attack_instance():

def start_attack(raspberry_port):
    '''
    Sends i messages to all raspberries I have access to

    Parameters:
        @i (int): number of messages to send
    '''
    i = total_amount_of_attacks
    names = ['rasp1', 'rasp3']#, 'rasp8', 'rasp10']
    #raspberry_port = 12345
    threads = []
    
    for raspberry_name in names:
        thread = threading.Thread(target=start_client, args=(raspberry_port, raspberry_name, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
        
start_attack(int(input()))
