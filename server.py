from mysql.connector import connect
import socket
from src.Config import Config
import threading

# Constants
HOST = "localhost" #socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDRESS = (HOST, PORT)
FORMAT = 'utf-8'

# MySQL connections
cnx = connect(
    user=Config.DB['user'],
    password=Config.DB['password'],
    host=Config.DB['host'],
    database=Config.DB['database'],
)
csr = cnx.cursor(dictionary=True, buffered=True)

# Crypto Wallet Class
class Wallet:
    def __init__(self, conn):
        self.conn = conn
    
    def create_account(self):
        csr.execute('SHOW TABLES')
        for item in csr: 
            item = item['Tables_in_omega']
            self.conn.sendall(bytes(item.encode(FORMAT)))
        
# Server Socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDRESS)

def handle_client(conn, addr):
    print('Connected to', addr)
    account = Wallet(conn)

    while True:
        msg = conn.recv(2048).decode(FORMAT)
        if msg:
            if msg == "quit": break
            if msg == 'create':
                print('hello')
            print(f"[{addr}] {msg}")
            conn.send("Message received".encode(FORMAT))

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

