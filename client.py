import pickle 
import socket

HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def handle_create():
    customer_info = {'first_name': r'', 'last_name': r'', 'email': r"", 'password': r"", 'coins': 0}

    name = input('What is your full name: ')
    customer_info['first_name'] = name.split()[0]
    customer_info['last_name'] = name.split()[1]
    email = input('What is your email: ')
    customer_info['email'] = email
    password = input('Please enter a unique password. Must be 10 characters, and contain special characters: ')
    customer_info['password'] = password

    customer_info = pickle.dumps(customer_info)
    client.send(customer_info)

    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))


def send():
    while True:
        cmd = input('How can I help you today? ')
        if cmd.lower() == 'quit': 
            client.sendall(b'Client disconnecting')
            break
        if cmd.lower() == 'create':
            client.sendall(b'create')
            handle_create()
        
        else:
            # sending what client wants
            cmd = cmd.encode(FORMAT)
            client.sendall(cmd)
            # receiving servers response
            msg = client.recv(8000)
            print(msg.decode(FORMAT))

                
send()
