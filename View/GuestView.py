class GuestView:
    def __init__(self, controller):
        self.controller = controller

    def show_menu(self):
        while True:
            print("\n===== GUEST MENU =====")
            print("1. Đăng ký tài khoản")
            print("2. Xem tất cả sách")
            print("3. Tìm kiếm sách theo tên hoặc tác giả")
            print("4. Lọc sách theo thể loại")
            print("5. Xem chi tiết sách")
            print("0. Quay lại")

            choice = input("Chon chuc nang: ")


            if choice == '1':
                print(self.register())

            elif choice == '2':
                result = self.view_all_books()
                if isinstance(result, str):
                    print(result)
                else:
                    for book in result:
                        print(
                            f"ID: {book[0]} | Tên: {book[1]} | Tác giả: {book[3]} | Giá: {book[8]:,}đ | Kho: {book[9]}")

            elif choice == '3':
                result = self.search_books()
                if isinstance(result, str):
                    print(result)
                else:
                    for book in result:
                        print(
                            f"ID: {book[0]} | Tên: {book[1]} | Tác giả: {book[3]} | Giá: {book[8]:,}đ | Kho: {book[9]}")

            elif choice == '4':
                result = self.filter_books_by_genre()
                if isinstance(result, str):
                    print(result)
                else:
                    for book in result:
                        print(
                            f"ID: {book[0]} | Tên: {book[1]} | Tác giả: {book[3]} | Giá: {book[8]:,}đ | Kho: {book[9]}")

            elif choice == '5':
                print(self.view_book_detail())

            elif choice == '0':
                return "Đã đăng xuất"

            else:
                print("Lựa chọn không hợp lệ")

    def register(self):
        username = input("Username: ")
        password = input("Password: ")
        phone = input("Số điện thoại: ")
        first_name = input("Tên: ")
        last_name = input("Họ: ")
        address = input("Địa chỉ: ")

        if self.controller.register(
                username, password, phone,
                first_name, last_name, address
        ):
            return "Đăng ký tài khoản thành công"

        return "Đăng ký thất bại"

    def view_all_books(self):
        books = self.controller.get_all_books()
        if not books:
            return "Không có sách"
        return books

    def search_books(self):
        keyword = input("Nhập từ khóa: ")
        books = self.controller.search_books(keyword)
        if not books:
            return "Không tìm thấy sách"
        return books

    def filter_books_by_genre(self):
        genres = self.controller.get_all_genres()
        if not genres:
            return "Không có thể loại"
        print("\n=== DANH SÁCH THỂ LOẠI ===")
        for genre in genres:
            print(f"{genre[0]}. {genre[1]}")
        try:
            genre_id = int(input("Chọn ID thể loại: "))
            books = self.controller.get_books_by_genre(genre_id)
            if not books:
                return "Không có sách thuộc thể loại này"
            return books
        except:
            return "ID không hợp lệ"

    def view_book_detail(self):
        try:
            book_id = int(input("Nhập ID sách: "))
            book = self.controller.get_book_detail(book_id)
            if not book:
                return "Không tìm thấy sách"
            return f"ID: {book[0]} | Tên: {book[1]} | ISBN: {book[2]} | Tác giả: {book[3]} | Ngôn ngữ: {book[4]} | Năm XB: {book[5]} | Mô tả: {book[6]} | Số trang: {book[7]} | Giá: {book[8]:,}đ | Kho: {book[9]}"
        except:
            return "ID không hợp lệ"

