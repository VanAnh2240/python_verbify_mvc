class Order:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all_by_customer(self, customer_id):
        """Lấy tất cả đơn hàng của khách hàng"""
        sql = "SELECT * FROM ORDERS WHERE CUSTOMER_ID = ? ORDER BY ORDER_DATE DESC"
        return self.db.query(sql, (customer_id,))

    def get_order_items(self, order_id):
        """Lấy chi tiết đơn hàng"""
        sql = """SELECT oi.*, b.NAME
                 FROM ORDER_ITEM oi
                          JOIN book b ON oi.BOOK_ID = b.BOOK_ID
                 WHERE oi.ORDER_ID = ?"""
        return self.db.query(sql, (order_id,))

    def create_order_from_cart(self, customer_id, cart_id, delivery_address, payment_type):
        """Tạo đơn hàng từ giỏ hàng"""
        sql_cart = "SELECT TOTAL_PRICE FROM cart WHERE CART_ID = ?"
        cart_result = self.db.query(sql_cart, (cart_id,))
        if not cart_result:
            return None
        total_price = cart_result[0][0]

        sql_order = """INSERT INTO ORDERS (CUSTOMER_ID, DELIVERY_ADDRESS, PAYMENT_STATUS, TOTAL_PRICE, PAYMENT_TYPE)
                       VALUES (?, ?, 'UNPAID', ?, ?)"""
        try:
            self.db.insert(sql_order, (customer_id, delivery_address, total_price, payment_type))

            sql_get_order = "SELECT TOP 1 ORDER_ID FROM ORDERS WHERE CUSTOMER_ID = ? ORDER BY ORDER_ID DESC"
            order_result = self.db.query(sql_get_order, (customer_id,))
            if not order_result:
                return None
            order_id = order_result[0][0]

            sql_items = """SELECT BOOK_ID, QUANTITY, SUBTOTAL
                           FROM CART_ITEM
                           WHERE CART_ID = ?"""
            cart_items = self.db.query(sql_items, (cart_id,))

            for item in cart_items:
                book_id, quantity, subtotal = item[0], item[1], item[2]
                sql_price = "SELECT PRICE FROM book WHERE BOOK_ID = ?"
                price_result = self.db.query(sql_price, (book_id,))
                unit_price = price_result[0][0] if price_result else 0

                sql_insert_item = """INSERT INTO ORDER_ITEM (ORDER_ID, BOOK_ID, QUANTITY, UNIT_PRICE, SUBTOTAL)
                                     VALUES (?, ?, ?, ?, ?)"""
                self.db.insert(sql_insert_item, (order_id, book_id, quantity, unit_price, subtotal))

            sql_delete_cart = "DELETE FROM cart WHERE CART_ID = ?"
            self.db.delete(sql_delete_cart, (cart_id,))

            return order_id
        except Exception as e:
            return None

    def delete_order(self, order_id):
        """Xóa đơn hàng"""
        sql = "DELETE FROM ORDERS WHERE ORDER_ID = ?"
        try:
            self.db.delete(sql, (order_id,))
            return True
        except Exception as e:
            return False

    def pay_order(self, order_id):
        """Thanh toán đơn hàng"""
        sql = "UPDATE ORDERS SET PAYMENT_STATUS = 'PAID' WHERE ORDER_ID = ?"
        try:
            self.db.update(sql, (order_id,))
            return True
        except Exception as e:
            return False

    def get_unpaid_orders(self, customer_id):
        """Lấy các đơn hàng chưa thanh toán"""
        sql = "SELECT * FROM ORDERS WHERE CUSTOMER_ID = ? AND PAYMENT_STATUS = 'UNPAID'"
        return self.db.query(sql, (customer_id,))

    def get_total_sales(self):
        """Tính tổng doanh số (số lượng sản phẩm đã bán)"""
        sql = """SELECT ISNULL(SUM(oi.QUANTITY), 0) as total_sales
                 FROM ORDER_ITEM oi
                          JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
                 WHERE o.PAYMENT_STATUS = 'PAID'"""
        result = self.db.query(sql)
        return result[0][0] if result else 0

    def get_total_revenue(self):
        """Tính tổng doanh thu"""
        sql = """SELECT ISNULL(SUM(TOTAL_PRICE), 0) as total_revenue
                 FROM ORDERS
                 WHERE PAYMENT_STATUS = 'PAID'"""
        result = self.db.query(sql)
        return result[0][0] if result else 0

    def get_least_sold_book(self):
        """Sách bán ít nhất"""
        sql = """SELECT TOP 1 b.NAME, ISNULL(SUM(oi.QUANTITY), 0) as total_sold
                 FROM book b
                          LEFT JOIN ORDER_ITEM oi ON b.BOOK_ID = oi.BOOK_ID
                          LEFT JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID AND o.PAYMENT_STATUS = 'PAID'
                 GROUP BY b.BOOK_ID, b.NAME
                 ORDER BY total_sold ASC"""
        result = self.db.query(sql)
        return result[0] if result else (None, 0)

    def get_most_sold_book(self):
        """Sách bán nhiều nhất"""
        sql = """SELECT TOP 1 b.NAME, SUM(oi.QUANTITY) as total_sold
                 FROM ORDER_ITEM oi
                          JOIN book b ON oi.BOOK_ID = b.BOOK_ID
                          JOIN ORDERS o ON oi.ORDER_ID = o.ORDER_ID
                 WHERE o.PAYMENT_STATUS = 'PAID'
                 GROUP BY b.BOOK_ID, b.NAME
                 ORDER BY total_sold DESC"""
        result = self.db.query(sql)
        return result[0] if result else (None, 0)

    def get_top_customer(self):
        """Khách hàng chi tiêu nhiều nhất"""
        sql = """SELECT TOP 1 c.USERNAME, c.FIRST_NAME, c.LAST_NAME, SUM(o.TOTAL_PRICE) as total_spent
                 FROM customer c
                          JOIN ORDERS o ON c.CUSTOMER_ID = o.CUSTOMER_ID
                 WHERE o.PAYMENT_STATUS = 'PAID'
                 GROUP BY c.CUSTOMER_ID, c.USERNAME, c.FIRST_NAME, c.LAST_NAME
                 ORDER BY total_spent DESC"""
        result = self.db.query(sql)
        return result[0] if result else (None, None, None, 0)