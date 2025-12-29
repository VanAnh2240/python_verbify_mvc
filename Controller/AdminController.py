from Model.Customer import Customer
from Model.Book import Book
from Model.Order import Order


class AdminController:
    def __init__(self, db_connection):
        self.db = db_connection
        self.customer_model = Customer(db_connection)
        self.book_model = Book(db_connection)
        self.order_model = Order(db_connection)
        self.current_user = None

    def login(self, username, password):
        """Đăng nhập"""
        user = self.customer_model.login(username, password)
        if user and user[7] == 1:
            self.current_user = user
            return True
        return False

    def get_account_info(self):
        """Xem thông tin tài khoản"""
        if self.current_user:
            return self.customer_model.get_info(self.current_user[0])
        return None

    def get_book_detail(self, book_id):
        """Xem chi tiết sách"""
        return self.book_model.get_by_id(book_id)


    def get_all_books(self):
        """Lấy danh sách tất cả sách"""
        return self.book_model.get_all()

    def add_book(self, name, isbn, author, language, release_year, description, page_quantity, price, stock_quantity):
        """Thêm sách mới"""
        return self.book_model.add(name, isbn, author, language, release_year, description, page_quantity, price,
                                   stock_quantity)

    def update_book(self, book_id, name, isbn, author, language, release_year,
                    description, page_quantity, price, stock_quantity):
        """Cập nhật thông tin sách"""
        return self.book_model.update(
            book_id, name, isbn, author, language,
            release_year, description,
            page_quantity, price, stock_quantity
        )

    def delete_book(self, book_id):
        """Xóa sách"""
        return self.book_model.delete(book_id)

    def get_report(self):
        """Xem báo cáo"""
        report = {
            'total_sales': self.order_model.get_total_sales(),
            'total_revenue': self.order_model.get_total_revenue(),
            'least_sold_book': self.order_model.get_least_sold_book(),
            'most_sold_book': self.order_model.get_most_sold_book(),
            'top_customer': self.order_model.get_top_customer()
        }
        return report