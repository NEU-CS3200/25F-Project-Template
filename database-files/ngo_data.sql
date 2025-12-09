-- Creating tables and adding all the mock data to them

Drop database if exists ngo_data;
CREATE DATABASE IF NOT EXISTS ngo_data;
USE ngo_data;

-- check not nulls for primary keys
-- Creating tables and adding all the mock data to them

Drop database if exists ngo_data;
CREATE DATABASE IF NOT EXISTS ngo_data;
USE ngo_data;

-- check not nulls for primary keys

CREATE TABLE IF NOT EXISTS Customer(
    customerID INT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL, -- think about not null or unique ????????
    lastName VARCHAR(50) NOT NULL,
    dietaryPref VARCHAR(500) NOT NULL,
    nutritionGoals VARCHAR(500) NOT NULL,
    email VARCHAR(50) -- how to handle multivalue
);

INSERT INTO Customer (CustomerID, firstName, lastName, email, dietaryPref, nutritionGoals)
VALUES
(1, 'Willdon', 'Cardillo', 'wcardillo0@posterous.com', 'gluten_free', 'muscle_gain'),
(2, 'Lyon', 'Levee', 'llevee1@auda.org.au', 'vegetarian', 'protein'),
(3, 'Garrott', 'Fairfull', 'gfairfull2@ifeng.com', 'pescatarian', 'heart_health'),
(4, 'Carolin', 'Jessel', 'cjessel3@hhs.gov', 'gluten_free', 'weight_loss'),
(5, 'Daniel', 'Thurgood', 'rthurgood4@meetup.com', 'vegetarian', 'muscle_gain'),
(6, 'Vivyanne', 'Boyington', 'vboyington5@ycombinator.com', 'pescatarian', 'muscle_gain'),
(7, 'Norma', 'Ferber', 'nferber6@netvibes.com', 'pescatarian', 'weight_loss'),
(8, 'Etta', 'Downton', 'edownton7@ucla.edu', 'pescatarian', 'heart_health'),
(9, 'Gayla', 'McKeney', 'gmckeney8@nps.gov', 'gluten_free', 'weight_loss'),
(10, 'Florina', 'Crangle', 'fcrangle9@weibo.com', 'vegetarian', 'heart_health'),
(11, 'Hasheem', 'Eteen', 'heteena@columbia.edu', 'pescatarian', 'muscle_gain'),
(12, 'Serene', 'Tankard', 'stankardb@cdbaby.com', 'none', 'protein'),
(13, 'Karlik', 'McGarrahan', 'kmcgarrahanc@rambler.ru', 'vegetarian', 'weight_loss'),
(14, 'Aharon', 'Hardaker', 'ahardakerd@joomla.org', 'gluten_free', 'weight_loss'),
(15, 'Car', 'Morrill', 'cmorrille@oakley.com', 'vegetarian', 'muscle_gain'),
(16, 'Friedrich', 'Donati', 'fdonatif@omniture.com', 'pescatarian', 'weight_loss'),
(17, 'Vaughan', 'Lakeman', 'vlakemang@geocities.com', 'pescatarian', 'muscle_gain'),
(18, 'Elsworth', 'Coggen', 'ecoggenh@cocolog-nifty.com', 'vegan', 'muscle_gain'),
(19, 'Berenice', 'Wasteney', 'bwasteneyi@nyu.edu', 'vegetarian', 'muscle_gain'),
(20, 'Rianon', 'Aloway', 'ralowayj@telegraph.co.uk', 'none', 'muscle_gain'),
(21, 'Mattie', 'Doyle', 'mdoylek@nymag.com', 'vegan', 'heart_health'),
(22, 'Keeley', 'Matthews', 'kmatthewsl@ovh.net', 'pescatarian', 'muscle_gain'),
(23, 'Nina', 'Larroway', 'nlarrowaym@github.io', 'gluten_free', 'heart_health'),
(24, 'Kristen', 'Stait', 'kstaitn@europa.eu', 'none', 'muscle_gain'),
(25, 'Klarrisa', 'Finnick', 'kfinnicko@bandcamp.com', 'vegan', 'protein'),
(26, 'Minni', 'MacNalley', 'mmacnalleyp@surveymonkey.com', 'gluten_free', 'heart_health'),
(27, 'Matt', 'China', 'mchinaq@tuttocitta.it', 'vegan', 'weight_loss'),
(28, 'Lavinia', 'Marte', 'lmarter@toplist.cz', 'none', 'heart_health'),
(29, 'Marguerite', 'Wolfenden', 'mwolfendens@surveymonkey.com', 'vegetarian', 'weight_loss'),
(30, 'Gerrilee', 'Saltrese', 'gsaltreset@ifeng.com', 'vegetarian', 'protein'),
(31, 'Liva', 'Wadworth', 'lwadworthu@booking.com', 'gluten_free', 'weight_loss'),
(32, 'Nikolos', 'Manvelle', 'nmanvellev@mashable.com', 'vegetarian', 'heart_health'),
(33, 'Cinda', 'Thickens', 'cthickensw@loc.gov', 'vegetarian', 'muscle_gain'),
(34, 'Elysee', 'Painten', 'epaintenx@1688.com', 'vegetarian', 'weight_loss'),
(35, 'Skippie', 'Kibby', 'skibbyy@arstechnica.com', 'vegan', 'muscle_gain'),
(36, 'Robinett', 'Chadbourn', 'rchadbournz@cdc.gov', 'vegan', 'muscle_gain'),
(37, 'Tamma', 'Desbrow', 'tdesbrow10@latimes.com', 'vegetarian', 'weight_loss'),
(38, 'Terrence', 'Hugonnet', 'thugonnet11@unicef.org', 'pescatarian', 'weight_loss'),
(39, 'Fanchon', 'Heigho', 'fheigho12@diigo.com', 'pescatarian', 'muscle_gain'),
(40, 'Roseanna', 'Keyse', 'rkeyse13@newsvine.com', 'vegan', 'heart_health'),
(41, 'Aviva', 'Watkiss', 'awatkiss14@nationalgeographic.com', 'vegan', 'weight_loss'),
(42, 'Theresa', 'Ventris', 'tventris15@unicef.org', 'vegan', 'muscle_gain'),
(43, 'Dyann', 'Pacheco', 'dpacheco16@netvibes.com', 'gluten_free', 'protein'),
(44, 'Emelita', 'Breitler', 'ebreitler17@123-reg.co.uk', 'none', 'heart_health'),
(45, 'Halli', 'Adamczyk', 'hadamczyk18@blog.com', 'none', 'weight_loss'),
(46, 'Jedidiah', 'Dinesen', 'jdinesen19@google.com.hk', 'gluten_free', 'heart_health'),
(47, 'Garwin', 'Szubert', 'gszubert1a@exblog.jp', 'vegan', 'protein'),
(48, 'Wenonah', 'Trevorrow', 'wtrevorrow1b@alexa.com', 'none', 'protein'),
(49, 'Jayson', 'Vern', 'jvern1c@google.cn', 'gluten_free', 'heart_health'),
(50, 'Martie', 'Osinin', 'mosinin1d@dedecms.com', 'pescatarian', 'heart_health');

CREATE TABLE IF NOT EXISTS CustomerMessage(
    messageID INT PRIMARY KEY,
    content TEXT NOT NULL,
    `timestamp` DATE NOT NULL,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) references Customer(customerID) ON UPDATE CASCADE
);

