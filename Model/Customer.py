class Customer:
    def __init__(self, db_connection):
        self.db = db_connection

    def login(self, username, password):
        """Đăng nhập"""
        sql = "SELECT * FROM customer WHERE USERNAME = ? AND PASSWORD = ?"
        result = self.db.query(sql, (username, password))
        return result[0] if result else None

    def register(self, username, password, phone, first_name, last_name, address):
        """Đăng ký tài khoản"""
        sql = """INSERT INTO customer (USERNAME, PASSWORD, PHONE_NUMBER, FIRST_NAME, LAST_NAME, ADDRESS, IS_ADMIN)
                 VALUES (?, ?, ?, ?, ?, ?, 0)"""
        try:
            self.db.insert(sql, (username, password, phone, first_name, last_name, address))
            return True
        except:
            return False

    def get_info(self, customer_id):
        """Lấy thông tin tài khoản"""
        sql = "SELECT * FROM customer WHERE CUSTOMER_ID = ?"
        result = self.db.query(sql, (customer_id,))
        return result[0] if result else None