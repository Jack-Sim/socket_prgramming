import socket
import threading

HEADER = 64
PORT = 5050
SERVER = '192.168.1.102'
FORMAT = 'utf-8'
DISCONNECT_MSG = 'DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def handle_client(conn, addr):
    # Running concurrently for each client
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        # Blocking line of code
        # Will not pass until a message is received
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f"[{addr}] {msg}")
    
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept() # wait on this line for new connection
        # When new connection occurs pass connection to handle client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # How many threads are active in process
        # minus one to account for start thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

print("[STARTING] server is starting")
start()