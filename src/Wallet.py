from mysql.connector import connect
import random
import string

FORMAT = 'utf-8'

class Wallet:
    def __init__(self, conn, db_conn):
        self.conn = conn
        self.cnx = db_conn
        self.credentials = {}
    
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

        success_msg = f"[ACCOUNT] Account created, your bitcoin wallet address is {wallet_address[1:13]}"
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
    
    def log_in(self, credentials:dict):
        self.credentials = credentials

        email = self.credentials['user']
        password = self.credentials['pass']
        address = self.credentials['wallet']

        query = f"""SELECT FirstName FROM wallets
                    WHERE Email = '{email}' AND EncPassword = '{password}' AND WalletAddress = '{address}'"""
        csr = self.cnx.cursor()
        csr.execute(query)
        name = csr.fetchone()[0]
        log_in_msg = f"[ACCOUNT] Logged in, welcome to your Krypto account {name}!"
        self.conn.send(log_in_msg.encode(FORMAT))
    
    def check_balance(self):
        email = self.credentials['user']
        password = self.credentials['pass']
        address = self.credentials['wallet']


        query = f"SELECT Coins FROM omega.wallets WHERE Email = '{email}' AND EncPassword = '{password}' AND WalletAddress = '{address}'"
        csr = self.cnx.cursor()
        csr.execute(query)

        balance = csr.fetchone()[0]
        
        success_msg = f"[BALANCE] The balance for the wallet address {address} is {balance}"
        self.conn.send(success_msg.encode(FORMAT))

    def deposit(self, coins:float):
        password = self.credentials['pass']
        address = self.credentials['wallet']
        
        update_query = f"UPDATE omega.wallets SET Coins = Coins + {coins} WHERE WalletAddress = '{address}' AND EncPassword = '{password}'"
        csr = self.cnx.cursor()
        csr.execute(update_query)
        self.cnx.commit()
        
        success_msg = f"[DEPOSIT] Your balance has been updated!"
        self.conn.send(success_msg.encode(FORMAT))
        
    def transfer(self, transfer_info):
        email = self.credentials['user']
        address = self.credentials['wallet']
        
        check_balance = f"SELECT Coins from wallets WHERE Email = '{email}' AND WalletAddress = '{address}'"
        csr = self.cnx.cursor()
        csr.execute(check_balance)

        current_coins = float(csr.fetchone()[0])
        transfer_amount = float(transfer_info['amount'])

        new_balance = float('inf')
        if current_coins - transfer_amount < 0:
            new_balance = 0
            transfer_amount = current_coins
        else:
            new_balance = current_coins - transfer_amount

        update_sender = f"""UPDATE wallets SET Coins = {new_balance} 
                            WHERE Email = '{email}' AND WalletAddress = '{address}'"""
        
        update_receiver = f"""UPDATE wallets 
                            SET Coins = Coins + {transfer_amount} 
                            WHERE Email = '{transfer_info['email']}' AND WalletAddress = '{transfer_info['address']}'"""

        csr.execute(update_receiver)
        self.cnx.commit()
        csr.execute(update_sender)
        self.cnx.commit()
        success_message = f"[TRANSFER] {transfer_info['amount']} coins sent to {transfer_info['email']}, your new balance is {new_balance}"
        self.conn.send(success_message.encode(FORMAT))

