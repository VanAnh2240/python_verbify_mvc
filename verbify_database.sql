USE master;
GO

-- Drop database if exists
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'verbify')
BEGIN
    ALTER DATABASE verbify SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE verbify;
END
GO

-- Create database
CREATE DATABASE verbify;
GO

USE verbify;
GO

-- --------------------------------------------------------
-- Table structure for table genres
-- --------------------------------------------------------

CREATE TABLE GENRES (
    GENRE_ID INT IDENTITY(1,1) PRIMARY KEY,
    GENRES_NAME NVARCHAR(100) NOT NULL UNIQUE
);
GO

-- --------------------------------------------------------
-- Table structure for table book
-- --------------------------------------------------------

CREATE TABLE BOOK (
    BOOK_ID INT IDENTITY(1,1) PRIMARY KEY,
    NAME NVARCHAR(200) NOT NULL,
    ISBN NVARCHAR(100) NULL,
    AUTHOR NVARCHAR(100) NULL,
    LANGUAGE NVARCHAR(50) NULL,
    RELEASE_YEAR INT NULL,
    DESCRIPTION NVARCHAR(1000) NULL,
    PAGE_QUANTITY INT NULL,
    PRICE INT NOT NULL,
    STOCK_QUANTITY INT NOT NULL DEFAULT 0,
    IS_SELLING BIT NULL DEFAULT 1
);
GO

CREATE TABLE BOOK_BELONG (
    BOOK_ID INT NOT NULL,
    GENRE_ID INT NOT NULL,
    PRIMARY KEY (BOOK_ID, GENRE_ID),
    FOREIGN KEY (BOOK_ID) REFERENCES book(BOOK_ID) ON DELETE CASCADE,
    FOREIGN KEY (GENRE_ID) REFERENCES genres(GENRE_ID) ON DELETE CASCADE
);
GO

-- --------------------------------------------------------
-- Table structure for table customer
-- --------------------------------------------------------

CREATE TABLE CUSTOMER (
    CUSTOMER_ID INT IDENTITY(1,1) PRIMARY KEY,
    USERNAME NVARCHAR(50) NOT NULL UNIQUE,
    PASSWORD NVARCHAR(255) NOT NULL,
    PHONE_NUMBER NVARCHAR(15) NULL,
    FIRST_NAME NVARCHAR(50) NULL,
    LAST_NAME NVARCHAR(50) NULL,
    ADDRESS NVARCHAR(300) NULL, 
    IS_ADMIN BIT NOT NULL DEFAULT 0
);
GO

-- --------------------------------------------------------
-- Table structure for table cart
-- --------------------------------------------------------

CREATE TABLE CART (
    CART_ID INT IDENTITY(1,1) PRIMARY KEY,
    CUSTOMER_ID INT NOT NULL,
    TOTAL_QUANTITY INT NOT NULL DEFAULT 0,
    TOTAL_PRICE INT NOT NULL DEFAULT 0,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES customer(CUSTOMER_ID) ON DELETE CASCADE
);
GO

-- --------------------------------------------------------
-- Table structure for table CART_ITEM
-- --------------------------------------------------------

CREATE TABLE CART_ITEM (
    CART_ITEM_ID INT IDENTITY(1,1) PRIMARY KEY,
    CART_ID INT NOT NULL,
    BOOK_ID INT NOT NULL,
    QUANTITY INT NOT NULL DEFAULT 1 CHECK (QUANTITY > 0),
    SUBTOTAL INT NOT NULL,
    FOREIGN KEY (CART_ID) REFERENCES cart(CART_ID) ON DELETE CASCADE,
    FOREIGN KEY (BOOK_ID) REFERENCES book(BOOK_ID),
    UNIQUE (CART_ID, BOOK_ID)
);
GO

-- --------------------------------------------------------
-- Table structure for table ORDERS
-- --------------------------------------------------------

CREATE TABLE ORDERS (
    ORDER_ID INT IDENTITY(1,1) PRIMARY KEY,
    CUSTOMER_ID INT NOT NULL,
    ORDER_DATE DATETIME DEFAULT GETDATE(),
    DELIVERY_ADDRESS NVARCHAR(300) NOT NULL,
    PAYMENT_STATUS NVARCHAR(20) DEFAULT 'UNPAID' CHECK (PAYMENT_STATUS IN ('PAID', 'UNPAID')),
    TOTAL_PRICE INT NOT NULL,
    PAYMENT_TYPE NVARCHAR(50) NULL, -- COD, Bank Transfer, Credit Card, Momo, VNPay, ZaloPay
    FOREIGN KEY (CUSTOMER_ID) REFERENCES customer(CUSTOMER_ID)
);
GO

