class AdminView:
    def __init__(self, controller):
        self.controller = controller

    def login(self):
        username = input("Username: ")
        password = input("Password: ")

        result = self.controller.login(username, password)
        if result:
            print("Đăng nhập thành công!")
            return True
        else:
            print("Đăng nhập thất bại! Sai username hoặc password!")
            return False

    def show_menu(self):
        while True:
            print("\n========== ADMIN MENU ==========")
            print("1. Xem thông tin tài khỏan")
            print("2. Xem danh sách sách")
            print("3. Thêm sách")
            print("4. Cập nhật sách")
            print("5. Xóa sách")
            print("6. Xem báo cáo")
            print("0. Đăng xuất")
            print("=" * 33)

            choice = input("Chọn chức năng: ")

            if choice == '1':
                print(self.view_account_info())

            elif choice == '2':
                self.view_all_books()

            elif choice == '3':
                print(self.add_book())

            elif choice == '4':
                print(self.update_book())

            elif choice == '5':
                print(self.delete_book())

            elif choice == '6':
                print(self.view_report())

            elif choice == '0':
                return "Đã đăng xuất!"

            else:
                print("Lựa chọn không hợp lệ")

    def view_account_info(self):
        info = self.controller.get_account_info()
        if not info:
            return "Không có thông tin tài khoản"
        return [(info[0]),info[1],info[4] + " " + info[5],info[3], info[6]]

    def view_all_books(self):
        books = self.controller.get_all_books()
        if not books:
            print("Không có sách")
            return
        for b in books:
            print([b[0], b[1], b[3],b[8], b[9] ])

    def add_book(self):
        try:
            name = input("Tên sách: ")
            isbn = input("ISBN: ")
            author = input("Tác gi: ")
            language = input("Ngôn ngữ: ")
            release_year = int(input("Năm xuất bản: "))
            description = input("Mô tả: ")
            page_quantity = int(input("Sô trang: "))
            price = float(input("Gía: "))
            stock_quantity = int(input("Sô lượng tôn kho: "))

            result = self.controller.add_book(
                name, isbn, author, language,
                release_year, description,
                page_quantity, price, stock_quantity
            )
            if result:
                return "Thêm sách thành công!"
            return "Thêm sách thất bại!"
        except ValueError:
            return "Dữ liệu nhập không hợp lệ!"

    def update_book(self):
        try:
            book_id = int(input("Nhập ID sách cần cập nhật (0 để hủy): "))
            if book_id == 0:
                return "Đã hủy cập nhật!"

            book = self.controller.get_book_detail(book_id)
            if not book:
                return "Không tìm thấy sách!"

            print(f"\nThông tin hiện tại: {book[1]} - Giá: {book[8]:,}đ")
            print("(Để giữ nguyên giá trị, nhấn Enter)\n")

            name = input(f"Tên sách [{book[1]}]: ") or book[1]
            isbn = input(f"ISBN [{book[2]}]: ") or book[2]
            author = input(f"Tác giả [{book[3]}]: ") or book[3]
            language = input(f"Ngôn ngữ [{book[4]}]: ") or book[4]

            year_input = input(f"Năm xuất bản [{book[5]}]: ")
            release_year = int(year_input) if year_input else book[5]

            description = input(f"Mô tả [{book[6]}]: ") or book[6]

            page_input = input(f"Số trang [{book[7]}]: ")
            page_quantity = int(page_input) if page_input else book[7]

            price_input = input(f"Giá [{book[8]}]: ")
            price = float(price_input) if price_input else book[8]

            stock_input = input(f"Số lượng tồn kho [{book[9]}]: ")
            stock_quantity = int(stock_input) if stock_input else book[9]

            if self.controller.update_book(
                    book_id, name, isbn, author,
                    language, release_year,
                    description, page_quantity,
                    price, stock_quantity
            ):
                return "Cập nhật sách thành công!"
            else:
                return "Cập nhật sách thất bại!"
        except ValueError:
            return "Dữ liệu nhập không hợp lệ!"

    def delete_book(self):
        books = self.controller.get_all_books()
        if not books:
            return "Không có sách để xóa!"
        book_id = int(input("Nhập ID sách muốn xóa (0 để hủy): "))
        if book_id == 0:
            return ("Đã hủy xóa!")

        if self.controller.delete_book(book_id):
            return "Xóa sách thành công!"
        return "Xóa sách thất bại!"

    def view_report(self):
        report = self.controller.get_report()

        least_book = report['least_sold_book']
        most_book = report['most_sold_book']
        top_cust = report['top_customer']

        return (
            f"\nTổng số đơn hàng: {report['total_sales']}\n"
            f"Tổng doanh thu: {report['total_revenue']:,.0f} VNĐ\n"
            f"Sách bán ít nhất: {least_book[0]} ({least_book[1]} cuốn)\n"
            f"Sách bán nhiều nhất: {most_book[0]} ({most_book[1]} cuốn)\n"
            f"Khách hàng mua nhiều nhất: {top_cust[0]} - {top_cust[1]} {top_cust[2]} ({top_cust[3]:,.0f} VNĐ)"
        )
