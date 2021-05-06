from mysql.connector import connect
import random
import string

FORMAT = 'utf-8'

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
    
    def check_balance(self, credentials:dict):
        email = credentials['user']
        password = credentials['pass']
        address = credentials['wallet']
        deposit = credentials['deposit']


        query = f"SELECT Coins FROM omega.wallets WHERE Email = '{email}' AND EncPassword = '{password}' AND WalletAddress = '{address}'"
        csr = self.cnx.cursor()
        csr.execute(query)

        balance = csr.fetchone()[0]
        msg_sent = False

        if deposit:
            self.__deposit_coins(address, password, balance, deposit)
            msg_sent = True
        
        if not msg_sent:
            success_msg = f"The balance for the wallet address {address} is {balance}"
            self.conn.send(success_msg.encode(FORMAT))

    def __deposit_coins(self, address, password, current_amount, coins):
        coins = float(coins) + float(current_amount)
        update_query = f"UPDATE omega.wallets SET Coins = '{coins}' WHERE WalletAddress = '{address}' AND EncPassword = '{password}'"
        csr = self.cnx.cursor()
        csr.execute(update_query)
        self.cnx.commit()
        
        success_msg = f"Your new balance for the wallet address {address} is {coins}"
        self.conn.send(success_msg.encode(FORMAT))
        
        