-- --------------------------------------------------------
-- Table structure for table ORDER_ITEM
-- --------------------------------------------------------

CREATE TABLE ORDER_ITEM (
    ORDER_ITEM_ID INT IDENTITY(1,1) PRIMARY KEY,
    ORDER_ID INT NOT NULL,
    BOOK_ID INT NOT NULL,
    QUANTITY INT NOT NULL CHECK (QUANTITY > 0),
    UNIT_PRICE INT NOT NULL,
    SUBTOTAL INT NOT NULL,
    FOREIGN KEY (ORDER_ID) REFERENCES ORDERS(ORDER_ID) ON DELETE CASCADE,
    FOREIGN KEY (BOOK_ID) REFERENCES book(BOOK_ID)
);
GO

-- --------------------------------------------------------
-- Insert sample data
-- --------------------------------------------------------
INSERT INTO GENRES (GENRES_NAME) VALUES
(N'Tâm lý học'),
(N'Triết học'),
(N'Lịch sử'),
(N'Tiểu thuyết'),
(N'Truyện ngắn'),
(N'Thơ ca'),
(N'Khoa học viễn tưởng'),
(N'Kinh dị'),
(N'Trinh thám'),
(N'Phiêu lưu'),
(N'Thần thoại'),
(N'Kỹ năng sống'),
(N'Kinh doanh'),
(N'Văn học thiếu nhi'),
(N'Sách giáo khoa');
GO

-- Insert sample books

SET IDENTITY_INSERT BOOK ON;
GO

