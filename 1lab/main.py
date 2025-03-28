import threading
import time
import subprocess

def start_server():
    subprocess.Popen(["python", "server.py"])
    time.sleep(1)

def start_client():
    subprocess.run(["python", "client.py"])

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    print(1)
    
    start_client()