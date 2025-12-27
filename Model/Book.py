class Book:
    def __init__(self, db_connection):
        self.db = db_connection

    def get_all(self):
        """Lấy tất cả sách"""
        sql = "SELECT * FROM book WHERE IS_SELLING = 1"
        result = self.db.query(sql)
        return result

    def get_by_id(self, book_id):
        """Lấy thông tin sách theo ID"""
        sql = """SELECT b.*, STRING_AGG(g.GENRES_NAME, ', ') as genres
                 FROM book b
                          LEFT JOIN book_belong bb ON b.BOOK_ID = bb.BOOK_ID
                          LEFT JOIN genres g ON bb.GENRE_ID = g.GENRE_ID
                 WHERE b.BOOK_ID = ?
                 GROUP BY b.BOOK_ID, b.NAME, b.ISBN, b.AUTHOR, b.LANGUAGE, b.RELEASE_YEAR,
                          b.DESCRIPTION, b.PAGE_QUANTITY, b.PRICE, b.STOCK_QUANTITY, b.IS_SELLING"""
        result = self.db.query(sql, (book_id,))
        return result[0] if result else None

    def get_by_genre(self, genre_id):
        """Lọc sách theo thể loại"""
        sql = """SELECT b.*
                 FROM book b
                          INNER JOIN book_belong bb ON b.BOOK_ID = bb.BOOK_ID
                 WHERE bb.GENRE_ID = ? \
                   AND b.IS_SELLING = 1"""
        result = self.db.query(sql, (genre_id,))
        return result

    def get_all_genres(self):
        """Lấy danh sách tất cả thể loại"""
        sql = "SELECT * FROM GENRES ORDER BY GENRE_ID"
        return self.db.query(sql)

    def add(self, name, isbn, author, language, release_year, description, page_quantity, price, stock_quantity):
        """Thêm sách mới"""
        sql = """INSERT INTO book (NAME, ISBN, AUTHOR, LANGUAGE, RELEASE_YEAR, DESCRIPTION, PAGE_QUANTITY, PRICE, \
                                   STOCK_QUANTITY, IS_SELLING)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)"""
        try:
            self.db.insert(sql, (name, isbn, author, language, release_year, description, page_quantity, price,
                                 stock_quantity))
            return True
        except Exception as e:
            return False

    def update(self, book_id, name, isbn, author, language, release_year, description, page_quantity, price,
               stock_quantity):
        """Cập nhật sách"""
        sql = """UPDATE book
                 SET NAME           = ?, 
                     ISBN           = ?, 
                     AUTHOR         = ?, 
                     LANGUAGE       = ?, 
                     RELEASE_YEAR   = ?,
                     DESCRIPTION    = ?, 
                     PAGE_QUANTITY  = ?, 
                     PRICE          = ?, 
                     STOCK_QUANTITY = ?
                 WHERE BOOK_ID = ?"""
        try:
            self.db.update(sql, (name, isbn, author, language, release_year, description, page_quantity, price,
                                 stock_quantity, book_id))
            return True
        except Exception as e:
            return False

    def delete(self, book_id):
        """Xóa sách"""
        sql = "DELETE FROM book WHERE BOOK_ID = ?"
        try:
            self.db.delete(sql, (book_id,))
            return True
        except Exception as e:
            return False

    def search(self, keyword):
        """Tìm kiếm sách theo tên hoặc tác giả"""
        sql = "SELECT * FROM book WHERE (NAME LIKE ? OR AUTHOR LIKE ?) AND IS_SELLING = 1"
        result = self.db.query(sql, (f'%{keyword}%', f'%{keyword}%'))
        print(f"\t+Tìm thấy: {len(result)}")
        return result