INSERT INTO BOOK (BOOK_ID, NAME, ISBN, AUTHOR, LANGUAGE, RELEASE_YEAR, DESCRIPTION, PAGE_QUANTITY, PRICE, STOCK_QUANTITY, IS_SELLING) VALUES
(1, N'Đắc Nhân Tâm', '978-6043652345', N'Dale Carnegie', N'Tiếng Việt', 1936, N'Cuốn sách kinh điển về nghệ thuật giao tiếp và ứng xử, giúp bạn thành công trong cuộc sống và công việc.', 320, 86000, 150, 1),
(2, N'Nhà Giả Kim', '978-6042068123', N'Paulo Coelho', N'Tiếng Việt', 1988, N'Câu chuyện về hành trình tìm kiếm kho báu và ý nghĩa cuộc đời của chàng chăn cừu Santiago.', 227, 79000, 200, 1),
(3, N'Tuổi Trẻ Đáng Giá Bao Nhiêu', '978-6041234567', N'Rosie Nguyễn', N'Tiếng Việt', 2018, N'Những trải nghiệm và bài học quý giá dành cho tuổi trẻ về cuộc sống, công việc và tình yêu.', 288, 95000, 180, 1),
(4, N'Sapiens: Lược Sử Loài Người', '978-6045678901', N'Yuval Noah Harari', N'Tiếng Việt', 2011, N'Khám phá lịch sử tiến hóa của loài người từ thời tiền sử đến hiện đại.', 543, 189000, 120, 1),
(5, N'Tôi Tài Giỏi, Bạn Cũng Thế', '978-6042345678', N'Adam Khoo', N'Tiếng Việt', 2008, N'Phương pháp học tập hiệu quả giúp học sinh, sinh viên đạt thành tích cao.', 365, 118000, 90, 1),
(6, N'Nghĩ Giàu Làm Giàu', '978-6043456789', N'Napoleon Hill', N'Tiếng Việt', 1937, N'Bí quyết thành công và làm giàu từ những người thành đạt nhất thế giới.', 416, 125000, 100, 1),
(7, N'Đời Ngắn Đừng Ngủ Dài', '978-6041111222', N'Robin Sharma', N'Tiếng Việt', 2016, N'Động lực sống tích cực, khuyến khích bạn sống hết mình với đam mê.', 256, 82000, 140, 1),
(8, N'Hành Trình Về Phương Đông', '978-6042222333', N'Nguyễn Phong', N'Tiếng Việt', 2005, N'Triết lý sống và những bài học nhân sinh từ phương Đông.', 312, 105000, 85, 1),
(9, N'Càng Bình Tĩnh Càng Hạnh Phúc', '978-6043333444', N'Đoàn Minh Phượng', N'Tiếng Việt', 2019, N'Nghệ thuật sống an yên và tìm thấy hạnh phúc trong từng khoảnh khắc.', 248, 89000, 110, 1),
(10, N'Không Diệt Không Sinh Đừng Sợ Hãi', '978-6044444555', N'Thích Nhất Hạnh', N'Tiếng Việt', 2002, N'Triết lý Phật giáo về sự sống, cái chết và ý nghĩa cuộc đời.', 180, 75000, 95, 1),
(11, N'7 Thói Quen Của Người Thành Đạt', '978-6045555666', N'Stephen Covey', N'Tiếng Việt', 1989, N'Bảy nguyên tắc cơ bản giúp bạn thành công trong cuộc sống và sự nghiệp.', 448, 148000, 75, 1),
(12, N'Quẳng Gánh Lo Đi Và Vui Sống', '978-6046666777', N'Dale Carnegie', N'Tiếng Việt', 1948, N'Phương pháp vượt qua lo lắng, căng thẳng và sống cuộc đời hạnh phúc hơn.', 368, 92000, 130, 1),
(13, N'Dám Nghĩ Lớn', '978-6047777888', N'David J. Schwartz', N'Tiếng Việt', 1959, N'Sức mạnh của tư duy tích cực và cách đạt được thành công vượt mong đợi.', 352, 115000, 88, 1),
(14, N'Hai Số Phận', '978-6048888999', N'Jeffrey Archer', N'Tiếng Việt', 1975, N'Câu chuyện về hai người con trai sinh cùng ngày nhưng số phận khác biệt.', 592, 165000, 65, 1),
(15, N'Mắt Biếc', '978-6049999000', N'Nguyễn Nhật Ánh', N'Tiếng Việt', 1990, N'Chuyện tình đẹp và buồn về tuổi thơ và tình yêu đầu.', 272, 98000, 200, 1),
(16, N'Cho Tôi Xin Một Vé Đi Tuổi Thơ', '978-6040001111', N'Nguyễn Nhật Ánh', N'Tiếng Việt', 2014, N'Hồi ức về những kỷ niệm tuổi thơ đẹp đẽ và trong sáng.', 284, 102000, 175, 1),
(17, N'Tôi Thấy Hoa Vàng Trên Cỏ Xanh', '978-6040002222', N'Nguyễn Nhật Ánh', N'Tiếng Việt', 2010, N'Những kỷ niệm tuổi thơ ở miền quê Việt Nam đầy thơ mộng.', 352, 110000, 160, 1),
(18, N'Cà Phê Cùng Tony', '978-6040003333', N'Tony Buổi Sáng', N'Tiếng Việt', 2012, N'Những góc nhìn về cuộc sống, kinh doanh và phát triển bản thân.', 256, 88000, 105, 1),
(19, N'Tâm Lý Học Tội Phạm', '978-6040004444', N'Tuệ Minh', N'Tiếng Việt', 2017, N'Phân tích tâm lý và hành vi của các loại tội phạm.', 398, 135000, 70, 1),
(20, N'Thuật Thao Túng', '978-6040005555', N'Shannon Thomas', N'Tiếng Việt', 2016, N'Nhận diện và thoát khỏi những mối quan hệ độc hại.', 312, 119000, 92, 1),
(21, N'Đừng Bao Giờ Đi Ăn Một Mình', '978-6040006666', N'Keith Ferrazzi', N'Tiếng Việt', 2005, N'Nghệ thuật xây dựng mạng lưới quan hệ thành công.', 384, 128000, 78, 1),
(22, N'Muôn Kiếp Nhân Sinh', '978-6040007777', N'Nguyên Phong', N'Tiếng Việt', 2020, N'Những câu chuyện về luân hồi và nghiệp báo qua các kiếp sống.', 648, 225000, 150, 1),
(23, N'Khéo Ăn Nói Sẽ Có Được Thiên Hạ', '978-6040008888', N'Trác Nhã', N'Tiếng Việt', 2018, N'Nghệ thuật giao tiếp giúp bạn thành công trong mọi hoàn cảnh.', 296, 95000, 115, 1),
(24, N'Nguyên Tắc 80/20', '978-6040009999', N'Richard Koch', N'Tiếng Việt', 1997, N'Bí quyết làm được nhiều việc hơn với ít công sức hơn.', 336, 138000, 68, 1),
(25, N'Chiến Binh Cầu Vồng', '978-6040010000', N'Andrea Hirata', N'Tiếng Việt', 2005, N'Câu chuyện cảm động về tình bạn và ước mơ ở Indonesia.', 288, 98000, 125, 1),
(26, N'Nhà Lãnh Đạo Không Chức Danh', '978-6040011111', N'Robin Sharma', N'Tiếng Việt', 2010, N'Ai cũng có thể trở thành nhà lãnh đạo dù không có chức vụ.', 272, 112000, 85, 1),
(27, N'Trên Đường Băng', '978-6040012222', N'Tony Buổi Sáng', N'Tiếng Việt', 2013, N'Những bài học về khởi nghiệp và phát triển sự nghiệp.', 304, 105000, 95, 1),
(28, N'Rèn Luyện Tư Duy Phản Biện', '978-6040013333', N'Albert Rutherford', N'Tiếng Việt', 2018, N'Kỹ năng tư duy logic và phản biện hiệu quả.', 248, 89000, 102, 1),
(29, N'Bạn Đắt Giá Bao Nhiêu', '978-6040014444', N'Vãn Tình', N'Tiếng Việt', 2019, N'Khám phá giá trị bản thân và cách nâng cao vị thế của mình.', 264, 92000, 118, 1),
(30, N'Sức Mạnh Của Thói Quen', '978-6040015555', N'Charles Duhigg', N'Tiếng Việt', 2012, N'Cách thức hình thành và thay đổi thói quen để thành công.', 416, 145000, 73, 1);

