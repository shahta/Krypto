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

def handle_balance():
    credentials = {'user': '', 'pass': '', 'wallet': '', 'deposit': 0}

    user_name = input('Username (email): ')
    password = input('Passsword: ')
    wallet_id = input('Wallet Address: ')
    credentials['user'] = user_name
    credentials['pass'] = password
    credentials['wallet'] = wallet_id

    deposit = input('Would you like to make a deposit today? (y/N) ')
    if deposit.lower() == 'y':
        invalid = True
        coins = 0
        while invalid:
            coins = input('How many bitcoins would you like to deposit (must be more than 0): ')
            if float(coins) > 0:
                credentials['deposit'] = coins
                invalid = False
    
    credentials = pickle.dumps(credentials)
    client.send(credentials)

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
        if 'balance' in cmd.lower() or 'deposit' in cmd.lower():
            client.sendall(b'balance')
            handle_balance()       
        else:
            # sending what client wants
            cmd = cmd.encode(FORMAT)
            client.sendall(cmd)
            # receiving servers response
            msg = client.recv(8000)
            print(msg.decode(FORMAT))

                
send()
