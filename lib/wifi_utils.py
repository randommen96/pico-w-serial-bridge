import network
import time

def connect_wifi(ssid, password, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f'Connecting to {ssid}...')
        wlan.connect(ssid, password)
        
        # Wait for connection with a timeout
        start_time = time.time()
        while not wlan.isconnected() and (time.time() - start_time) < timeout:
            time.sleep(1)
            print("...")

    if wlan.isconnected():
        print('Connection successful!')
        print('IP Configuration:', wlan.ifconfig())
        return True
    else:
        print('Connection failed.')
        return False