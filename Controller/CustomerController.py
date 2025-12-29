from Model.Customer import Customer
from Model.Book import Book
from Model.Cart import Cart
from Model.Order import Order


class CustomerController:
    def __init__(self, db_connection):
        self.db = db_connection
        self.customer_model = Customer(db_connection)
        self.book_model = Book(db_connection)
        self.cart_model = Cart(db_connection)
        self.order_model = Order(db_connection)
        self.user = None

    def login(self, username, password):
        """Đăng nhập"""
        user = self.customer_model.login(username, password)
        if user and user[7] == 0:
            self.user = user
            return True
        return False

    def get_account_info(self):
        """Xem thông tin tài khoản"""
        if self.user:
            return self.customer_model.get_info(self.user[0])
        return None

    def search_books(self, keyword):
        """Tìm kiếm sách"""
        return self.book_model.search(keyword)

    def get_all_books(self):
        """Lấy danh sách tất cả sách"""
        return self.book_model.get_all()

    def get_book_detail(self, book_id):
        """Xem chi tiết sách"""
        return self.book_model.get_by_id(book_id)

    def get_all_genres(self):
        """Lấy danh sách thể loại"""
        return self.book_model.get_all_genres()

    def get_books_by_genre(self, genre_id):
        """Lọc sách theo thể loại"""
        return self.book_model.get_by_genre(genre_id)

    def get_all_carts(self):
        """Lấy tất cả giỏ hàng của khách hàng"""
        if self.user:
            return self.cart_model.get_all_by_customer(self.user[0])
        return []

    def get_cart_items(self, cart_id):
        """Lấy chi tiết trong giỏ hàng"""
        return self.cart_model.get_cart_items(cart_id)

    def create_cart(self):
        """Tạo giỏ hàng mới"""
        if self.user:
            return self.cart_model.create_cart(self.user[0])
        return None

    def add_to_cart(self, cart_id, book_id, quantity):
        """Thêm sách vào giỏ hàng"""
        return self.cart_model.add_to_cart(cart_id, book_id, quantity)

    def get_cart_total(self, cart_id):
        """Tính tổng giá trị giỏ hàng"""
        # Cập nhật tổng trước khi lấy
        self.cart_model.update_cart_total(cart_id)
        return self.cart_model.get_cart_total(cart_id)

    def delete_cart(self, cart_id):
        """Xóa giỏ hàng"""
        return self.cart_model.delete_cart(cart_id)

    def get_all_orders(self):
        """Lấy tất cả đơn hàng của khách hàng"""
        if self.user:
            return self.order_model.get_all_by_customer(self.user[0])
        return []

    def get_order_items(self, order_id):
        """Lấy chi tiết đơn hàng"""
        return self.order_model.get_order_items(order_id)

    def create_order(self, cart_id, delivery_address, payment_type):
        """Tạo đơn hàng từ giỏ hàng"""
        if self.user:
            order_id = self.order_model.create_order_from_cart(self.user[0], cart_id, delivery_address, payment_type)
            return order_id
        return None

    def get_unpaid_orders(self):
        """Lấy các đơn hàng chưa thanh toán"""
        if self.user:
            return self.order_model.get_unpaid_orders(self.user[0])
        return []

    def pay_order(self, order_id):
        """Thanh toán đơn hàng"""
        return self.order_model.pay_order(order_id)