SET IDENTITY_INSERT book OFF;
GO

SET IDENTITY_INSERT CUSTOMER ON;
GO

INSERT INTO CUSTOMER (CUSTOMER_ID, USERNAME, PASSWORD, PHONE_NUMBER, FIRST_NAME, LAST_NAME, ADDRESS, IS_ADMIN) VALUES
(1, 'admin', 'admin', '0901234567', N'Admin', N'', N'123 Nguyễn Huệ, Quận 1, TP.HCM', 1),
(2, 'nguyenvana', 'Pass@123', '0912345678', N'An', N'Nguyễn Văn', N'456 Lê Lợi, Quận 3, TP.HCM', 0),
(3, 'tranthib', 'Pass@456', '0923456789', N'Bình', N'Trần Thị', N'789 Trần Hưng Đạo, Quận 5, TP.HCM', 0),
(4, 'lethic', 'Pass@789', '0934567890', N'Chi', N'Lê Thị', N'321 Võ Văn Kiệt, Quận 1, TP.HCM', 0),
(5, 'phamvand', 'Pass@012', '0945678901', N'Dũng', N'Phạm Văn', N'654 Nguyễn Thị Minh Khai, Quận 3, TP.HCM', 0);

SET IDENTITY_INSERT CUSTOMER OFF;
GO

INSERT INTO BOOK_BELONG (BOOK_ID, GENRE_ID) VALUES
(1, 12), (1, 4),  
(2, 4), (2, 2),   
(3, 12), (3, 1),  
(4, 3), (4, 2),   
(5, 12),          
(6, 13), (6, 12), 
(7, 12), (7, 1),  
(8, 2), (8, 4),   
(9, 1), (9, 12),  
(10, 2),          
(11, 12), (11, 13),
(12, 1), (12, 12), 
(13, 12), (13, 1), 
(14, 4),            
(15, 4), (15, 14),  
(16, 4), (16, 14),  
(17, 4), (17, 14),  
(18, 13), (18, 12), 
(19, 1), (19, 9),   
(20, 1),            
(21, 12), (21, 13), 
(22, 2), (22, 4),   
(23, 12),           
(24, 13), (24, 12), 
(25, 4), (25, 14), 
(26, 13), (26, 12), 
(27, 13), (27, 12), 
(28, 1), (28, 12),  
(29, 12), (29, 1),  
(30, 1), (30, 12);  
GO
