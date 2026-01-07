import machine
import socket
import time
from wifi_utils import connect_wifi
import config 

# 1. Use the shared module to connect
if connect_wifi(config.WIFI_SSID, config.WIFI_PASS):
    
    # 2. Local Serial Bridge Logic
    # Added rxbuf=1024: This increases the Pico's internal hardware buffer 
    # so it can hold more data while the WiFi chip is busy sending.
    uart = machine.UART(0, baudrate=9600, rxbuf=1024)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_addr = (config.TARGET_IP, 5005)

    print(f"Starting Serial-to-Network Bridge (Target: {config.TARGET_IP})...")
    
    while True:
        # Drain the UART buffer: Process ALL lines currently waiting
        # before allowing the script to sleep.
        while uart.any():
            line = uart.readline()
            if line:
                try:
                    sock.sendto(line, target_addr)
                except Exception as e:
                    # If WiFi blips, we print the error but keep the loop running
                    print(f"Network error: {e}")
        
        # Reduced sleep to 1ms. This is the "breathing room" for the Pico 
        # background tasks without causing significant data lag.
        time.sleep_ms(1)