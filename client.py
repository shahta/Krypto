import socket

HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send():
    while True:
        cmd = input('How can I help you today? ')
        if cmd.lower() == 'quit': 
            client.sendall(b'Client disconnecting')
            break
        cmd = bytes(cmd.encode(FORMAT))
        client.sendall(cmd)
        cmd = client.recv(2048)
        print(cmd.decode(FORMAT))

                
send()
