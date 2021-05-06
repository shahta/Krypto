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

    first_name = input('What is your first name: ')
    customer_info['first_name'] = first_name
    last_name = input('What is your last name: ')
    customer_info['last_name'] = last_name
    email = input('What is your email: ')
    customer_info['email'] = email
    password = input('Password (must contain at least 10 characters, special character, uppercase): ')
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
        if 'create' in cmd.lower():
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
