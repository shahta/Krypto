from mysql.connector import connect
import pickle
import socket
from src.Config import Config
from src.Wallet import Wallet
import threading

# Constants
HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

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
            if msg == "quit": 
                break
            if msg == 'create':
                customer_info = conn.recv(8000)
                customer_info = pickle.loads(customer_info)
                if customer_info:
                    account.create_account(customer_info)

            else:   
                print(f"[User {addr[1]}] {msg}")
                conn.send(b'Message Received')

    conn.close()

def start():
    print('Server starting on', HOST.upper())
    s.listen()

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.active_count() - 1} Connections Active")


start()

