from Model.Customer import Customer
from Model.Book import Book


class GuestController:
    def __init__(self, db_connection):
        self.db = db_connection
        self.customer_model = Customer(db_connection)
        self.book_model = Book(db_connection)

    def register(self, username, password, phone, first_name, last_name, address):
        """Đăng ký tài khoản mới"""
        return self.customer_model.register(username, password, phone, first_name, last_name, address)

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

