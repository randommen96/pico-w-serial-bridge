import machine
import socket
import time
from wifi_utils import connect_wifi
import config  # This is your ignored config file

# 1. Use the shared module to connect
if connect_wifi(config.WIFI_SSID, config.WIFI_PASS):
    
    # 2. Local Serial Bridge Logic
    uart = machine.UART(0, baudrate=9600)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_addr = (config.TARGET_IP, 5005)

    print("Starting Serial-to-Network Bridge...")
    while True:
        if uart.any():
            line = uart.readline()
            if line:
                try:
                    sock.sendto(line, target_addr)
                except Exception as e:
                    print(f"Network error: {e}")
        time.sleep(0.01)