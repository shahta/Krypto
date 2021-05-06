from mysql.connector import connect
import random
from src.Config import Config
import string

# cnx = connect(
#     user=Config.DB['user'],
#     password=Config.DB['password'],
#     host=Config.DB['host'],
#     database=Config.DB['database'],
# )
# csr = cnx.cursor(dictionary=True, buffered=True)

FORMAT = 'utf-8'

# Crypto Wallet Class
class Wallet:
    def __init__(self, conn, db_conn):
        self.conn = conn
        self.cnx = db_conn
    
    def create_account(self, customer_info:dict):
        insert_query = "INSERT INTO omega.wallets VALUES ("
        for value in customer_info.values():
            value = "'" + str(value) + "', " 
            insert_query += value
        
        wallet_address = self.__unique_wallet_address()
        wallet_address = "'" + str(wallet_address) + "'" + ")"
        insert_query += wallet_address
        
        csr = self.cnx.cursor()
        csr.execute(insert_query)
        self.cnx.commit()

        success_msg = f"Account created, your bitcoin wallet address is {wallet_address[1:13]}"
        self.conn.send(success_msg.encode(FORMAT))
    
    def __unique_wallet_address(self):
        dic = {
            1: string.ascii_letters,
            2: string.digits,
            3: ['!', '@', '#','%','$','!', '^', '*', '(', ')', '-', '_', '+', '=', '~',]
        }
        address = ''
        for _ in range(12):
            char = random.randint(1, 3)
            char = random.choice(dic[char])
            address += char
        
        return address

        
        
