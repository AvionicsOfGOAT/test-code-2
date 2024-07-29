import datetime
import mysql.connector
import time

db_config = {
    'host': '43.202.228.198', 
    'port': 3306,  
    'database': 'goat',  
    'user': 'root',  
    'password': '' 
}

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**db_config)
            if self.conn.is_connected():
                print('MySQL 데이터베이스에 연결되었습니다.')
        except mysql.connector.Error as e:
            print(f'Error connecting to MySQL: {e}')
        finally:
            if 'conn' in locals() and conn.is_connected():
                self.conn.close()
                print('MySQL 연결이 닫혔습니다.')

        
    def save(self, name, data):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO rocket_data VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (0, name, time.time(), str(data)))
            self.conn.commit()

        except mysql.connector.Error as e:
            print(f'Error inserting data into MySQL: {e}')

        finally:
            if 'cursor' in locals():
                cursor.close()
        
<<<<<<< HEAD
    def get_last(self, name):
        try:
            cursor = self.conn.cursor()
            query = "SELECT * FROM rocket_data WHERE name = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(query, (name))
            result = cursor.fetchone()
            return result
        except mysql.connector.Error as e:
            print(f'Error fetching data from MySQL: {e}')
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
            # if 'conn' in locals() and self.conn.is_connected():
            #     self.conn.close()
=======
    def get_last(self, table_name):
        try:
            cursor = self.conn.cursor(dictionary=True)

            # 테이블에서 가장 최근 데이터 가져오기
            query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1"
            cursor.execute(query)

            # 결과 가져오기
            last_data = cursor.fetchone()

            return last_data

        except mysql.connector.Error as e:
            print(f'Error fetching last data from MySQL: {e}')

        finally:
            if 'cursor' in locals():
                cursor.close()
        return

>>>>>>> d5068142f2ff2aeade019ac9a9e003f627c7c8f2
