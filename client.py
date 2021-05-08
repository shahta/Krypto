import pickle 
import socket

HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def log_in():
    credentials = {'user': '', 'pass': '', 'wallet': ''}

    print('[ACCOUNT] Please log in to you account')
    user_name = input('Username (email): ')
    password = input('Passsword: ')
    wallet_id = input('Wallet Address: ')
    credentials['user'] = user_name
    credentials['pass'] = password
    credentials['wallet'] = wallet_id

    client.send(pickle.dumps(credentials))
    success_msg = client.recv(8000).decode(FORMAT)
    if 'Logged in' in success_msg:
        print(success_msg)
        return True
    else:
        print('[ACCOUNT] Log in failed')
        return False

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
    
    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))

def handle_deposit():
    invalid = True
    coins = 0
    while invalid:
        coins = (input('How many bitcoins would you like to deposit (must be more than 0): '))
        if float(coins) > 0:
            invalid = False

    client.send(coins.encode(FORMAT))

    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))

def handle_transfer():
    amount = input('How many coins would you like to transfer: ')
    email = input('What is the email of the recipient: ')
    address = input('What is the bitcoin wallet address of the recipient: ')
    transfer_info = {'amount': float(amount), 'email': email, 'address': address}

    client.send(pickle.dumps(transfer_info))

    finish_msg = client.recv(8000)
    print(finish_msg.decode(FORMAT))

def send():
    logged_in = False
    while True:
        cmd = input('How can I help you today? ').lower()
        if cmd == 'quit' or cmd == 'log off': 
            client.sendall(b'Client disconnecting')
            break
        if 'create' in cmd:
            client.sendall(b'create')
            handle_create()
        if not logged_in:
            client.sendall(b'log in')
            log_success = log_in()
            if log_success: logged_in = True
        if 'transfer' in cmd:
            client.sendall(b'transfer')
            handle_transfer()
        if 'balance' in cmd:
            client.sendall(b'balance')
            handle_balance()       
        if 'deposit' in cmd:
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
