import socket

UDP_IP = "0.0.0.0" # Listen on all interfaces
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening for Pico data on port {UDP_PORT}...")

with open("pico_logs.txt", "a") as f:
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8').strip()
        print(f"Received: {message}")
        f.write(message + "\n")
        f.flush() # Ensure it writes to disk immediately