import pyodbc

class MSSQLConnection:
    def __init__(self, drive='ODBC Driver 18 for SQL Server',
                 server=r'VANANH\MSSQLSERVER02',
                 database='verbify',
                 username='',
                 password=''):
        self.drive = drive
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={self.drive};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password};'
                "Trusted_Connection=yes;"
                "Encrypt=no;"
            )
            print("Kết nối database thành công!")
        except Exception as e:
            print(f" Lỗi kết nối database: {e}")

    def disconnect(self):
        """Đóng kết nối"""
        if self.connection:
            self.connection.close()
            print("Đã đóng kết nối database!")

    def query(self, sql, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()

    def update(self, sql, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.connection.commit()

    def insert(self, sql, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.connection.commit()

    def delete(self, sql, params=None):
        cursor = self.connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.disconnect()