from src.Config import Config
from mysql.connector import connect
import pickle

cnx = connect(
    user=Config.DB['user'],
    password=Config.DB['password'],
    host=Config.DB['host'],
    database=Config.DB['database'],
)
csr = cnx.cursor(dictionary=True, buffered=True)

FORMAT = 'utf-8'

# Crypto Wallet Class
class Wallet:
    def __init__(self, conn):
        self.conn = conn
    
    def create_account(self):
        insert_query = "INSERT INTO wallets VALUES ("
        self.conn.send(b'First Name: ')
        first_name = self.conn.recv(8000).decode(FORMAT)
        insert_query += first_name
        self.conn.send(b'Last Name: ')
        last_name = self.conn.recv(8000).decode(FORMAT)
        insert_query += last_name
        
        

