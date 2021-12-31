from hashlib import sha1
import time


def gen_auth_code(sapisid):
    current_time = str(int(time.time()))
    key = f"{current_time}_{sha1(' '.join([current_time, sapisid, 'https://voice.google.com']).encode()).hexdigest()}"
    
    return key