INSERT INTO CustomerMessage(messageID, content, `timestamp`, customerID)
VALUES
(1, 'Quisque ut erat.', '2025-08-30', 34),
(2, 'Nam dui. Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.', '2025-09-09', 18),
(3, 'Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus. In sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti.', '2025-09-21', 16),
(4, 'Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis.', '2024-12-24', 13),
(5, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem. Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien.', '2025-05-05', 27),
(6, 'Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend.', '2025-07-26', 10),
(7, 'In sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti. In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh.', '2025-10-24', 12),
(8, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis.', '2025-03-21', 27),
(9, 'Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst.', '2025-08-07', 48),
(10, 'Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.', '2025-04-14', 18),
(11, 'Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue.', '2025-06-21', 50),
(12, 'Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', '2025-06-16', 40),
(13, 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', '2025-09-14', 23),
(14, 'Mauris lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam.', '2025-03-05', 32),
(15, 'Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus.', '2025-05-17', 11),
(16, 'Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero.', '2025-11-22', 49),
(17, 'Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius.', '2025-05-27', 7),
(18, 'Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla.', '2025-09-02', 11),
(19, 'Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue.', '2025-02-19', 14),
(20, 'Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti. In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt.', '2025-09-01', 19),
(21, 'Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum.', '2025-07-05', 7),
(22, 'Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros.', '2025-07-04', 17),
(23, 'Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim.', '2025-10-17', 2),
(24, 'Aenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi.', '2025-06-07', 44),
(25, 'Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.', '2025-01-07', 34),
(26, 'Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia.', '2025-01-14', 22),
(27, 'Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc.', '2025-11-16', 42),
(28, 'Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl.', '2025-11-22', 25),
(29, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo.', '2025-08-01', 36),
(30, 'Integer a nibh.', '2025-09-10', 18);

-- Driver
CREATE TABLE IF NOT EXISTS Driver(
    DriverID INT PRIMARY KEY,
    name varchar(100) NOT NULL
);

INSERT INTO Driver (DriverID, Name)
VALUES
(1, 'Cassey Raylton'),
(2, 'Wally Truitt'),
(3, 'Ronnica Binfield'),
(4, 'Blanch Shattock'),
(5, 'Griffin Petyakov'),
(6, 'Bob Johnson');

CREATE TABLE IF NOT EXISTS Orders(
    orderID INT PRIMARY KEY,
    `status` ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
    orderDate DATE NOT NULL,
    scheduledTime DATE NOT NULL,
    deliveryAddress VARCHAR(100) NOT NULL,
    quantityOrdered INT NOT NULL,
    produceID INT NOT NULL,
    ingredientID INT NOT NULL,
    DriverID INT,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO Orders (OrderID, `status`, orderDate, scheduledTime, deliveryAddress, quantityOrdered, produceID, ingredientID, DriverID, customerID)
VALUES
(1, 'cancelled', '2025-01-08', '2025-03-27', '61 Main St', 8, 8, 15, 3, 1),
(2, 'cancelled', '2025-01-19', '2025-03-21', '30 Oak Ave', 1, 13, 6, 1, 2),
(3, 'cancelled', '2025-04-05', '2025-09-05', '68 Pine Rd', 4, 4, 24, 3, 45),
(4, 'confirmed', '2024-12-21', '2025-11-15', '93 Elm St', 8, 8, 25, 3, 31),
(5, 'out_for_delivery', '2025-01-04', '2025-01-13', '50 Maple Dr', 2, 12, 2, 4, 42),
(6, 'pending', '2025-11-11', '2025-02-27', '92 Cedar Ln', 4, 1, 30, 2, 8),
(7, 'delivered', '2025-07-14', '2025-04-28', '62 Birch Way', 4, 8, 19, null, 41),
(8, 'preparing', '2025-09-21', '2025-06-23', '11 Walnut Ct', 5, 5, 10, null, 24),
(9, 'preparing', '2025-07-12', '2025-07-07', '71 Spruce St', 1, 7, 18, 1, 29),
(10, 'out_for_delivery', '2025-04-12', '2025-05-06', '3 Ash Blvd', 10, 6, 19, 1, 9),
(11, 'cancelled', '2025-10-04', '2025-04-22', '24 Cherry Ln', 8, 1, 13, 3, 9),
(12, 'out_for_delivery', '2025-03-05', '2025-10-26', '33 Poplar Ave', 10, 6, 7, 2, 7),
(13, 'out_for_delivery', '2025-09-18', '2025-02-16', '27 Willow Rd', 1, 7, 10, 3, 31),
(14, 'cancelled', '2025-01-02', '2025-03-13', '30 Hickory Dr', 10, 1, 30, 1, 6),
(15, 'cancelled', '2024-12-18', '2025-11-18', '48 Sycamore St', 4, 1, 10, 2, 14),
(16, 'delivered', '2025-11-03', '2025-01-03', '89 Magnolia Way', 10, 2, 12, 4, 33),
(17, 'preparing', '2025-01-03', '2025-05-30', '92 Dogwood Ct', 5, 1, 22, 1, 49),
(18, 'out_for_delivery', '2025-04-17', '2025-03-27', '18 Redwood Ln', 8, 10, 21, 5, 10),
(19, 'confirmed', '2025-08-21', '2025-05-18', '45 Sequoia Ave', 7, 3, 15, 1, 32),
(20, 'delivered', '2025-04-21', '2025-10-07', '4 Cypress Rd', 10, 6, 13, 3, 43),
(21, 'out_for_delivery', '2025-04-25', '2025-08-13', '36 Palm Dr', 7, 6, 22, 1, 13),
(22, 'confirmed', '2025-08-24', '2025-09-28', '17 Juniper St', 9, 11, 18, 2, 15),
(23, 'pending', '2025-04-04', '2024-12-09', '83 Olive Way', 4, 6, 19, 2, 28),
(24, 'delivered', '2025-05-24', '2025-02-05', '12 Laurel Ct', 6, 14, 14, 4, 5),
(25, 'out_for_delivery', '2025-01-07', '2025-03-14', '72 Hazel Ln', 4, 9, 7, 3, 19);

CREATE TABLE IF NOT EXISTS DeliveryIssue(
    IssueID INT PRIMARY KEY,
    orderID INT NOT NULL,
    `timestamp` DATE NOT NULL,
    `description` TEXT,
    FOREIGN KEY (orderID) REFERENCES Orders (orderID) ON DELETE CASCADE
);

INSERT INTO DeliveryIssue (IssueID, OrderID, `timestamp`, `description`)
VALUES
(1, 7, '2024-12-15', 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.'),
(2, 21, '2025-07-20', 'Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien.'),
(3, 19, '2025-05-08', 'Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor.'),
(4, 19, '2025-08-12', 'In quis justo.'),
(5, 20, '2025-09-20', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.'),
(6, 20, '2025-09-06', 'Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit.'),
(7, 18, '2025-09-24', 'Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus.'),
(8, 5, '2025-10-04', 'In congue. Etiam justo. Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius.'),
(9, 20, '2025-10-01', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam.'),
(10, 9, '2025-01-27', 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.');


-- Delivery Message
CREATE TABLE IF NOT EXISTS DeliveryMessage(
    messageID INT PRIMARY KEY,
    `timestamp` DATE NOT NULL,
    content TEXT NOT NULL,
    DriverID INT NOT NULL,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE
);

INSERT INTO DeliveryMessage (messageID, content, `timestamp`, DriverID)
VALUES
(1, 'Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui.', '2025-02-10', 4),
(2, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo.', '2025-03-13', 4),
(3, 'Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus.', '2025-01-28', 3),
(4, 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl.', '2024-12-28', 4),
(5, 'Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo.', '2025-04-19', 1),
(6, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem. Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti.', '2024-12-24', 4),
(7, 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', '2025-01-20', 5),
(8, 'Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit.', '2025-04-26', 1),
(9, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', '2025-05-21', 1),
(10, 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus.', '2025-02-25', 2),
(11, 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue.', '2025-08-14', 4),
(12, 'Quisque porta volutpat erat.', '2025-11-17', 2),
(13, 'Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo. Etiam pretium iaculis justo.', '2025-01-27', 4),
(14, 'Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros.', '2025-06-29', 4),
(15, 'Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim.', '2025-01-06', 3),
(16, 'Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est.', '2025-01-24', 1),
(17, 'Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam. Nam tristique tortor eu pede.', '2025-05-29', 4),
(18, 'Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante.', '2025-01-19', 1),
(19, 'Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui.', '2025-08-28', 3),
(20, 'Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.', '2025-02-28', 5),
(21, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.', '2025-03-05', 2),
(22, 'Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo.', '2025-08-02', 5),
(23, 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.', '2024-12-16', 1),
(24, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.', '2025-01-15', 3),
(25, 'Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit.', '2025-10-22', 5),
(26, 'Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum.', '2025-11-23', 3),
(27, 'Nulla facilisi.', '2025-05-28', 4),
(28, 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', '2025-09-02', 4),
(29, 'Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.', '2025-06-02', 1),
(30, 'In congue.', '2025-01-22', 5);

-- DriverAvailibilty
CREATE TABLE IF NOT EXISTS DriverAvailability(
    availibilityID INT PRIMARY KEY,
    availStartTime TIME NOT NULL, -- change the diagram, came from timeWindow
    availEndTime TIME NOT NULL, -- change the diagram, came from timeWindow
    `date` DATE NOT NULL,
    isAvailable BOOLEAN,
    DriverID INT NOT NULL,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE
);

INSERT INTO DriverAvailability (availibilityID, availStartTime, availEndTime, `date`, isAvailable, DriverID)
VALUES
(1, '10:32:00', '09:27:00', '2025-11-22', true, 1),
(2, '08:19:00', '10:56:00', '2025-05-05', false, 5),
(3, '02:21:00', '18:33:00', '2025-02-05', true, 3),
(4, '11:15:00', '11:35:00', '2025-04-06', false, 5),
(5, '17:04:00', '02:13:00', '2025-08-16', true, 1),
(6, '00:42:00', '04:48:00', '2025-05-06', true, 1),
(7, '16:55:00', '05:24:00', '2025-05-15', false, 3),
(8, '21:41:00', '01:19:00', '2025-05-25', false, 4),
(9, '00:43:00', '22:42:00', '2025-08-07', true, 1),
(10, '18:23:00', '10:11:00', '2025-10-12', true, 5),
(11, '02:31:00', '18:23:00', '2025-06-13', false, 1),
(12, '23:54:00', '16:01:00', '2025-04-10', true, 5),
(13, '17:46:00', '16:35:00', '2025-03-11', true, 4),
(14, '15:49:00', '15:57:00', '2025-08-21', true, 2),
(15, '14:17:00', '19:26:00', '2025-11-19', true, 4),
(16, '11:52:00', '09:54:00', '2025-08-04', true, 1),
(17, '10:34:00', '01:20:00', '2025-11-10', false, 2),
(18, '23:47:00', '09:26:00', '2025-10-09', false, 2),
(19, '10:20:00', '01:53:00', '2025-06-28', false, 1),
(20, '13:12:00', '20:47:00', '2025-09-20', false, 2),
(21, '05:30:00', '00:26:00', '2025-11-04', true, 3),
(22, '07:46:00', '05:07:00', '2025-07-29', false, 2),
(23, '20:27:00', '17:51:00', '2025-02-08', false, 2),
(24, '21:48:00', '21:01:00', '2025-03-18', true, 1),
(25, '18:12:00', '16:17:00', '2025-11-03', true, 1),
(26, '04:43:00', '11:35:00', '2025-11-11', true, 2),
(27, '20:11:00', '08:39:00', '2025-07-13', false, 2),
(28, '03:21:00', '02:03:00', '2024-12-15', true, 1),
(29, '22:28:00', '11:26:00', '2025-10-25', true, 3),
(30, '07:55:00', '01:32:00', '2025-05-13', false, 1),
(31, '01:04:00', '06:55:00', '2025-03-05', false, 3),
(32, '13:12:00', '05:19:00', '2025-08-15', false, 5),
(33, '16:36:00', '04:52:00', '2024-12-10', true, 1),
(34, '18:46:00', '09:01:00', '2025-08-10', false, 3),
(35, '11:04:00', '15:26:00', '2025-07-06', false, 3),
(36, '03:25:00', '05:15:00', '2024-12-06', false, 5),
(37, '02:54:00', '01:17:00', '2025-04-12', true, 2),
(38, '01:29:00', '01:23:00', '2025-03-09', false, 2),
(39, '18:03:00', '10:54:00', '2025-11-18', false, 1),
(40, '22:08:00', '07:03:00', '2025-04-02', true, 3);

-- meal plan
CREATE TABLE IF NOT EXISTS mealPlan(
    mealPlanId INT PRIMARY KEY,
    startDate DATE NOT NULL,
    endDate DATE,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE
);

INSERT INTO mealPlan (mealPlanID, startDate, endDate, customerID)
VALUES
(1, '2025-01-04', '2025-03-27', 28),
(2, '2025-10-29', '2025-11-13', 4),
(3, '2025-02-11', '2025-04-10', 5),
(4, '2025-02-08', '2025-06-08', 4),
(5, '2025-06-26', '2024-12-06', 38),
(6, '2025-10-28', null, 39),
(7, '2025-05-09', null, 21),
(8, '2024-12-06', '2025-02-02', 43),
(9, '2025-08-03', '2025-09-21', 13),
(10, '2025-10-29', '2025-05-04', 26);

CREATE TABLE IF NOT EXISTS Recipe(
    recipeID INT PRIMARY KEY,
    name varchar(100) NOT NULL,
    description TEXT NOT NULL,
    nutritionInfo TEXT NOT NULL,
    popularityScore SMALLINT NOT NULL,
    isActive BOOLEAN NOT NULL,
    suitibleFor TEXT NOT NULL,
    cuisineType VARCHAR(250)
);

INSERT INTO Recipe (RecipeID, Name, description, nutritionInfo, popularityScore, isActive, suitibleFor, cuisineType)
VALUES
(1, 'consequat nulla nisl nunc', 'Sed ante. Vivamus tortor. Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.', 'Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue.', 99, false, 'vegan', 'mediterranean'),
(2, 'congue etiam justo etiam', 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis. Fusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo. Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna.', 96, true, 'vegan', 'mediterranean'),
(3, 'donec semper sapien', 'Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus.', 9, true, 'low_carb', 'asian'),
(4, 'dictumst aliquam augue', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.', 'Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 95, true, 'gluten_free', 'mexican'),
(5, 'tortor risus dapibus', 'Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est.', 'Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 70, true, 'gluten_free', 'asian'),
(6, 'iaculis congue vivamus', 'Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh.', 'Curabitur in libero ut massa volutpat convallis.', 96, false, 'low_carb', 'asian'),
(7, 'odio donec vitae', 'Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet.', 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 10, false, 'vegetarian', 'mexican'),
(8, 'pharetra magna ac consequat', 'Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.', 'Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc.', 30, true, 'vegetarian', 'mediterranean'),
(9, 'tincidunt in leo maecenas', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.', 'Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue.', 47, false, 'vegan', 'mediterranean'),
(10, 'venenatis lacinia aenean sit', 'Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', 54, false, 'high_protein', 'mexican'),
(11, 'in sapien iaculis', 'Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 'Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum.', 4, false, 'high_protein', 'asian'),
(12, 'vitae nisl aenean', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius.', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo.', 97, false, 'high_protein', 'mediterranean'),
(13, 'elit sodales scelerisque mauris', 'Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', 'Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', 71, false, 'high_protein', 'mexican'),
(14, 'praesent blandit nam', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui.', 'Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 33, true, 'vegan', 'mexican'),
(15, 'sapien placerat ante nulla', 'Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem.', 69, true, 'low_carb', 'mediterranean');


CREATE TABLE IF NOT EXISTS Produce(
    produceID INT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    expectedHarvestDate DATE NOT NULL,
    quantityAvailable INT NOT NULL,
    UNIT VARCHAR(100)
);

INSERT INTO Produce (produceID, name, expectedHarvestDate, quantityAvailable, UNIT)
VALUES
(1, 'non velit nec nisi', '2025-03-04', 352, 'kg'),
(2, 'nisl duis bibendum', '2025-08-01', 3, 'bunches'),
(3, 'aliquet pulvinar sed', '2025-09-01', 256, 'pieces'),
(4, 'proin interdum mauris', '2025-11-23', 213, 'pieces'),
(5, 'cum sociis natoque', '2025-03-22', 340, 'pieces'),
(6, 'purus sit amet', '2025-01-02', 446, 'pieces'),
(7, 'habitasse platea dictumst', '2024-12-28', 289, 'pieces'),
(8, 'sem fusce consequat', '2025-06-03', 142, 'lbs'),
(9, 'molestie lorem quisque ut', '2024-12-10', 214, 'kg'),
(10, 'quam pede lobortis', '2024-12-16', 133, 'lbs'),
(11, 'erat quisque erat', '2025-09-21', 123, 'lbs'),
(12, 'natoque penatibus et magnis', '2025-05-17', 329, 'lbs'),
(13, 'ligula vehicula consequat morbi', '2025-04-04', 355, 'bunches'),
(14, 'sed justo pellentesque', '2024-12-20', 388, 'pieces'),
(15, 'nam ultrices libero', '2025-11-30', 241, 'kg');


-- CREATE TABLE IF NOT EXISTS OrderProduce( / can delete ?
CREATE TABLE IF NOT EXISTS OrderProduce (
    orderID INT NOT NULL,
    produceID INT NOT NULL,
    PRIMARY KEY (orderID, produceID),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO OrderProduce (orderID, produceID)
VALUES
(15, 4),
(10, 8),
(11, 12),
(18, 3),
(20, 12),
(16, 1),
(20, 13),
(4, 1),
(15, 3),
(4, 8),
(2, 11),
(6, 10),
(13, 1),
(5, 6),
(17, 1),
(12, 5),
(25, 1),
(10, 7),
(19, 5),
(10, 11),
(1, 10),
(5, 14),
(5, 13),
(1, 6),
(6, 3),
(20, 14),
(19, 2),
(24, 15),
(20, 10),
(22, 1),
(2, 3),
(12, 1),
(11, 9),
(24, 8),
(3, 7);

CREATE TABLE IF NOT EXISTS mealPlanRecipe(
    mealPlanID INT NOT NULL,
    recipeID INT NOT NULL,
    day VARCHAR(20) NOT NULL,
    mealType VARCHAR(20),
    PRIMARY KEY (mealPlanID, recipeID, day),
    FOREIGN KEY (mealPlanID) REFERENCES mealPlan(mealPlanID) ON DELETE CASCADE,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO mealPlanRecipe (mealPlanID, recipeID, day, mealType)
VALUES
(1, 1, 'Monday', 'Breakfast'),
(2, 2, 'Friday', 'Lunch'),
(3, 3, 'Monday', 'Lunch'),
(4, 4, 'Friday', 'Breakfast'),
(5, 5, 'Tuesday', 'Lunch'),
(6, 6, 'Wednesday', 'Breakfast'),
(7, 7, 'Friday', 'Lunch'),
(8, 8, 'Thursday', 'Dinner'),
(9, 9, 'Tuesday', 'Dinner'),
(10, 10, 'Thursday', 'Breakfast'),
(1, 11, 'Thursday', 'Lunch'),
(2, 12, 'Sunday', 'Dinner'),
(3, 13, 'Wednesday', 'Dinner'),
(4, 14, 'Sunday', 'Dinner'),
(5, 15, 'Sunday', 'Breakfast'),
(6, 1, 'Thursday', 'Dinner'),
(7, 2, 'Thursday', 'Breakfast'),
(8, 3, 'Wednesday', 'Dinner'),
(9, 4, 'Monday', 'Lunch'),
(10, 5, 'Sunday', 'Lunch');

-- Recipe Produce
CREATE TABLE IF NOT EXISTS RecipeProduce(
    recipeID INT NOT NULL,
    produceID INT NOT NULL,
    PRIMARY KEY(recipeID, produceID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID),
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO RecipeProduce (recipeID, produceID)
VALUES
(14, 9),
(8, 8),
(1, 2),
(3, 8),
(11, 1),
(7, 6),
(2, 1),
(6, 5),
(9, 3),
(12, 7),
(3, 13),
(15, 5),
(5, 4),
(4, 9),
(10, 9),
(11, 2),
(1, 5),
(8, 4),
(7, 7),
(2, 10),
(1, 10),
(1, 6),
(11, 11),
(2, 14),
(15, 8),
(3, 7),
(6, 10),
(4, 10),
(13, 11),
(9, 4),
(11, 14),
(10, 15),
(8, 2),
(2, 6),
(8, 11),
(12, 1),
(14, 8);

-- produce --> demand
CREATE TABLE IF NOT EXISTS Demand(
    produceID INT NOT NULL,
    forcastID INT NOT NULL,
    predictedDemand FLOAT,
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO Demand (produceID, forcastID, predictedDemand)
VALUES
(11, 1, 473.73),
(13, 2, 44.23),
(12, 3, 859.14),
(6, 4, 85.81),
(10, 5, 708.52),
(3, 6, 74.81),
(14, 7, 606.66),
(8, 8, 572.84),
(9, 9, 580.85),
(3, 10, 83.77),
(8, 11, 985.98),
(7, 12, 873.31);

CREATE TABLE IF NOT EXISTS Farmer(
    farmerID INT PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    status VARCHAR(500) NOT NULL,
    email VARCHAR(500) NOT NULL,
    contactInfo TEXT
);

INSERT INTO Farmer (farmerID, name, status, email, contactInfo)
VALUES
(1, 'Sharity Bruckental', 'pending', 'sb@gmail.com', 'personal'),
(2, 'Delbert Serjeant', 'approved', 'ds@gmail.com', 'business'),
(3, 'Charmaine Aleksashin', 'approved', 'ca@gmail.com', 'business'),
(4, 'Irene Carlyle', 'approved', 'ic@gmail.com', 'business'),
(5, 'Bobbette Genders', 'pending', 'bg@gmail.com', 'personal'),
(6, 'Lorita Henzer', 'suspended', 'lh@gmail.com', 'business'),
(7, 'Garvin Duffy', 'approved', 'gd@gmail.com', 'business'),
(8, 'Nana Pallesen', 'suspended', 'np@gmail.com', 'personal');


-- produce -> inventory entry
CREATE TABLE IF NOT EXISTS InventoryEntry(
    inventoryID INT PRIMARY KEY,
    farmerID INT NOT NULL,
    produceID INT NOT NULL,
    dateUpdate DATE,
    quantity INT NOT NULL,
    FOREIGN KEY (farmerID) REFERENCES Farmer(farmerID),
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO InventoryEntry (inventoryID, farmerID, produceID, dateUpdate, quantity)
VALUES
(1, 5, 11, '2025-07-30', 258),
(2, 8, 8, '2025-02-09', 47),
(3, 4, 12, '2025-03-05', 359),
(4, 8, 1, '2025-02-23', 90),
(5, 4, 7, '2025-05-09', 171),
(6, 8, 9, '2024-12-13', 177),
(7, 3, 6, '2025-04-20', 187),
(8, 4, 8, '2025-01-12', 115),
(9, 1, 9, '2025-05-07', 219),
(10, 1, 1, '2025-09-04', 394),
(11, 4, 7, '2025-10-15', 114),
(12, 1, 6, '2025-08-28', 326),
(13, 2, 5, '2024-12-24', 467),
(14, 1, 2, '2025-06-02', 101),
(15, 3, 3, '2025-05-20', 3),
(16, 1, 9, '2025-07-28', 430),
(17, 1, 4, '2025-03-07', 74),
(18, 6, 8, '2025-04-07', 130),
(19, 4, 7, '2025-10-17', 348),
(20, 6, 8, '2025-09-25', 322),
(21, 6, 9, '2025-09-21', 441),
(22, 7, 6, '2025-06-21', 202),
(23, 5, 3, '2025-08-31', 438),
(24, 4, 2, '2025-01-19', 402),
(25, 8, 5, '2025-05-14', 490),
(26, 3, 10, '2025-01-14', 237),
(27, 7, 5, '2024-12-25', 134),
(28, 1, 8, '2025-10-24', 369),
(29, 4, 4, '2025-04-19', 175),
(30, 3, 4, '2025-11-05', 206);

-- weekly Menu
CREATE TABLE IF NOT EXISTS weeklyMenu(
    menuID INT NOT NULL PRIMARY KEY,
    weekNumber INT NOT NULL
);

INSERT INTO weeklyMenu (menuID, weekNumber)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 22),
(23, 23),
(24, 24),
(25, 25),
(26, 26),
(27, 27),
(28, 28),
(29, 29),
(30, 30);

-- Recipe weekly menu
CREATE TABLE IF NOT EXISTS Recipe_WeeklyMenu(
    menuID INT NOT NULL,
    recipeID INT NOT NULL,
    PRIMARY KEY (menuID, recipeID),
    FOREIGN KEY (menuID) REFERENCES weeklyMenu(menuID) ON DELETE CASCADE,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO Recipe_WeeklyMenu(menuID, recipeID)
VALUES
(1,8),
(2,15),
(3,10),
(5,6),
(7,5),
(8,3),
(9,2),
(10,11),
(11,1),
(12,6),
(13,15),
(14,2),
(15,6),
(16,3),
(17,12),
(18,13),
(19,15),
(20,2),
(21,13),
(22,14),
(23,11),
(24,12),
(25,3),
(26,11),
(27,3),
(28,11),
(29,11),
(30,2);


-- ingredient
CREATE TABLE IF NOT EXISTS Ingredient(
    ingredientID INT PRIMARY KEY,
    name varchar(100) Not Null,
    portionSize ENUM('Small','Medium','Large'),
    amountNeeded INT NOT NULL,
    quantityAvailable INT NOT NULL,
    recipeID INT,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO Ingredient (ingredientID, name, portionSize, amountNeeded, quantityAvailable, recipeID)
VALUES
(1, 'lacus morbi quis', 'Large', 2, 83, 13),
(2, 'convallis nunc proin at', 'Large', 1, 37, null),
(3, 'faucibus cursus urna ut', 'Large', 2, 126, 11),
(4, 'dapibus augue vel accumsan', 'Medium', 5, 97, 14),
(5, 'felis eu sapien cursus', 'Large', 4, 199, 4),
(6, 'non velit nec nisi', 'Large', 3, 78, 9),
(7, 'luctus rutrum nulla', 'Small', 3, 143, 10),
(8, 'a libero nam', 'Large', 5, 81, 11),
(9, 'imperdiet sapien urna', 'Large', 1, 159, 14),
(10, 'nam tristique tortor eu', 'Medium', 1, 17, 14),
(11, 'bibendum felis sed interdum', 'Large', 5, 94, 10),
(12, 'nulla suscipit ligula in', 'Large', 4, 120, 13),
(13, 'ridiculus mus etiam vel', 'Small', 1, 172, 12),
(14, 'magna bibendum imperdiet', 'Small', 5, 170, 13),
(15, 'neque libero convallis', 'Large', 1, 172, 2),
(16, 'ligula in lacus curabitur', 'Small', 1, 133, 6),
(17, 'donec odio justo sollicitudin', 'Large', 4, 73, 2),
(18, 'duis bibendum morbi', 'Small', 3, 2, null),
(19, 'sed tristique in', 'Small', 3, 109, 9),
(20, 'molestie hendrerit at vulputate', 'Large', 5, 124, 1),
(21, 'integer non velit', 'Large', 1, 195, 11),
(22, 'ut nulla sed', 'Large', 5, 191, 8),
(23, 'id consequat in consequat', 'Small', 1, 107, 4),
(24, 'eget congue eget semper', 'Medium', 4, 87, 2),
(25, 'dictumst maecenas ut massa', 'Small', 5, 81, 7),
(26, 'amet nunc viverra', 'Large', 3, 138, 3),
(27, 'quam pharetra magna ac', 'Medium', 2, 198, 7),
(28, 'vitae mattis nibh', 'Small', 3, 136, 10),
(29, 'vulputate luctus cum', 'Small', 2, 175, 10),
(30, 'lorem vitae mattis', 'Large', 1, 97, 15);

-- CREATE TABLE IF NOT EXISTS OrderIngredient
CREATE TABLE IF NOT EXISTS OrderIngredient (
    orderID INT NOT NULL,
    ingredientID INT NOT NULL,
    PRIMARY KEY (orderID, ingredientID),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ingredientID)
);

INSERT INTO OrderIngredient (orderID, ingredientID)
VALUES
(6, 23),
(6, 12),
(21, 21),
(8, 27),
(14, 25),
(12, 3),
(3, 6),
(20, 1),
(5, 24),
(23, 24),
(12, 2),
(19, 7),
(25, 17),
(21, 11),
(14, 14),
(12, 1),
(4, 20),
(21, 30),
(6, 27),
(21, 25),
(8, 11),
(3, 19),
(13, 4),
(15, 27),
(15, 17),
(8, 22),
(24, 20),
(2, 4),
(19, 10),
(18, 14),
(11, 12),
(23, 2),
(9, 2),
(2, 13),
(12, 7),
(24, 25),
(7, 12),
(7, 6),
(16, 28);

CREATE TABLE IF NOT EXISTS Notification
(
    notificationID INT PRIMARY KEY,
    timestamp DATE NOT NULL,
    message TEXT,
    FarmerID INT NOT NULL,
    customerID INT NOT NULL,
    FOREIGN KEY (FarmerID) REFERENCES Farmer(farmerID),
    FOREIGN KEY (customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE
);

INSERT INTO Notification (notificationID, timestamp, message, FarmerID, customerID)
VALUES
(1, '2025-11-09', 'Your order has been shipped!', 5, 7),
(2, '2025-11-10', 'New produce available from your favorite farmer.', 8, 28),
(3, '2025-12-07', 'Delivery scheduled for tomorrow.', 8, 28),
(4, '2025-01-26', 'Weekly menu updated with new recipes.', 8, 43),
(5, '2025-04-10', 'Your subscription has been renewed.', 1, 20),
(6, '2025-08-12', 'Fresh harvest arriving this week!', 4, 7),
(7, '2025-10-23', 'Special discount on seasonal produce.', 7, 43),
(8, '2025-06-28', 'Your meal plan has been updated.', 1, 23),
(9, '2025-06-24', 'Driver en route with your delivery.', 2, 18),
(10, '2025-01-15', 'Thank you for your order!', 2, 25),
(11, '2025-04-05', 'New farmer joined the network.', 5, 37),
(12, '2025-08-24', 'Your feedback has been received.', 7, 24),
(13, '2025-09-24', 'Order confirmed for next week.', 7, 31),
(14, '2025-07-19', 'Produce quality report available.', 8, 3),
(15, '2025-06-12', 'Reminder: Update your dietary preferences.', 8, 44),
(16, '2025-03-13', 'Your order is being prepared.', 1, 23),
(17, '2025-02-22', 'Welcome to FreshRoutes!', 6, 37),
(18, '2025-05-05', 'Seasonal produce now in stock.', 8, 21),
(19, '2025-04-09', 'Delivery completed successfully.', 3, 23),
(20, '2025-08-16', 'Rate your recent order.', 8, 13);

CREATE TABLE IF NOT EXISTS Traffic
(
    locationID INT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    trafficLevels varchar(50) NOT NULL,
    notification TEXT,
    driverID INT NOT NULL,
    FOREIGN KEY (driverID) REFERENCES Driver(driverID) ON UPDATE CASCADE
);

INSERT INTO Traffic (locationID, timestamp, trafficLevels, notification, driverID)
VALUES
(101, '2025-02-01 08:15:23', 'Low', NULL, 1),
(102, '2025-02-01 08:17:45', 'Moderate', 'Slight delays expected.', 2),
(103, '2025-02-01 08:22:10', 'High', 'Heavy congestion reported near Exit 12.', 3),
(104, '2025-02-01 08:30:55', 'Severe', 'Road blocked due to an accident. Seek alternate route.', 2),
(105, '2025-02-01 09:05:31', 'Low', NULL, 4),
(106, '2025-02-01 09:10:12', 'Moderate', 'Traffic slowing down due to construction.', 5),
(107, '2025-02-01 09:20:41', 'High', 'Expect delays: peak hour congestion.', 1),
(10
CREATE TABLE IF NOT EXISTS Customer(
    customerID INT PRIMARY KEY,
    firstName VARCHAR(50) NOT NULL, -- think about not null or unique ????????
    lastName VARCHAR(50) NOT NULL,
    dietaryPref VARCHAR(500) NOT NULL,
    nutritionGoals VARCHAR(500) NOT NULL,
    email VARCHAR(50) -- how to handle multivalue
);

INSERT INTO Customer (CustomerID, firstName, lastName, email, dietaryPref, nutritionGoals)
VALUES
(1, 'Willdon', 'Cardillo', 'wcardillo0@posterous.com', 'gluten_free', 'muscle_gain'),
(2, 'Lyon', 'Levee', 'llevee1@auda.org.au', 'vegetarian', 'protein'),
(3, 'Garrott', 'Fairfull', 'gfairfull2@ifeng.com', 'pescatarian', 'heart_health'),
(4, 'Carolin', 'Jessel', 'cjessel3@hhs.gov', 'gluten_free', 'weight_loss'),
(5, 'Daniel', 'Thurgood', 'rthurgood4@meetup.com', 'vegetarian', 'muscle_gain'),
(6, 'Vivyanne', 'Boyington', 'vboyington5@ycombinator.com', 'pescatarian', 'muscle_gain'),
(7, 'Norma', 'Ferber', 'nferber6@netvibes.com', 'pescatarian', 'weight_loss'),
(8, 'Etta', 'Downton', 'edownton7@ucla.edu', 'pescatarian', 'heart_health'),
(9, 'Gayla', 'McKeney', 'gmckeney8@nps.gov', 'gluten_free', 'weight_loss'),
(10, 'Florina', 'Crangle', 'fcrangle9@weibo.com', 'vegetarian', 'heart_health'),
(11, 'Hasheem', 'Eteen', 'heteena@columbia.edu', 'pescatarian', 'muscle_gain'),
(12, 'Serene', 'Tankard', 'stankardb@cdbaby.com', 'none', 'protein'),
(13, 'Karlik', 'McGarrahan', 'kmcgarrahanc@rambler.ru', 'vegetarian', 'weight_loss'),
(14, 'Aharon', 'Hardaker', 'ahardakerd@joomla.org', 'gluten_free', 'weight_loss'),
(15, 'Car', 'Morrill', 'cmorrille@oakley.com', 'vegetarian', 'muscle_gain'),
(16, 'Friedrich', 'Donati', 'fdonatif@omniture.com', 'pescatarian', 'weight_loss'),
(17, 'Vaughan', 'Lakeman', 'vlakemang@geocities.com', 'pescatarian', 'muscle_gain'),
(18, 'Elsworth', 'Coggen', 'ecoggenh@cocolog-nifty.com', 'vegan', 'muscle_gain'),
(19, 'Berenice', 'Wasteney', 'bwasteneyi@nyu.edu', 'vegetarian', 'muscle_gain'),
(20, 'Rianon', 'Aloway', 'ralowayj@telegraph.co.uk', 'none', 'muscle_gain'),
(21, 'Mattie', 'Doyle', 'mdoylek@nymag.com', 'vegan', 'heart_health'),
(22, 'Keeley', 'Matthews', 'kmatthewsl@ovh.net', 'pescatarian', 'muscle_gain'),
(23, 'Nina', 'Larroway', 'nlarrowaym@github.io', 'gluten_free', 'heart_health'),
(24, 'Kristen', 'Stait', 'kstaitn@europa.eu', 'none', 'muscle_gain'),
(25, 'Klarrisa', 'Finnick', 'kfinnicko@bandcamp.com', 'vegan', 'protein'),
(26, 'Minni', 'MacNalley', 'mmacnalleyp@surveymonkey.com', 'gluten_free', 'heart_health'),
(27, 'Matt', 'China', 'mchinaq@tuttocitta.it', 'vegan', 'weight_loss'),
(28, 'Lavinia', 'Marte', 'lmarter@toplist.cz', 'none', 'heart_health'),
(29, 'Marguerite', 'Wolfenden', 'mwolfendens@surveymonkey.com', 'vegetarian', 'weight_loss'),
(30, 'Gerrilee', 'Saltrese', 'gsaltreset@ifeng.com', 'vegetarian', 'protein'),
(31, 'Liva', 'Wadworth', 'lwadworthu@booking.com', 'gluten_free', 'weight_loss'),
(32, 'Nikolos', 'Manvelle', 'nmanvellev@mashable.com', 'vegetarian', 'heart_health'),
(33, 'Cinda', 'Thickens', 'cthickensw@loc.gov', 'vegetarian', 'muscle_gain'),
(34, 'Elysee', 'Painten', 'epaintenx@1688.com', 'vegetarian', 'weight_loss'),
(35, 'Skippie', 'Kibby', 'skibbyy@arstechnica.com', 'vegan', 'muscle_gain'),
(36, 'Robinett', 'Chadbourn', 'rchadbournz@cdc.gov', 'vegan', 'muscle_gain'),
(37, 'Tamma', 'Desbrow', 'tdesbrow10@latimes.com', 'vegetarian', 'weight_loss'),
(38, 'Terrence', 'Hugonnet', 'thugonnet11@unicef.org', 'pescatarian', 'weight_loss'),
(39, 'Fanchon', 'Heigho', 'fheigho12@diigo.com', 'pescatarian', 'muscle_gain'),
(40, 'Roseanna', 'Keyse', 'rkeyse13@newsvine.com', 'vegan', 'heart_health'),
(41, 'Aviva', 'Watkiss', 'awatkiss14@nationalgeographic.com', 'vegan', 'weight_loss'),
(42, 'Theresa', 'Ventris', 'tventris15@unicef.org', 'vegan', 'muscle_gain'),
(43, 'Dyann', 'Pacheco', 'dpacheco16@netvibes.com', 'gluten_free', 'protein'),
(44, 'Emelita', 'Breitler', 'ebreitler17@123-reg.co.uk', 'none', 'heart_health'),
(45, 'Halli', 'Adamczyk', 'hadamczyk18@blog.com', 'none', 'weight_loss'),
(46, 'Jedidiah', 'Dinesen', 'jdinesen19@google.com.hk', 'gluten_free', 'heart_health'),
(47, 'Garwin', 'Szubert', 'gszubert1a@exblog.jp', 'vegan', 'protein'),
(48, 'Wenonah', 'Trevorrow', 'wtrevorrow1b@alexa.com', 'none', 'protein'),
(49, 'Jayson', 'Vern', 'jvern1c@google.cn', 'gluten_free', 'heart_health'),
(50, 'Martie', 'Osinin', 'mosinin1d@dedecms.com', 'pescatarian', 'heart_health');

CREATE TABLE IF NOT EXISTS CustomerMessage(
    messageID INT PRIMARY KEY,
    content TEXT NOT NULL,
    `timestamp` DATE NOT NULL,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) references Customer(customerID) ON UPDATE CASCADE
);

INSERT INTO CustomerMessage(messageID, content, `timestamp`, customerID)
VALUES
(1, 'Quisque ut erat.', '2025-08-30', 34),
(2, 'Nam dui. Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.', '2025-09-09', 18),
(3, 'Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus. In sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti.', '2025-09-21', 16),
(4, 'Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis.', '2024-12-24', 13),
(5, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem. Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien.', '2025-05-05', 27),
(6, 'Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend.', '2025-07-26', 10),
(7, 'In sagittis dui vel nisl. Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti. In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh.', '2025-10-24', 12),
(8, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis.', '2025-03-21', 27),
(9, 'Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst.', '2025-08-07', 48),
(10, 'Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.', '2025-04-14', 18),
(11, 'Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue.', '2025-06-21', 50),
(12, 'Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', '2025-06-16', 40),
(13, 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', '2025-09-14', 23),
(14, 'Mauris lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam.', '2025-03-05', 32),
(15, 'Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus.', '2025-05-17', 11),
(16, 'Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit. Vivamus vel nulla eget eros elementum pellentesque. Quisque porta volutpat erat. Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero.', '2025-11-22', 49),
(17, 'Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius.', '2025-05-27', 7),
(18, 'Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla.', '2025-09-02', 11),
(19, 'Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue.', '2025-02-19', 14),
(20, 'Duis ac nibh. Fusce lacus purus, aliquet at, feugiat non, pretium quis, lectus. Suspendisse potenti. In eleifend quam a odio. In hac habitasse platea dictumst. Maecenas ut massa quis augue luctus tincidunt.', '2025-09-01', 19),
(21, 'Maecenas ut massa quis augue luctus tincidunt. Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum.', '2025-07-05', 7),
(22, 'Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros.', '2025-07-04', 17),
(23, 'Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim.', '2025-10-17', 2),
(24, 'Aenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi.', '2025-06-07', 44),
(25, 'Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo. Morbi ut odio.', '2025-01-07', 34),
(26, 'Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia.', '2025-01-14', 22),
(27, 'Aenean sit amet justo. Morbi ut odio. Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc.', '2025-11-16', 42),
(28, 'Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl.', '2025-11-22', 25),
(29, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo.', '2025-08-01', 36),
(30, 'Integer a nibh.', '2025-09-10', 18);

-- Driver
CREATE TABLE IF NOT EXISTS Driver(
    DriverID INT PRIMARY KEY,
    name varchar(100) NOT NULL
);

INSERT INTO Driver (DriverID, Name)
VALUES
(1, 'Cassey Raylton'),
(2, 'Wally Truitt'),
(3, 'Ronnica Binfield'),
(4, 'Blanch Shattock'),
(5, 'Griffin Petyakov');

CREATE TABLE IF NOT EXISTS Orders(
    orderID INT PRIMARY KEY,
    `status` ENUM('pending', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
    orderDate DATE NOT NULL,
    scheduledTime DATE NOT NULL,
    deliveryAddress VARCHAR(100) NOT NULL,
    quantityOrdered INT NOT NULL,
    produceID INT NOT NULL,
    ingredientID INT NOT NULL,
    DriverID INT,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON UPDATE CASCADE ON DELETE SET NULL
);

INSERT INTO Orders (OrderID, `status`, orderDate, scheduledTime, deliveryAddress, quantityOrdered, produceID, ingredientID, DriverID, customerID) 
VALUES
(1, 'cancelled', '2025-01-08', '2025-03-27', '61 Main St', 8, 8, 15, 3, 1),
(2, 'cancelled', '2025-01-19', '2025-03-21', '30 Oak Ave', 1, 13, 6, 1, 2),
(3, 'cancelled', '2025-04-05', '2025-09-05', '68 Pine Rd', 4, 4, 24, 3, 45),
(4, 'confirmed', '2024-12-21', '2025-11-15', '93 Elm St', 8, 8, 25, 3, 31),
(5, 'out_for_delivery', '2025-01-04', '2025-01-13', '50 Maple Dr', 2, 12, 2, 4, 42),
(6, 'pending', '2025-11-11', '2025-02-27', '92 Cedar Ln', 4, 1, 30, 2, 8),
(7, 'delivered', '2025-07-14', '2025-04-28', '62 Birch Way', 4, 8, 19, null, 41),
(8, 'preparing', '2025-09-21', '2025-06-23', '11 Walnut Ct', 5, 5, 10, null, 24),
(9, 'preparing', '2025-07-12', '2025-07-07', '71 Spruce St', 1, 7, 18, 1, 29),
(10, 'out_for_delivery', '2025-04-12', '2025-05-06', '3 Ash Blvd', 10, 6, 19, 1, 9),
(11, 'cancelled', '2025-10-04', '2025-04-22', '24 Cherry Ln', 8, 1, 13, 3, 9),
(12, 'out_for_delivery', '2025-03-05', '2025-10-26', '33 Poplar Ave', 10, 6, 7, 2, 7),
(13, 'out_for_delivery', '2025-09-18', '2025-02-16', '27 Willow Rd', 1, 7, 10, 3, 31),
(14, 'cancelled', '2025-01-02', '2025-03-13', '30 Hickory Dr', 10, 1, 30, 1, 6),
(15, 'cancelled', '2024-12-18', '2025-11-18', '48 Sycamore St', 4, 1, 10, 2, 14),
(16, 'delivered', '2025-11-03', '2025-01-03', '89 Magnolia Way', 10, 2, 12, 4, 33),
(17, 'preparing', '2025-01-03', '2025-05-30', '92 Dogwood Ct', 5, 1, 22, 1, 49),
(18, 'out_for_delivery', '2025-04-17', '2025-03-27', '18 Redwood Ln', 8, 10, 21, 5, 10),
(19, 'confirmed', '2025-08-21', '2025-05-18', '45 Sequoia Ave', 7, 3, 15, 1, 32),
(20, 'delivered', '2025-04-21', '2025-10-07', '4 Cypress Rd', 10, 6, 13, 3, 43),
(21, 'out_for_delivery', '2025-04-25', '2025-08-13', '36 Palm Dr', 7, 6, 22, 1, 13),
(22, 'confirmed', '2025-08-24', '2025-09-28', '17 Juniper St', 9, 11, 18, 2, 15),
(23, 'pending', '2025-04-04', '2024-12-09', '83 Olive Way', 4, 6, 19, 2, 28),
(24, 'delivered', '2025-05-24', '2025-02-05', '12 Laurel Ct', 6, 14, 14, 4, 5),
(25, 'out_for_delivery', '2025-01-07', '2025-03-14', '72 Hazel Ln', 4, 9, 7, 3, 19);

CREATE TABLE IF NOT EXISTS DeliveryIssue(
    IssueID INT PRIMARY KEY,
    orderID INT NOT NULL,
    `timestamp` DATE NOT NULL,
    `description` TEXT,
    FOREIGN KEY (orderID) REFERENCES Orders (orderID) ON DELETE CASCADE
);

INSERT INTO DeliveryIssue (IssueID, OrderID, `timestamp`, `description`) 
VALUES 
(1, 7, '2024-12-15', 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci.'),
(2, 21, '2025-07-20', 'Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien.'),
(3, 19, '2025-05-08', 'Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor.'),
(4, 19, '2025-08-12', 'In quis justo.'),
(5, 20, '2025-09-20', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.'),
(6, 20, '2025-09-06', 'Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit.'),
(7, 18, '2025-09-24', 'Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus.'),
(8, 5, '2025-10-04', 'In congue. Etiam justo. Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius.'),
(9, 20, '2025-10-01', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam.'),
(10, 9, '2025-01-27', 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.');


-- Delivery Message
CREATE TABLE IF NOT EXISTS DeliveryMessage(
    messageID INT PRIMARY KEY,
    `timestamp` DATE NOT NULL,
    content TEXT NOT NULL,
    DriverID INT NOT NULL,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE
);

INSERT INTO DeliveryMessage (messageID, content, `timestamp`, DriverID)
VALUES 
(1, 'Quisque erat eros, viverra eget, congue eget, semper rutrum, nulla. Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui.', '2025-02-10', 4),
(2, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem. Praesent id massa id nisl venenatis lacinia. Aenean sit amet justo.', '2025-03-13', 4),
(3, 'Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus.', '2025-01-28', 3),
(4, 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat. Nulla nisl.', '2024-12-28', 4),
(5, 'Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo.', '2025-04-19', 1),
(6, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem. Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti.', '2024-12-24', 4),
(7, 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', '2025-01-20', 5),
(8, 'Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit.', '2025-04-26', 1),
(9, 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', '2025-05-21', 1),
(10, 'Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus.', '2025-02-25', 2),
(11, 'Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue.', '2025-08-14', 4),
(12, 'Quisque porta volutpat erat.', '2025-11-17', 2),
(13, 'Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo. Etiam pretium iaculis justo.', '2025-01-27', 4),
(14, 'Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros.', '2025-06-29', 4),
(15, 'Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim.', '2025-01-06', 3),
(16, 'Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est.', '2025-01-24', 1),
(17, 'Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam. Nam tristique tortor eu pede.', '2025-05-29', 4),
(18, 'Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante.', '2025-01-19', 1),
(19, 'Nunc purus. Phasellus in felis. Donec semper sapien a libero. Nam dui.', '2025-08-28', 3),
(20, 'Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla.', '2025-02-28', 5),
(21, 'Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.', '2025-03-05', 2),
(22, 'Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo.', '2025-08-02', 5),
(23, 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin risus. Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor. Morbi vel lectus in quam fringilla rhoncus.', '2024-12-16', 1),
(24, 'Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl.', '2025-01-15', 3),
(25, 'Etiam faucibus cursus urna. Ut tellus. Nulla ut erat id mauris vulputate elementum. Nullam varius. Nulla facilisi. Cras non velit nec nisi vulputate nonummy. Maecenas tincidunt lacus at velit.', '2025-10-22', 5),
(26, 'Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum.', '2025-11-23', 3),
(27, 'Nulla facilisi.', '2025-05-28', 4),
(28, 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', '2025-09-02', 4),
(29, 'Nulla mollis molestie lorem. Quisque ut erat. Curabitur gravida nisi at nibh. In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem.', '2025-06-02', 1),
(30, 'In congue.', '2025-01-22', 5);
 
-- DriverAvailibilty
CREATE TABLE IF NOT EXISTS DriverAvailability(
    availibilityID INT AUTO_INCREMENT PRIMARY KEY,
    availStartTime TIME NOT NULL, -- change the diagram, came from timeWindow
    availEndTime TIME NOT NULL, -- change the diagram, came from timeWindow
    `date` DATE NOT NULL,
    isAvailable BOOLEAN,
    DriverID INT NOT NULL,
    FOREIGN KEY (DriverID) REFERENCES Driver(DriverID) ON DELETE CASCADE
);

INSERT INTO DriverAvailability (availibilityID, availStartTime, availEndTime, `date`, isAvailable, DriverID) 
VALUES 
(1, '10:32:00', '09:27:00', '2025-11-22', true, 1),
(2, '08:19:00', '10:56:00', '2025-05-05', false, 5),
(3, '02:21:00', '18:33:00', '2025-02-05', true, 3),
(4, '11:15:00', '11:35:00', '2025-04-06', false, 5),
(5, '17:04:00', '02:13:00', '2025-08-16', true, 1),
(6, '00:42:00', '04:48:00', '2025-05-06', true, 1),
(7, '16:55:00', '05:24:00', '2025-05-15', false, 3),
(8, '21:41:00', '01:19:00', '2025-05-25', false, 4),
(9, '00:43:00', '22:42:00', '2025-08-07', true, 1),
(10, '18:23:00', '10:11:00', '2025-10-12', true, 5),
(11, '02:31:00', '18:23:00', '2025-06-13', false, 1),
(12, '23:54:00', '16:01:00', '2025-04-10', true, 5),
(13, '17:46:00', '16:35:00', '2025-03-11', true, 4),
(14, '15:49:00', '15:57:00', '2025-08-21', true, 2),
(15, '14:17:00', '19:26:00', '2025-11-19', true, 4),
(16, '11:52:00', '09:54:00', '2025-08-04', true, 1),
(17, '10:34:00', '01:20:00', '2025-11-10', false, 2),
(18, '23:47:00', '09:26:00', '2025-10-09', false, 2),
(19, '10:20:00', '01:53:00', '2025-06-28', false, 1),
(20, '13:12:00', '20:47:00', '2025-09-20', false, 2),
(21, '05:30:00', '00:26:00', '2025-11-04', true, 3),
(22, '07:46:00', '05:07:00', '2025-07-29', false, 2),
(23, '20:27:00', '17:51:00', '2025-02-08', false, 2),
(24, '21:48:00', '21:01:00', '2025-03-18', true, 1),
(25, '18:12:00', '16:17:00', '2025-11-03', true, 1),
(26, '04:43:00', '11:35:00', '2025-11-11', true, 2),
(27, '20:11:00', '08:39:00', '2025-07-13', false, 2),
(28, '03:21:00', '02:03:00', '2024-12-15', true, 1),
(29, '22:28:00', '11:26:00', '2025-10-25', true, 3),
(30, '07:55:00', '01:32:00', '2025-05-13', false, 1),
(31, '01:04:00', '06:55:00', '2025-03-05', false, 3),
(32, '13:12:00', '05:19:00', '2025-08-15', false, 5),
(33, '16:36:00', '04:52:00', '2024-12-10', true, 1),
(34, '18:46:00', '09:01:00', '2025-08-10', false, 3),
(35, '11:04:00', '15:26:00', '2025-07-06', false, 3),
(36, '03:25:00', '05:15:00', '2024-12-06', false, 5),
(37, '02:54:00', '01:17:00', '2025-04-12', true, 2),
(38, '01:29:00', '01:23:00', '2025-03-09', false, 2),
(39, '18:03:00', '10:54:00', '2025-11-18', false, 1),
(40, '22:08:00', '07:03:00', '2025-04-02', true, 3);

-- meal plan
CREATE TABLE IF NOT EXISTS mealPlan(
    mealPlanId INT PRIMARY KEY,
    startDate DATE NOT NULL,
    endDate DATE,
    customerID INT NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID) ON UPDATE CASCADE
);

INSERT INTO mealPlan (mealPlanID, startDate, endDate, customerID) 
VALUES 
(1, '2025-01-04', '2025-03-27', 28),
(2, '2025-10-29', '2025-11-13', 4),
(3, '2025-02-11', '2025-04-10', 5),
(4, '2025-02-08', '2025-06-08', 4),
(5, '2025-06-26', '2024-12-06', 38),
(6, '2025-10-28', null, 39),
(7, '2025-05-09', null, 21),
(8, '2024-12-06', '2025-02-02', 43),
(9, '2025-08-03', '2025-09-21', 13),
(10, '2025-10-29', '2025-05-04', 26);

CREATE TABLE IF NOT EXISTS Recipe(
    recipeID INT PRIMARY KEY,
    name varchar(100) NOT NULL,
    description TEXT NOT NULL,
    nutritionInfo TEXT NOT NULL,
    popularityScore SMALLINT NOT NULL,
    isActive BOOLEAN NOT NULL,
    suitibleFor TEXT NOT NULL,
    cuisineType VARCHAR(250)
);

INSERT INTO Recipe (RecipeID, Name, description, nutritionInfo, popularityScore, isActive, suitibleFor, cuisineType) 
VALUES 
(1, 'consequat nulla nisl nunc', 'Sed ante. Vivamus tortor. Duis mattis egestas metus. Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh.', 'Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue.', 99, false, 'vegan', 'mediterranean'),
(2, 'congue etiam justo etiam', 'Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis. Fusce posuere felis sed lacus. Morbi sem mauris, laoreet ut, rhoncus aliquet, pulvinar sed, nisl. Nunc rhoncus dui vel sem.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue. Etiam justo. Etiam pretium iaculis justo. In hac habitasse platea dictumst. Etiam faucibus cursus urna.', 96, true, 'vegan', 'mediterranean'),
(3, 'donec semper sapien', 'Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus.', 9, true, 'low_carb', 'asian'),
(4, 'dictumst aliquam augue', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio. Donec vitae nisi.', 'Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 95, true, 'gluten_free', 'mexican'),
(5, 'tortor risus dapibus', 'Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl. Aenean lectus. Pellentesque eget nunc. Donec quis orci eget orci vehicula condimentum. Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est.', 'Pellentesque ultrices mattis odio. Donec vitae nisi. Nam ultrices, libero non mattis pulvinar, nulla pede ullamcorper augue, a suscipit nulla elit ac nulla. Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus.', 70, true, 'gluten_free', 'asian'),
(6, 'iaculis congue vivamus', 'Mauris enim leo, rhoncus sed, vestibulum sit amet, cursus id, turpis. Integer aliquet, massa id lobortis convallis, tortor risus dapibus augue, vel accumsan tellus nisi eu orci. Mauris lacinia sapien quis libero. Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh.', 'Curabitur in libero ut massa volutpat convallis.', 96, false, 'low_carb', 'asian'),
(7, 'odio donec vitae', 'Nullam sit amet turpis elementum ligula vehicula consequat. Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet.', 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Proin interdum mauris non ligula pellentesque ultrices. Phasellus id sapien in sapien iaculis congue. Vivamus metus arcu, adipiscing molestie, hendrerit at, vulputate vitae, nisl.', 10, false, 'vegetarian', 'mexican'),
(8, 'pharetra magna ac consequat', 'Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum.', 'Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem. Duis aliquam convallis nunc.', 30, true, 'vegetarian', 'mediterranean'),
(9, 'tincidunt in leo maecenas', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.', 'Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros. Vestibulum ac est lacinia nisi venenatis tristique. Fusce congue, diam id ornare imperdiet, sapien urna pretium nisl, ut volutpat sapien arcu sed augue. Aliquam erat volutpat. In congue.', 47, false, 'vegan', 'mediterranean'),
(10, 'venenatis lacinia aenean sit', 'Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Mauris viverra diam vitae quam. Suspendisse potenti. Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 'Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Nulla dapibus dolor vel est. Donec odio justo, sollicitudin ut, suscipit a, feugiat et, eros.', 54, false, 'high_protein', 'mexican'),
(11, 'in sapien iaculis', 'Nullam porttitor lacus at turpis. Donec posuere metus vitae ipsum. Aliquam non mauris. Morbi non lectus. Aliquam sit amet diam in magna bibendum imperdiet. Nullam orci pede, venenatis non, sodales sed, tincidunt eu, felis.', 'Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum.', 4, false, 'high_protein', 'asian'),
(12, 'vitae nisl aenean', 'Proin leo odio, porttitor id, consequat in, consequat ut, nulla. Sed accumsan felis. Ut at dolor quis odio consequat varius.', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo.', 97, false, 'high_protein', 'mediterranean'),
(13, 'elit sodales scelerisque mauris', 'Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', 'Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede.', 71, false, 'high_protein', 'mexican'),
(14, 'praesent blandit nam', 'In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui.', 'Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 33, true, 'vegan', 'mexican'),
(15, 'sapien placerat ante nulla', 'Cras mi pede, malesuada in, imperdiet et, commodo vulputate, justo. In blandit ultrices enim. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.', 'Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Etiam vel augue. Vestibulum rutrum rutrum neque. Aenean auctor gravida sem.', 69, true, 'low_carb', 'mediterranean');


CREATE TABLE IF NOT EXISTS Produce(
    produceID INT PRIMARY KEY,
    name VARCHAR(250) NOT NULL,
    expectedHarvestDate DATE NOT NULL,
    quantityAvailable INT NOT NULL,
    UNIT VARCHAR(100)
);

INSERT INTO Produce (produceID, name, expectedHarvestDate, quantityAvailable, UNIT) 
VALUES 
(1, 'non velit nec nisi', '2025-03-04', 352, 'kg'),
(2, 'nisl duis bibendum', '2025-08-01', 3, 'bunches'),
(3, 'aliquet pulvinar sed', '2025-09-01', 256, 'pieces'),
(4, 'proin interdum mauris', '2025-11-23', 213, 'pieces'),
(5, 'cum sociis natoque', '2025-03-22', 340, 'pieces'),
(6, 'purus sit amet', '2025-01-02', 446, 'pieces'),
(7, 'habitasse platea dictumst', '2024-12-28', 289, 'pieces'),
(8, 'sem fusce consequat', '2025-06-03', 142, 'lbs'),
(9, 'molestie lorem quisque ut', '2024-12-10', 214, 'kg'),
(10, 'quam pede lobortis', '2024-12-16', 133, 'lbs'),
(11, 'erat quisque erat', '2025-09-21', 123, 'lbs'),
(12, 'natoque penatibus et magnis', '2025-05-17', 329, 'lbs'),
(13, 'ligula vehicula consequat morbi', '2025-04-04', 355, 'bunches'),
(14, 'sed justo pellentesque', '2024-12-20', 388, 'pieces'),
(15, 'nam ultrices libero', '2025-11-30', 241, 'kg');


-- CREATE TABLE IF NOT EXISTS OrderProduce( / can delete ?
CREATE TABLE IF NOT EXISTS OrderProduce (
    orderID INT NOT NULL,
    produceID INT NOT NULL,
    PRIMARY KEY (orderID, produceID),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO OrderProduce (orderID, produceID) 
VALUES 
(15, 4),
(10, 8),
(11, 12),
(18, 3),
(20, 12),
(16, 1),
(20, 13),
(4, 1),
(15, 3),
(4, 8),
(2, 11),
(6, 10),
(13, 1),
(5, 6),
(17, 1),
(12, 5),
(25, 1),
(10, 7),
(19, 5),
(10, 11),
(1, 10),
(5, 14),
(5, 13),
(1, 6),
(6, 3),
(20, 14),
(19, 2),
(24, 15),
(20, 10),
(22, 1),
(2, 3),
(12, 1),
(11, 9),
(24, 8),
(3, 7);

CREATE TABLE IF NOT EXISTS mealPlanRecipe(
    mealPlanID INT NOT NULL,
    recipeID INT NOT NULL,
    day VARCHAR(20) NOT NULL,
    mealType VARCHAR(20),
    PRIMARY KEY (mealPlanID, recipeID, day),
    FOREIGN KEY (mealPlanID) REFERENCES mealPlan(mealPlanID) ON DELETE CASCADE,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO mealPlanRecipe (mealPlanID, recipeID, day, mealType) 
VALUES 
(1, 1, 'Monday', 'Breakfast'),
(2, 2, 'Friday', 'Lunch'),
(3, 3, 'Monday', 'Lunch'),
(4, 4, 'Friday', 'Breakfast'),
(5, 5, 'Tuesday', 'Lunch'),
(6, 6, 'Wednesday', 'Breakfast'),
(7, 7, 'Friday', 'Lunch'),
(8, 8, 'Thursday', 'Dinner'),
(9, 9, 'Tuesday', 'Dinner'),
(10, 10, 'Thursday', 'Breakfast'),
(1, 11, 'Thursday', 'Lunch'),
(2, 12, 'Sunday', 'Dinner'),
(3, 13, 'Wednesday', 'Dinner'),
(4, 14, 'Sunday', 'Dinner'),
(5, 15, 'Sunday', 'Breakfast'),
(6, 1, 'Thursday', 'Dinner'),
(7, 2, 'Thursday', 'Breakfast'),
(8, 3, 'Wednesday', 'Dinner'),
(9, 4, 'Monday', 'Lunch'),
(10, 5, 'Sunday', 'Lunch');

-- Recipe Produce
CREATE TABLE IF NOT EXISTS RecipeProduce(
    recipeID INT NOT NULL,
    produceID INT NOT NULL,
    PRIMARY KEY(recipeID, produceID),
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID),
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO RecipeProduce (recipeID, produceID) 
VALUES 
(14, 9),
(8, 8),
(1, 2),
(3, 8),
(11, 1),
(7, 6),
(2, 1),
(6, 5),
(9, 3),
(12, 7),
(3, 13),
(15, 5),
(5, 4),
(4, 9),
(10, 9),
(11, 2),
(1, 5),
(8, 4),
(7, 7),
(2, 10),
(1, 10),
(1, 6),
(11, 11),
(2, 14),
(15, 8),
(3, 7),
(6, 10),
(4, 10),
(13, 11),
(9, 4),
(11, 14),
(10, 15),
(8, 2),
(2, 6),
(8, 11),
(12, 1),
(14, 8);

-- produce --> demand
CREATE TABLE IF NOT EXISTS Demand(
    produceID INT NOT NULL,
    forcastID INT NOT NULL,
    predictedDemand FLOAT,
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO Demand (produceID, forcastID, predictedDemand) 
VALUES 
(11, 1, 473.73),
(1, 2, 44.23),
(12, 3, 859.14),
(6, 4, 85.81),
(10, 5, 708.52),
(2, 6, 74.81),
(5, 7, 606.66),
(4, 8, 572.84),
(9, 9, 580.85),
(3, 10, 83.77),
(8, 11, 985.98),
(14, 12, 187.5),
(13, 13, 294.769),
(15, 14, 948.102),
(7, 15, 873.31);

CREATE TABLE IF NOT EXISTS Farmer(
    farmerID INT PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    status VARCHAR(500) NOT NULL,
    email VARCHAR(500) NOT NULL,
    contactInfo TEXT
);

INSERT INTO Farmer (farmerID, name, status, email, contactInfo)
VALUES 
(1, 'Sharity Bruckental', 'pending', 'sb@gmail.com', 'personal'),
(2, 'Delbert Serjeant', 'approved', 'ds@gmail.com', 'business'),
(3, 'Charmaine Aleksashin', 'approved', 'ca@gmail.com', 'business'),
(4, 'Irene Carlyle', 'approved', 'ic@gmail.com', 'business'),
(5, 'Bobbette Genders', 'pending', 'bg@gmail.com', 'personal'),
(6, 'Lorita Henzer', 'suspended', 'lh@gmail.com', 'business'),
(7, 'Garvin Duffy', 'approved', 'gd@gmail.com', 'business'),
(8, 'Nana Pallesen', 'suspended', 'np@gmail.com', 'personal');


-- produce -> inventory entry
CREATE TABLE IF NOT EXISTS InventoryEntry(
    inventoryID INT PRIMARY KEY,
    farmerID INT NOT NULL,
    produceID INT NOT NULL,
    dateUpdate DATE,
    quantity INT NOT NULL,
    FOREIGN KEY (farmerID) REFERENCES Farmer(farmerID),
    FOREIGN KEY (produceID) REFERENCES Produce(produceID)
);

INSERT INTO InventoryEntry (inventoryID, farmerID, produceID, dateUpdate, quantity) 
VALUES 
(1, 5, 11, '2025-07-30', 258),
(2, 8, 8, '2025-02-09', 47),
(3, 4, 12, '2025-03-05', 359),
(4, 8, 1, '2025-02-23', 90),
(5, 4, 7, '2025-05-09', 171),
(6, 8, 9, '2024-12-13', 177),
(7, 3, 6, '2025-04-20', 187),
(8, 4, 8, '2025-01-12', 115),
(9, 1, 9, '2025-05-07', 219),
(10, 1, 1, '2025-09-04', 394),
(11, 4, 7, '2025-10-15', 114),
(12, 1, 6, '2025-08-28', 326),
(13, 2, 5, '2024-12-24', 467),
(14, 1, 2, '2025-06-02', 101),
(15, 3, 3, '2025-05-20', 3),
(16, 1, 9, '2025-07-28', 430),
(17, 1, 4, '2025-03-07', 74),
(18, 6, 8, '2025-04-07', 130),
(19, 4, 7, '2025-10-17', 348),
(20, 6, 8, '2025-09-25', 322),
(21, 6, 9, '2025-09-21', 441),
(22, 7, 6, '2025-06-21', 202),
(23, 5, 3, '2025-08-31', 438),
(24, 4, 2, '2025-01-19', 402),
(25, 8, 5, '2025-05-14', 490),
(26, 3, 10, '2025-01-14', 237),
(27, 7, 5, '2024-12-25', 134),
(28, 1, 8, '2025-10-24', 369),
(29, 4, 4, '2025-04-19', 175),
(30, 3, 4, '2025-11-05', 206);

-- weekly Menu
CREATE TABLE IF NOT EXISTS weeklyMenu(
    menuID INT NOT NULL PRIMARY KEY,
    weekNumber INT NOT NULL
);

INSERT INTO weeklyMenu (menuID, weekNumber) 
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15),
(16, 16),
(17, 17),
(18, 18),
(19, 19),
(20, 20),
(21, 21),
(22, 22),
(23, 23),
(24, 24),
(25, 25),
(26, 26),
(27, 27),
(28, 28),
(29, 29),
(30, 30);

-- Recipe weekly menu
CREATE TABLE IF NOT EXISTS Recipe_WeeklyMenu(
    menuID INT NOT NULL,
    recipeID INT NOT NULL,
    PRIMARY KEY (menuID, recipeID),
    FOREIGN KEY (menuID) REFERENCES weeklyMenu(menuID) ON DELETE CASCADE,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO Recipe_WeeklyMenu(menuID, recipeID)
VALUES 
(1,8),
(2,15),
(3,10),
(5,6),
(7,5),
(8,3),
(9,2),
(10,11),
(11,1),
(12,6),
(13,15),
(14,2),
(15,6),
(16,3),
(17,12),
(18,13),
(19,15),
(20,2),
(21,13),
(22,14),
(23,11),
(24,12),
(25,3),
(26,11),
(27,3),
(28,11),
(29,11),
(30,2);


-- ingredient
CREATE TABLE IF NOT EXISTS Ingredient(
    ingredientID INT PRIMARY KEY,
    name varchar(100) Not Null,
    portionSize ENUM('Small','Medium','Large'),
    amountNeeded INT NOT NULL,
    quantityAvailable INT NOT NULL,
    recipeID INT,
    FOREIGN KEY (recipeID) REFERENCES Recipe(recipeID)
);

INSERT INTO Ingredient (ingredientID, 'name', portionSize, amountNeeded, quantityAvailable, recipeID) 
VALUES 
(1, 'Tomatoe', 'Large', 2, 83, 13),
(2, 'Cucumber', 'Large', 1, 37, null),
(3, 'Onion', 'Large', 2, 126, 11),
(4, 'Carrot', 'Medium', 5, 97, 14),
(5, 'Garlic', 'Large', 4, 199, 4),
(6, 'Peas', 'Large', 3, 78, 9),
(7, 'Beet', 'Small', 3, 143, 10),
(8, 'Asparagus', 5, 81, 11),
(9, 'Corn', 'Large', 1, 159, 14),
(10, 'Sweet Potatoes', 'Medium', 1, 17, 14),
(11, 'Leek', 'Large', 5, 94, 10),
(12, 'Potatoe', 'Large', 4, 120, 13),
(13, 'Artichoke', 'Small', 1, 172, 12),
(14, 'Green Bean', 'Small', 5, 170, 13),
(15, 'Brocoli', 'Large', 1, 172, 2),
(16, 'Brussel Sprouts', 'Small', 1, 133, 6),
(17, 'Cabbage', 'Large', 4, 73, 2),
(18, 'Cauliflower', 'Small', 3, 2, null),
(19, 'Celery', 'Small', 3, 109, 9),
(20, 'Eggplant', 'Large', 5, 124, 1),
(21, 'Chilli Pepper', 'Large', 1, 195, 11),
(22, 'Ginger', 5, 191, 8),
(23, 'Kale', 'Small', 1, 107, 4),
(24, 'Pumpkins', 'Medium', 4, 87, 2),
(25, 'Spinach', 'Small', 5, 81, 7),
(26, 'Tumeric', 'Large', 3, 138, 3),
(27, 'Taro', 'Medium', 2, 198, 7),
(28, 'Mushroom', 'Small', 3, 136, 10),
(29, 'Zucchini', 'Small', 2, 175, 10),
(30, 'Beetroot', 'Large', 1, 97, 15);

-- CREATE TABLE IF NOT EXISTS OrderIngredient
CREATE TABLE IF NOT EXISTS OrderIngredient (
    orderID INT NOT NULL,
    ingredientID INT NOT NULL,
    PRIMARY KEY (orderID, ingredientID),
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (ingredientID) REFERENCES Ingredient(ingredientID)
);

INSERT INTO OrderIngredient (orderID, ingredientID) 
VALUES 
(6, 23),
(6, 12),
(21, 21),
(8, 27),
(14, 25),
(12, 3),
(3, 6),
(20, 1),
(5, 24),
(23, 24),
(12, 2),
(19, 7),
(25, 17),
(21, 11),
(14, 14),
(12, 1),
(4, 20),
(21, 30),
(6, 27),
(21, 25),
(8, 11),
(3, 19),
(13, 4),
(15, 27),
(15, 17),
(8, 22),
(24, 20),
(2, 4),
(19, 10),
(18, 14),
(11, 12),
(23, 2),
(9, 2),
(2, 13),
(12, 7),
(24, 25),
(7, 12),
(7, 6),
(16, 28); 

CREATE TABLE IF NOT EXISTS Traffic
(
    locationID INT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    trafficLevels varchar(50) NOT NULL,
    notification TEXT,
    driverID INT NOT NULL,
    FOREIGN KEY (driverID) REFERENCES Driver(driverID) ON UPDATE CASCADE
);

INSERT INTO Traffic (locationID, timestamp, trafficLevels, notification, driverID) 
VALUES
(101, '2025-02-01 08:15:23', 'Low', NULL, 1),
(102, '2025-02-01 08:17:45', 'Moderate', 'Slight delays expected.', 2),
(103, '2025-02-01 08:22:10', 'High', 'Heavy congestion reported near Exit 12.', 3),
(104, '2025-02-01 08:30:55', 'Severe', 'Road blocked due to an accident. Seek alternate route.', 2),
(105, '2025-02-01 09:05:31', 'Low', NULL, 4),
(106, '2025-02-01 09:10:12', 'Moderate', 'Traffic slowing down due to construction.', 5),
(107, '2025-02-01 09:20:41', 'High', 'Expect delays: peak hour congestion.', 1),
(108, '2025-02-01 09:35:05', 'Severe', 'Visibility low. Hazardous driving conditions.', 3);