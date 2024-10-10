import subprocess
import sys
import psutil
import subprocess
import time
import os
import socket
from datetime import datetime

required_packages = ["psutil"]

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
white = '\033[97m'
yellow = '\033[93m'

current_date = datetime.now().strftime("%Y-%m-%d")
log_file_path = f"Rat_network_log_{current_date}.txt"

def write_to_log(log_data):
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(log_data + "\n")
    except Exception as e:
        print(f"{red}Fehler beim Schreiben in die Log-Datei: {e}{end}")

def ping_ip(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', ip], stderr=subprocess.STDOUT, universal_newlines=True, encoding='cp850')
        for line in output.splitlines():
            if "Zeit=" in line:
                return int(line.split('Zeit=')[1].split()[0].replace("ms", ""))
    except subprocess.CalledProcessError:
        return None

def get_host_by_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

while True:
    os.system('cls')

    header = f"{'IP Address':<20}{'Host':<30}{'Status':<15}{'Ping (ms)':<10}"
    separator = "="*75
    print(f"{white}{header}")
    print(f"{white}{separator}")

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n--- {current_time} ---\n{header}\n{separator}"
    write_to_log(log_entry)

    connections = psutil.net_connections(kind='inet')

    for conn in connections:
        if conn.raddr:
            ip = conn.raddr.ip
            status = conn.status
            ping = ping_ip(ip)
            host = get_host_by_ip(ip)

            if ping is None:
                ping_color = f"{red}N/A{end}"
                ping_log = "N/A"
            elif ping > 150:
                ping_color = f"{red}{ping}ms{end}"
                ping_log = f"{ping}ms"
            else:
                ping_color = f"{green}{ping}ms{end}"
                ping_log = f"{ping}ms"

            if status in ["CLOSE_WAIT", "TIME_WAIT", "LAST_ACK"]:
                status_color = f"{red}{status:<15}{end}"
            else:
                status_color = f"{yellow}{status:<15}{end}"

            display_host = host if len(host) <= 25 else host[:25] + "..."
            print(f"{white}{ip:<20}{display_host:<30}{status_color}{ping_color}")

            log_line = f"{ip:<20}{host:<30}{status:<15}{ping_log}"
            write_to_log(log_line)

    time.sleep(1)

#By Mausi Schmausi