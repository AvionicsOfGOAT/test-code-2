import datetime
import mysql.connector

db_config = {
    'host': '43.202.228.198', 
    'port': 3306,  
    'database': 'goat',  
    'user': 'root',  
    'password': 'tkrhk0123!!' 
}

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.save("test","1")
            if self.conn.is_connected():
                print('MySQL connected.')
        except mysql.connector.Error as e:
            print(f'Error connecting to MySQL: {e}')
        
    def save(self, name, data):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO rocket_data VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (0, name, 1, str(data)))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f'{name} Error inserting data into MySQL: {e}')
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_last(self, name):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM rocket_data WHERE name = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as e:
            print(f'Error fetching data from MySQL: {e}')
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
