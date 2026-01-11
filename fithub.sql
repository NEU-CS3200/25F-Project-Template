
DROP DATABASE IF EXISTS fithub;
CREATE DATABASE fithub;
USE fithub;



CREATE TABLE User (
    UserID      INT AUTO_INCREMENT PRIMARY KEY,
    Name        VARCHAR(100) NOT NULL,
    Email       VARCHAR(255) NOT NULL UNIQUE,
    Phone       VARCHAR(20) NOT NULL,
    Address     VARCHAR(255) NOT NULL,
    DOB         DATE NOT NULL,
    Gender      VARCHAR(20) NOT NULL,
    IsActive    BOOLEAN NOT NULL
);


CREATE TABLE Announcements (
    AnnouncementID INT AUTO_INCREMENT PRIMARY KEY,
    UserID         INT NOT NULL,
    Message        TEXT NOT NULL,
    AnnouncedAt    DATETIME NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);


CREATE TABLE Items (
    ItemID       INT AUTO_INCREMENT PRIMARY KEY,
    Title        VARCHAR(255) NOT NULL,
    Category     VARCHAR(100) NOT NULL,
    Description  TEXT NOT NULL,
    Size         VARCHAR(10) NOT NULL,
    `Condition`  VARCHAR(100) NOT NULL,
    Availability VARCHAR(20) NOT NULL,
    OwnerID      INT NOT NULL,
    ListedAt     DATETIME NOT NULL,
    FOREIGN KEY (OwnerID) REFERENCES User(UserID)
);


CREATE TABLE Reports (
    ReportID    INT AUTO_INCREMENT PRIMARY KEY,
    note        TEXT NOT NULL,
    severity    INT NOT NULL,
    resolved    BOOLEAN NOT NULL,
    ReporterID  INT NOT NULL,
    ItemID      INT NOT NULL,
    FOREIGN KEY (ReporterID) REFERENCES User(UserID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);

CREATE TABLE Images (
    ImageID        INT AUTO_INCREMENT PRIMARY KEY,
    ItemID         INT NOT NULL,
    ImageURL       TEXT NOT NULL,
    ImageOrderNum  INT NOT NULL,
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID)
);


CREATE TABLE Tags (
    TagID     INT AUTO_INCREMENT PRIMARY KEY,
    Title     VARCHAR(100) NOT NULL
);


CREATE TABLE ItemTags (
    ItemID INT NOT NULL,
    TagID  INT NOT NULL,
    PRIMARY KEY (ItemID, TagID),
    FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
    FOREIGN KEY (TagID) REFERENCES Tags(TagID)
);


CREATE TABLE Orders (
    OrderID     INT AUTO_INCREMENT PRIMARY KEY,
    SenderID    INT NOT NULL,
    ReceiverID  INT NOT NULL,
    ItemID      INT NOT NULL,
    CreatedAt   DATETIME NOT NULL,
    FOREIGN KEY (SenderID)   REFERENCES User(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES User(UserID),
    FOREIGN KEY (ItemID)     REFERENCES Items(ItemID)
);


CREATE TABLE Shippings (
    ShippingID   INT AUTO_INCREMENT PRIMARY KEY,
    OrderID      INT NOT NULL,
    Carrier      VARCHAR(100) NOT NULL,
    TrackingNum  VARCHAR(255) NOT NULL,
    DateShipped  DATE NOT NULL,
    DateArrived  DATE NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);


CREATE TABLE Feedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID    INT NOT NULL,
    Rating     INT NOT NULL,
    Comment    TEXT NOT NULL,
    CreatedAt  DATETIME NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    CHECK (Rating BETWEEN 1 AND 5)
);


-- Users
INSERT INTO User(Name, Email, Phone, Address, DOB, Gender, IsActive)
VALUES('Lena Park',    'lena@example.com',    '5551112222','12 Willow Lane, Brooklyn, NY', '1998-06-15', 'Female', 1),
('Marcus Lee',   'marcus@example.com',  '5552223333','89 Cedar St, Seattle, WA',    '1995-03-02', 'Male',   1),
('Jade Alvarez', 'jade@example.com',    '5553334444','301 Sunset Blvd, Los Angeles, CA', '2000-11-20', 'Female', 1);

