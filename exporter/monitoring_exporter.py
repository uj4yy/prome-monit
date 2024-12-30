from prometheus_client import start_http_server, Gauge                                                                                                                              # type: ignore
import psutil
import time

ram_usage = Gauge('system_memory_usage_bytes', 'Total RAM usage in bytes')
disk_usage = Gauge('system_disk_usage_bytes', 'Total disk usage in bytes')
disk_available = Gauge('system_disk_available_bytes', 'Available disk space in bytes')
cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
process_count = Gauge('system_process_count', 'Number of active processes')
network_sent = Gauge('system_network_sent_bytes', 'Total network sent in bytes')
network_received = Gauge('system_network_received_bytes', 'Total network received in bytes')

def collect_metrics():
    ram = psutil.virtual_memory()
    ram_usage.set(ram.used)  
    
    disk = psutil.disk_usage('/')
    disk_usage.set(disk.used)  
    disk_available.set(disk.free)  

    cpu_usage.set(psutil.cpu_percent(interval=1))

    process_count.set(len(psutil.pids()))

    net_io = psutil.net_io_counters()
    network_sent.set(net_io.bytes_sent)
    network_received.set(net_io.bytes_recv)

if __name__ == '__main__':
    start_http_server(8000)
    print("Exporter running on http://localhost:8000")
    while True:
        collect_metrics()
        time.sleep(5)   