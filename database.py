import datetime
# import mysql.connector

db_config = {
    'host': 'localhost',  
    'database': 'mydatabase', 
    'user': 'root',  
    'password': 'password', 
}

class Database:
    # def __init__(self):
    #     self.connect()

    # def connect(self):
    #     try:
    #         # MySQL 서버에 연결
    #         self.conn = mysql.connector.connect(**db_config)

    #         if self.conn.is_connected():
    #             print('MySQL 데이터베이스에 연결되었습니다.')

    #     except mysql.connector.Error as e:
    #         print(f'Error connecting to MySQL: {e}')

    #     finally:
    #         if 'conn' in locals() and conn.is_connected():
    #             self.conn.close()
    #             print('MySQL 연결이 닫혔습니다.')
    pass
        
    def save(self, table_name, data):
        # try:
        #     cursor = self.conn.cursor()

        #     data = {
        #         'name': 'John',
        #         'age': 30,
        #         'city': 'New York'
        #     }

        #     query = "INSERT INTO "+table_name+" (name, age, city) VALUES (%s, %s, %s)"
        #     cursor.execute(query, (data['name'], data['age'], data['city']))

        #     self.conn.commit()

        #     print(f'{cursor.rowcount} 개의 레코드가 삽입되었습니다.')

        # except mysql.connector.Error as e:
        #     print(f'Error inserting data into MySQL: {e}')

        # finally:
        #     if 'cursor' in locals():
        #         cursor.close()
        pass
        