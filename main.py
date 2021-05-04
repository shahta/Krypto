from src.Config import Config
from mysql.connector import connect

cnx = connect(
    user=Config.DB['user'],
    password=Config.DB['password'],
    host=Config.DB['host'],
    database=Config.DB['database'],
)
csr = cnx.cursor(dictionary=True, buffered=True)


class Wallet:
    def create_account(self):
        print('created')
