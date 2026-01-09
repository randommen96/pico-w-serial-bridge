import socket
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for Pico data on port {UDP_PORT}...")

with open("pico_logs.txt", "a") as f:
    while True:
        data, addr = sock.recvfrom(4096) # Increased buffer size
        
        # 1. Use 'replace' to swap invalid bytes with a '?' instead of crashing
        # 2. Get the current timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        try:
            # Decode and handle errors
            message = data.decode('utf-8', errors='replace').rstrip()
            
            # Format the line with a timestamp
            output = f"[{now}] {message}"
            
            print(output)
            f.write(output + "\n")
            f.flush()
        except Exception as e:
            print(f"[{now}] System Error processing packet: {e}")