server_ip = '0.0.0.0' #removido mas endereço da prestigio
server_port = 50505

num_workers = 1#3
workers_names = 'A' #'0.0.0.0'#['rasp1', 'rasp3', 'rasp5']
worker_port = 60606

contaminated_data = True
contamination_algorithm = None
data_path = './data/BoT-IoT.pcap'

ROUND_TIMEOUT = 5
MESSAGE_BUFFER_SIZE = 10
buffer_size = 1024

logname = './logs/app.log'
global_logname = './logs/global.log'


