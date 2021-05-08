from mysql.connector import connect
import pickle
import socket
from src.Config import Config
from src.Wallet import Wallet
import threading

# Constants
HOST = "localhost" 
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

# db connection
cnx = connect(
    user=Config.DB['user'],
    password=Config.DB['password'],
    host=Config.DB['host'],
    database=Config.DB['database'],
)
        
# Server Socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

def handle_client(conn, addr):
    print('Connected to', addr)
    account = Wallet(conn, cnx)

    while True:
        msg = conn.recv(8000).decode(FORMAT)
        if msg:
            if msg == "quit" or msg == 'log off': 
                break
            if msg == 'log in':
                credentials = conn.recv(8000)
                credentials = pickle.loads(credentials)
                if credentials:
                    account.log_in(credentials)
            if msg == 'create':
                customer_info = conn.recv(8000)
                customer_info = pickle.loads(customer_info)
                if customer_info:
                    account.create_account(customer_info)
            if msg == 'balance':
                account.check_balance()
            if msg == 'deposit':
                coins = conn.recv(8000).decode(FORMAT)
                if coins:
                    account.deposit(float(coins))
            if msg == 'transfer':
                transfer_info = conn.recv(8000)
                transfer_info = pickle.loads(transfer_info)
                if transfer_info:
                    account.transfer(transfer_info)
            else:   
                print(f"[User {addr[1]}] {msg}")
                conn.send(b'Message Received')

    conn.close()

def start():
    print(f"Server starting on {HOST}")
    s.listen()

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.active_count() - 1} Connections Active")


start()

