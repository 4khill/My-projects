import mysql.connector
import secrets
import sys

class Datas:
    def __init__(self):
        try:
            # Connect to the database
            self.db = mysql.connector.connect(
                host="localhost",
                user="root", #Enter User Name
                password="", #Enter Password
                database="users" #Enter database 
                )
            self.cursor = self.db.cursor()
        except:
            print('Connection Failed')
            sys.exit(0)
    def search(self,name):
        try:
            self.cursor.execute("SELECT * FROM user WHERE username=%s",(name,))
            if self.cursor.fetchone() is not None:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            sys.exit(0)
    def insert(self,name):
        try:
            password=secrets.randbelow(98889)+1111
            self.cursor.execute("INSERT INTO user (username,password) VALUES (%s,%s)",(name,password))
            self.db.commit()  # Don't forget to commit the transaction
        except Exception as e:
            print(e)
            sys.exit(0)
    def fetch(self,name):
        try:
            self.cursor.execute("SELECT password FROM user WHERE username=%s",(name,))
            password=self.cursor.fetchone()
            return password[0]
        except Exception as e:
            print(e)
            sys.exit(0)
