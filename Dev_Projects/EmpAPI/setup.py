from json import dumps
import os

mysql_host = input("Enter the MySQL host name:\n")
mysql_user = input("Enter the MySQL user name:\n")
mysql_pass = input("Enter the MySQL user password:\n")
mysql_db = input("Enter the MySQL database name:\n")
mysql_table = input("Enter the MySQL table name:\n")

with open('connections.json', 'w') as f:
    conn = {
        "mysql_host": mysql_host,
        "mysql_user": mysql_user,
        "mysql_pass": mysql_pass,
        "mysql_db": mysql_db,
        "mysql_table": mysql_table
    }
    f.write(dumps(conn))

os.system('pip install mysql-connector-python')