class Cart:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_by_customer(self, customer_id):
        """Lấy tất cả giỏ hàng của khách hàng"""
        sql = """SELECT c.CART_ID, \
                        c.CUSTOMER_ID, \
                        c.TOTAL_QUANTITY, \
                        c.TOTAL_PRICE,
                        (SELECT COUNT(*) FROM CART_ITEM WHERE CART_ID = c.CART_ID) as item_count
                 FROM cart c
                 WHERE c.CUSTOMER_ID = ?"""
        return self.db.query(sql, (customer_id,))

    def get_cart_items(self, cart_id):
        """Lấy các sản phẩm trong giỏ hàng"""
        sql = """SELECT ci.*, b.NAME, b.PRICE
                 FROM CART_ITEM ci
                          JOIN book b ON ci.BOOK_ID = b.BOOK_ID
                 WHERE ci.CART_ID = ?"""
        return self.db.query(sql, (cart_id,))

    def create_cart(self, customer_id):
        """Tạo giỏ hàng mới"""
        sql = "INSERT INTO cart (CUSTOMER_ID, TOTAL_QUANTITY, TOTAL_PRICE) VALUES (?, 0, 0)"
        try:
            self.db.insert(sql, (customer_id,))
            # Lấy cart_id vừa tạo
            sql_get = "SELECT TOP 1 CART_ID FROM cart WHERE CUSTOMER_ID = ? ORDER BY CART_ID DESC"
            result = self.db.query(sql_get, (customer_id,))
            return result[0][0] if result else None
        except Exception as e:
            return None

    def add_to_cart(self, cart_id, book_id, quantity):
        """Thêm sách vào giỏ hàng - nếu đã có thì cập nhật số lượng"""
        sql_check = "SELECT QUANTITY, SUBTOTAL FROM CART_ITEM WHERE CART_ID = ? AND BOOK_ID = ?"
        existing = self.db.query(sql_check, (cart_id, book_id))

        sql_price = "SELECT PRICE FROM book WHERE BOOK_ID = ?"
        price_result = self.db.query(sql_price, (book_id,))
        if not price_result:
            return False
        price = price_result[0][0]

        try:
            if existing:
                new_subtotal = price * quantity
                sql_update = """UPDATE CART_ITEM
                                SET QUANTITY = ?,
                                    SUBTOTAL = ?
                                WHERE CART_ID = ?
                                  AND BOOK_ID = ?"""
                self.db.update(sql_update, (quantity, new_subtotal, cart_id, book_id))
            else:
                subtotal = price * quantity
                sql_insert = """INSERT INTO CART_ITEM (CART_ID, BOOK_ID, QUANTITY, SUBTOTAL)
                                VALUES (?, ?, ?, ?)"""
                self.db.insert(sql_insert, (cart_id, book_id, quantity, subtotal))

            return True
        except Exception as e:
            return False

    def update_cart_total(self, cart_id):
        """Cập nhật tổng giá trị giỏ hàng"""
        sql = """UPDATE cart
                 SET TOTAL_QUANTITY = (SELECT ISNULL(SUM(QUANTITY), 0) FROM CART_ITEM WHERE CART_ID = ?),
                     TOTAL_PRICE    = (SELECT ISNULL(SUM(SUBTOTAL), 0) FROM CART_ITEM WHERE CART_ID = ?)
                 WHERE CART_ID = ?"""
        self.db.update(sql, (cart_id, cart_id, cart_id))

    def get_cart_total(self, cart_id):
        """Lấy tổng giá trị giỏ hàng"""
        sql = "SELECT TOTAL_PRICE FROM cart WHERE CART_ID = ?"
        result = self.db.query(sql, (cart_id,))
        return result[0][0] if result else 0

    def delete_cart(self, cart_id):
        """Xóa giỏ hàng"""
        sql = "DELETE FROM cart WHERE CART_ID = ?"
        try:
            self.db.delete(sql, (cart_id,))
            return True
        except Exception as e:
            return False