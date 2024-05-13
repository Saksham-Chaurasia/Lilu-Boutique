import mysql.connector
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'LiluBoutique21@',
    'database': 'boutique'
}

def db():
    conn = mysql.connector.connect(**db_config)
    return conn