-- Announcements
INSERT INTO Announcements(UserID, Message, AnnouncedAt)
VALUES (1, 'Welcome to FitHub! List your pre-loved fits and swap with the community.', '2025-02-01 09:00:00'),
 (2, 'Pro tip: Use aesthetic tags like Y2K, Coquette, or Streetwear so people can find your vibe.', '2025-02-02 15:30:00'),
(3, 'Weekend challenge: Swap at least one item and leave feedback for your partner.', '2025-02-03 18:45:00');


INSERT INTO Items(Title, Category, Description, Size, `Condition`,Availability, OwnerID, ListedAt)
VALUES('Brandy Melville Baby Tee', 't-shirt','y2k white baby tee with tiny blue graphic, super cropped and super cute', 'S', 'Very good', 'swap', 1, '2025-02-04 11:00:00'),
 ('Levi''s 501 Straight Jeans', 'jeans', 'vintage light wash levi''s 501 straight leg, perfect everyday denim','M', 'Good', 'trade', 2, '2025-02-04 13:20:00'),
('Zara Oversized Hoodie', 'hoodie','charcoal gray oversized hoodie, cozy streetwear essential, fleece inside','L', 'Excellent', 'swap', 3, '2025-02-05 10:15:00'),
('American Eagle Maxi Skirt', 'skirt','boho floral maxi skirt, soft fabric, elastic waist, very flowy', 'M', 'Good', 'claimed', 1, '2025-02-05 16:40:00');


INSERT INTO Reports(note, severity, resolved, ReporterID, ItemID)
VALUES
('Small stain near hem that wasn''t mentioned, still wearable though.',1, 1, 2, 1),
('Jeans arrived slightly more faded than pictured but still cute.',2, 0, 3, 2),
('Hoodie had a loose thread on cuff, not a big deal.',1, 1, 1, 3);


INSERT INTO Images
(ItemID, ImageURL, ImageOrderNum)
VALUES
 (1, 'https://example.com/images/brandy_baby_tee_front.jpg', 1),
(2, 'https://example.com/images/levis_501_full.jpg',        1),
 (3, 'https://example.com/images/zara_hoodie_flatlay.jpg',   1),
(4, 'https://example.com/images/ae_maxi_skirt_hanger.jpg',  1);


INSERT INTO Tags
(Title)
VALUES
('Y2K'),
 ('Vintage'),
('Clean Girl'),
('Streetwear'),
('Coquette'),
('Basic');


INSERT INTO ItemTags
    (ItemID, TagID)
VALUES
    -- Brandy tee → Y2K, Coquette
    (1, 1),
    (1, 5),

    -- Levi's jeans → Vintage, Streetwear
    (2, 2),
    (2, 4),

    -- Zara hoodie → Streetwear, Basic
    (3, 4),
    (3, 6),

    -- AE maxi skirt → Y2K, Clean Girl
    (4, 1),
    (4, 3);

-- Orders (swaps/trades between users)
INSERT INTO Orders(SenderID, ReceiverID, ItemID, CreatedAt)
VALUES
(2, 1, 2, '2025-02-06 12:00:00'),
(1, 3, 1, '2025-02-06 14:30:00'),
(3, 2, 3, '2025-02-07 09:45:00');

-- Shippings (for each order)
INSERT INTO Shippings (OrderID, Carrier, TrackingNum, DateShipped, DateArrived)
VALUES
(1, 'USPS', 'USPS9400111899223000000001', '2025-02-06', '2025-02-08'),
(2, 'UPS',  '1ZSWAP000000000001',        '2025-02-06', '2025-02-09'),
(3, 'FedEx','FEDEXTRADE123456789',       '2025-02-07', '2025-02-09');

-- Feedback (post-swap reviews)
INSERT INTO Feedback
    (OrderID, Rating, Comment, CreatedAt)
VALUES
(1, 5, 'Jeans fit perfectly, exactly the vintage vibe I wanted. Would swap again!', '2025-02-09 18:00:00'),
(2, 4, 'Baby tee is so cute and very Y2K. Slightly more cropped than expected but still love it.', '2025-02-10 11:20:00'),
 (3, 5, 'Hoodie is insanely soft, looks just like photos. Great communication too.',
     '2025-02-10 20:45:00');
