import pickle 
import socket

HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

def handle_create():
    customer_info = {'first_name': r'', 'last_name': r'', 'email': r"", 'password': r"", 'coins': 0.0}

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
    credentials = __log_in()

    credentials = pickle.dumps(credentials)
    client.send(credentials)

    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))

def handle_deposit():
    credentials = __log_in()

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

def handle_transfer():
    credentials = __log_in()

    amount = input('How many coins would you like to transfer: ')
    email = input('What is the email of the recipient: ')
    address = input('What is the bitcoin wallet address of the recipient: ')
    transfer_info = {'amount': float(amount), 'email': email, 'address': address}

    client.send(pickle.dumps(credentials))
    client.send(pickle.dumps(transfer_info))

    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))

def __log_in():
    credentials = {'user': '', 'pass': '', 'wallet': ''}

    print('[ACCOUNT] Please log in to you account')
    user_name = input('Username (email): ')
    password = input('Passsword: ')
    wallet_id = input('Wallet Address: ')
    credentials['user'] = user_name
    credentials['pass'] = password
    credentials['wallet'] = wallet_id

    return credentials

def send():
    while True:
        cmd = input('How can I help you today? ')
        if cmd.lower() == 'quit': 
            client.sendall(b'Client disconnecting')
            break
        if 'create' in cmd.lower():
            client.sendall(b'create')
            handle_create()
        if 'transfer' in cmd.lower():
            client.sendall(b'transfer')
            handle_transfer()
        if 'balance' in cmd.lower():
            client.sendall(b'balance')
            handle_balance()       
        if 'deposit' in cmd.lower():
            client.sendall(b'deposit')
            handle_deposit()       
        else:
            # sending what client wants
            cmd = cmd.encode(FORMAT)
            client.sendall(cmd)
            # receiving servers response
            msg = client.recv(8000)
            print(msg.decode(FORMAT))

                
send()
