class CustomerView:
    def __init__(self, controller):
        self.controller = controller

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        if self.controller.login(username, password):
            print("Đăng nhập thành công!")
            return True
        else:
            print("Đăng nhập thất bại, vui lòng thử lại!")
            return False

    def show_menu(self):
        while True:
            print("\n===== CUSTOMER MENU =====")
            print("1. Xem thông tin tài khoản")
            print("2. Xem tất cả sách")
            print("3. Tìm kiếm sách theo tên hoặc tác giả")
            print("4. Lọc sách theo thể loại")
            print("5. Xem chi tiết sách")
            print("6. Xem tất cả giỏ hàng")
            print("7. Xem chi tiết giỏ hàng")
            print("8. Tạo giỏ hàng mới")
            print("9. Thêm sách vào giỏ hàng")
            print("11. Tính tổng giỏ hàng")
            print("12. Xóa giỏ hàng")
            print("13. Xem tất cả đơn hàng")
            print("14. Xem chi tiết đơn hàng")
            print("15. Tạo đơn hàng")
            print("16. Xem đơn hàng chưa thanh toán")
            print("17. Thanh toán đơn hàng")
            print("0. Đăng xuất")

            choice = input("-----Chọn chức năng: ")

            if choice == '1':
                print(self.view_account_info())

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

            elif choice == '6':
                result = self.view_all_carts()
                if isinstance(result, str):
                    print(result)
                else:
                    for cart in result:
                        print(
                            f"Giỏ hàng ID: {cart[0]} | Số items: {cart[4]} | SL tổng: {cart[2]} | Tổng tiền: {cart[3]:,}đ")

            elif choice == '7':
                result = self.view_cart_items()
                if isinstance(result, str):
                    print(result)
                else:
                    for item in result:
                        print(f"Sách: {item[5]} | SL: {item[3]} | Đơn giá: {item[6]:,}đ | Tổng: {item[4]:,}đ")

            elif choice == '8':
                print(self.create_cart())

            elif choice == '9':
                print(self.add_to_cart())

            elif choice == '11':
                print(self.get_cart_total())

            elif choice == '12':
                print(self.delete_cart())

            elif choice == '13':
                result = self.view_all_orders()
                if isinstance(result, str):
                    print(result)
                else:
                    for order in result:
                        print(f"Đơn ID: {order[0]} | Ngày: {order[2]} | Tổng: {order[5]:,}đ | TT: {order[4]}")

            elif choice == '14':
                result = self.view_order_items()
                if isinstance(result, str):
                    print(result)
                else:
                    for item in result:
                        print(f"Sách: {item[6]} | SL: {item[3]} | Đơn giá: {item[4]:,}đ | Tổng: {item[5]:,}đ")

            elif choice == '15':
                print(self.create_order())

            elif choice == '16':
                result = self.view_unpaid_orders()
                if isinstance(result, str):
                    print(result)
                else:
                    for order in result:
                        print(
                            f"Đơn ID: {order[0]} | Ngày: {order[2]} | Địa chỉ: {order[3]} | Tổng: {order[5]:,}đ | PT: {order[6]}")

            elif choice == '17':
                print(self.pay_order())

            elif choice == '0':
                return "Đã đăng xuất"
            else:
                print("Lựa chọn không hợp lệ")

    def view_account_info(self):
        info = self.controller.get_account_info()
        if not info:
            return "Không có thông tin tài khoản"
        return f"ID: {info[0]} | Username: {info[1]} | Họ tên: {info[4]} {info[5]} | SĐT: {info[3]} | Địa chỉ: {info[6]}"

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

    def view_all_carts(self):
        carts = self.controller.get_all_carts()
        if not carts:
            return "Không có giỏ hàng"
        return carts

    def view_cart_items(self):
        try:
            cart_id = int(input("Nhập ID giỏ hàng: "))
            items = self.controller.get_cart_items(cart_id)
            if not items:
                return "Giỏ hàng trống"

            print("\n-----CHI TIẾT GIỎ HÀNG")
            for item in items:
                print(f"Sách: {item[5]} | SL: {item[3]} | Đơn giá: {item[6]:,}đ | Tổng: {item[4]:,}đ")

            carts = self.controller.get_all_carts()
            for cart in carts:
                if cart[0] == cart_id:
                    print("=" * 70)
                    print(f"TỔNG GIÁ TRỊ GIỎ HÀNG: {cart[3]:,}đ")
                    break
            return ""
        except:
            return "ID không hợp lệ"

    def create_cart(self):
        cart_id = self.controller.create_cart()
        if cart_id:
            return f"Tạo giỏ hàng thành công! Mã giỏ hàng: {cart_id}"
        return "Không thể tạo giỏ hàng"

    def add_to_cart(self):
        cart_id = int(input("Nhập ID giỏ hàng: "))
        book_id = int(input("Nhập ID sách: "))
        quantity = int(input("Nhập số lượng: "))
        result = self.controller.add_to_cart(cart_id, book_id, quantity)
        if result:
            return "Đã thêm sách vào giỏ hàng!"
        return "Thêm thất bại!"

    def get_cart_total(self):
        try:
            cart_id = int(input("Nhập ID giỏ hàng: "))

            # Hiển thị chi tiết giỏ hàng trước
            items = self.controller.get_cart_items(cart_id)
            if not items:
                return "Giỏ hàng trống"

            print("\n=== CHI TIẾT GIỎ HÀNG ===")
            for item in items:
                print(f"Sách: {item[5]} | SL: {item[3]} | Đơn giá: {item[6]:,}đ | Tổng: {item[4]:,}đ")

            print("----")
            total = self.controller.get_cart_total(cart_id)
            return f"TỔNG GIÁ TRỊ GIỎ HÀNG: {total:,}đ"
        except:
            return "ID không hợp lệ"

    def delete_cart(self):
        try:
            cart_id = int(input("Nhập ID giỏ hàng: "))
            if self.controller.delete_cart(cart_id):
                return "Đã xóa giỏ hàng"
            return "Xóa thất bại"
        except:
            return "ID không hợp lệ"

    def view_all_orders(self):
        orders = self.controller.get_all_orders()
        if not orders:
            return "Không có đơn hàng"
        return orders

    def view_order_items(self):
        try:
            order_id = int(input("Nhập ID đơn hàng: "))
            items = self.controller.get_order_items(order_id)
            if not items:
                return "Đơn hàng trống"
            return items
        except:
            return "ID không hợp lệ"

    def create_order(self):
        try:
            cart_id = int(input("Nhập ID giỏ hàng: "))
            address = input("Địa chỉ giao hàng: ")
            payment = input("Hình thức thanh toán: ")
            order_id = self.controller.create_order(cart_id, address, payment)
            if order_id:
                return f"Tạo đơn hàng thành công! Mã đơn hàng: {order_id}"
            return "Tạo đơn hàng thất bại"
        except:
            return "Dữ liệu không hợp lệ"

    def view_unpaid_orders(self):
        orders = self.controller.get_unpaid_orders()
        if not orders:
            return "Không có đơn chưa thanh toán"
        return orders

    def pay_order(self):
        try:
            order_id = int(input("Nhập ID đơn hàng: "))
            if self.controller.pay_order(order_id):
                return "Thanh toán thành công"
            return "Thanh toán thất bại"
        except:
            return "ID không hợp lệ"