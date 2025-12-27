import os
from DoAn.MSSQLConnection import MSSQLConnection
from DoAn.Controller.AdminController import AdminController
from DoAn.Controller.CustomerController import CustomerController
from DoAn.Controller.GuestController import GuestController
from DoAn.View.AdminView import AdminView
from DoAn.View.CustomerView import CustomerView
from DoAn.View.GuestView import GuestView


def show_main_menu():
    print("\n" + "-" * 50)
    print("           CỬA HÀNG VERBIFY")
    print("-" * 50)
    print("Chọn vai trò:")
    print("1. Admin")
    print("2. Customer")
    print("3. Guest")
    print("0. Thoát")
    print("-" * 50)
    return input("Nhập lựa chọn: ")


if __name__ == "__main__":
    db = MSSQLConnection()
    db.connect()

    if not db.connection:
        print("Không thể kết nối database. Vui lòng kiểm tra lại cấu hình!!")
        exit()

    admin_controller = AdminController(db)
    customer_controller = CustomerController(db)
    guest_controller = GuestController(db)

    admin_view = AdminView(admin_controller)
    customer_view = CustomerView(customer_controller)
    guest_view = GuestView(guest_controller)

    while True:
        choice = show_main_menu()

        if choice == '1':
            if admin_view.login():
                admin_view.show_menu()

        elif choice == '2':
            if customer_view.login():
                customer_view.show_menu()

        elif choice == '3':
            guest_view.show_menu()

        elif choice == '0':
            print("\n" + "-" * 50)
            print("      CAM ON BAN DA SU DUNG HE THONG!")
            print("-" * 50)
            db.close()
            break

        else:
            print("\nLựa chọn không hợp lệ!")
            input("Nhấn Enter để tiếp tục...")