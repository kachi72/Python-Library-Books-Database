import mysql.connector

def connection():
    db = mysql.connector.connect(host = 'localhost', user = 'kachi', password = 'kachihost72', db = 'librarybooksinventory')
    return db