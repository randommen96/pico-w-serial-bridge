import machine
import socket
import time
from wifi_utils import connect_wifi
import config 

# 1. Use the shared module to connect
if connect_wifi(config.WIFI_SSID, config.WIFI_PASS):
    
    # 2. Setup UART with a larger buffer
    uart = machine.UART(0, baudrate=9600, rxbuf=1024)
    
    # 3. Setup Networking
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target_addr = (config.TARGET_IP, 5005)

    # 4. Send "Alive" message immediately on startup
    # We include uptime (ticks_ms) so you know if the Pico just rebooted
    uptime = time.ticks_ms()
    startup_msg = f"--- Pico System Online (Uptime: {uptime}ms) ---\n"
    try:
        sock.sendto(startup_msg.encode(), target_addr)
        print("Sent 'Alive' message to receiver.")
    except Exception as e:
        print(f"Failed to send startup message: {e}")

    print(f"Bridge active. Forwarding Serial -> {config.TARGET_IP}:5005")
    
    while True:
        # Drain the UART buffer
        while uart.any():
            line = uart.readline()
            if line:
                try:
                    # We use the raw bytes from UART directly for efficiency
                    sock.sendto(line, target_addr)
                except Exception as e:
                    print(f"Network error: {e}")
        
        # Tight loop with minimal sleep
        time.sleep_ms(1)