-- Don't Be Dumb Budgeting Database Schema
DROP DATABASE IF EXISTS budget_db;
CREATE DATABASE budget_db;
USE budget_db;

-- User Table
CREATE TABLE User (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    userType VARCHAR(50),
    supervisorUserID INT,
    FOREIGN KEY (supervisorUserID) REFERENCES User(userID) ON DELETE SET NULL
);

-- Category Table
CREATE TABLE Category (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    isExpense BOOLEAN DEFAULT TRUE
);

-- Account Table
CREATE TABLE Account (
    acctID INT PRIMARY KEY AUTO_INCREMENT,
    accType VARCHAR(50) NOT NULL,
    balance DECIMAL(15,2) DEFAULT 0,
    institution VARCHAR(100),
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Budget Table
CREATE TABLE Budget (
    budgetID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    limitAmount DECIMAL(15,2) NOT NULL,
    budgetType ENUM('total', 'category', 'custom') DEFAULT 'custom',
    userID INT NOT NULL,
    categoryID INT,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID) ON DELETE SET NULL
);

-- Transaction Table
CREATE TABLE Transaction (
    transactionID INT PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(15,2) NOT NULL,
    date DATE NOT NULL,
    description VARCHAR(200),
    method VARCHAR(50),
    source VARCHAR(100),
    accountID INT NOT NULL,
    categoryID INT,
    budgetID INT,
    FOREIGN KEY (accountID) REFERENCES Account(acctID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID) ON DELETE SET NULL,
    FOREIGN KEY (budgetID) REFERENCES Budget(budgetID) ON DELETE SET NULL
);

-- Saving Table
CREATE TABLE Saving (
    savingID INT PRIMARY KEY AUTO_INCREMENT,
    goalName VARCHAR(100) NOT NULL,
    targAmt DECIMAL(15,2) NOT NULL,
    currAmt DECIMAL(15,2) DEFAULT 0,
    targetDeadline DATE,
    monthlyContribution DECIMAL(15,2) DEFAULT 0,
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Subscription Table
CREATE TABLE Subscription (
    subID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    frequency VARCHAR(50),
    startDate DATE,
    nextBilling DATE,
    accountID INT NOT NULL,
    FOREIGN KEY (accountID) REFERENCES Account(acctID) ON DELETE CASCADE
);

-- Loan Table
CREATE TABLE Loan (
    loanID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    purpose VARCHAR(200),
    amount DECIMAL(15,2) NOT NULL,
    amountPaid DECIMAL(15,2) DEFAULT 0,
    interestRate DECIMAL(5,2),
    minPayment DECIMAL(15,2),
    accountID INT NOT NULL,
    FOREIGN KEY (accountID) REFERENCES Account(acctID) ON DELETE CASCADE
);

-- Investment Table
CREATE TABLE Investment (
    investmentID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    accountType VARCHAR(50),
    balance DECIMAL(15,2) DEFAULT 0,
    returnRate DECIMAL(5,2),
    userID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES User(userID) ON DELETE CASCADE
);

-- Bill Table
CREATE TABLE Bill (
    billID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    dueDate DATE NOT NULL,
    isPaid BOOLEAN DEFAULT FALSE,
    isRecurring BOOLEAN DEFAULT FALSE,
    frequency VARCHAR(50),
    accountID INT NOT NULL,
    FOREIGN KEY (accountID) REFERENCES Account(acctID) ON DELETE CASCADE
);

-- Insert Users (4 personas plus Sarah's kids)
INSERT INTO User (name, email, userType, supervisorUserID) VALUES
('Alex Chen', 'alex.chen@northeastern.edu', 'College Student', NULL),
('Jamie Rodriguez', 'jamie.rodriguez@email.com', 'Working Professional', NULL),
('Jordan Park', 'jordan.park@northeastern.edu', 'Club Treasurer', NULL),
('Sarah Kim', 'sarah.kim@email.com', 'Family Manager', NULL),
('Tommy Kim', 'tommy.kim@email.com', 'Child', 4),
('Emma Kim', 'emma.kim@email.com', 'Child', 4);

-- Insert Categories
INSERT INTO Category (name, description, isExpense) VALUES
('Food & Dining', 'Restaurants, groceries, delivery', TRUE),
('Entertainment', 'Movies, games, streaming', TRUE),
('Housing', 'Rent, mortgage, utilities', TRUE),
('Transportation', 'Gas, public transit, rideshare', TRUE),
('Personal & Other', 'Shopping, personal care', TRUE),
('Healthcare', 'Medical, dental, pharmacy', TRUE),
('Education', 'Tuition, books, supplies', TRUE),
('Shopping', 'Clothing, electronics, household', TRUE),
('Utilities', 'Electric, water, internet', TRUE),
('Subscriptions', 'Monthly services', TRUE),
('Income', 'All income sources', FALSE);

-- Insert Accounts
INSERT INTO Account (accType, balance, institution, userID) VALUES
-- Alex (User 1)
('Checking', 850, 'Bank of America', 1),
('Savings', 200, 'Bank of America', 1),
-- Jamie (User 2)
('Checking', 5200, 'Chase', 2),
('Savings', 15000, 'Chase', 2),
-- Jordan (User 3) - Club account
('Checking', 12500, 'Citizens Bank', 3),
-- Sarah (User 4)
('Checking', 8500, 'Wells Fargo', 4),
('Savings', 25000, 'Wells Fargo', 4),
('Joint Checking', 12000, 'Wells Fargo', 4);

-- Insert Budgets (Total + Category + Custom)
INSERT INTO Budget (name, limitAmount, budgetType, userID, categoryID) VALUES
-- Alex (User 1)
('Total Budget', 1400, 'total', 1, NULL),
('Food & Dining', 400, 'category', 1, 1),
('Entertainment', 200, 'category', 1, 2),
('Transportation', 100, 'category', 1, 4),
('Textbooks', 150, 'custom', 1, NULL),
-- Jamie (User 2)
('Total Budget', 10000, 'total', 2, NULL),
('Food & Dining', 800, 'category', 2, 1),
('Entertainment', 500, 'category', 2, 2),
('Housing', 2800, 'category', 2, 3),
('Vacation Fund', 500, 'custom', 2, NULL),
-- Jordan (User 3)
('Total Budget', 15000, 'total', 3, NULL),
('Club Events', 5000, 'custom', 3, NULL),
('Marketing', 2000, 'custom', 3, NULL),
('Software', 1000, 'custom', 3, NULL),
-- Sarah (User 4)
('Total Budget', 25000, 'total', 4, NULL),
('Food & Dining', 2000, 'category', 4, 1),
('Entertainment', 800, 'category', 4, 2),
('Housing', 5000, 'category', 4, 3),
('Kids Activities', 500, 'custom', 4, NULL),
('Holiday Fund', 1000, 'custom', 4, NULL);

-- Insert Transactions for Alex (User 1)
INSERT INTO Transaction (amount, date, description, method, source, accountID, categoryID, budgetID) VALUES
-- December 2025 Income
(800, '2025-12-01', 'Monthly Stipend', NULL, 'Salary', 1, 11, NULL),
(600, '2025-12-01', 'Part-time Job', NULL, 'Salary', 1, 11, NULL),
-- December 2025 Expenses
(-45, '2025-12-02', 'Uber Eats - Thai Food', 'Debit Card', NULL, 1, 1, 2),
(-12, '2025-12-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-85, '2025-12-04', 'Grocery Store', 'Debit Card', NULL, 1, 1, 2),
(-15, '2025-12-05', 'Netflix', 'Debit Card', NULL, 1, 2, 3),
(-8, '2025-12-06', 'Campus Coffee', 'Cash', NULL, 1, 1, 2),
(-25, '2025-12-07', 'Movie Tickets', 'Debit Card', NULL, 1, 2, 3),
(-35, '2025-12-08', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, 4),
(-120, '2025-12-09', 'Textbook - Database Systems', 'Debit Card', NULL, 1, 7, 5),
(-55, '2025-12-10', 'DoorDash - Pizza', 'Credit Card', NULL, 1, 1, 2),
(-30, '2025-12-11', 'Video Game', 'Debit Card', NULL, 1, 2, 3),

-- November 2025 Income
(800, '2025-11-01', 'Monthly Stipend', NULL, 'Salary', 1, 11, NULL),
(600, '2025-11-01', 'Part-time Job', NULL, 'Salary', 1, 11, NULL),
(150, '2025-11-15', 'Tutoring', NULL, 'Freelance', 1, 11, NULL),
-- November 2025 Expenses
(-90, '2025-11-03', 'Grocery Store', 'Debit Card', NULL, 1, 1, NULL),
(-12, '2025-11-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-15, '2025-11-05', 'Netflix', 'Debit Card', NULL, 1, 2, NULL),
(-65, '2025-11-08', 'Dinner with Friends', 'Debit Card', NULL, 1, 1, NULL),
(-35, '2025-11-10', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, NULL),
(-40, '2025-11-12', 'Concert Tickets', 'Credit Card', NULL, 1, 2, NULL),
(-25, '2025-11-18', 'Campus Food', 'Cash', NULL, 1, 1, NULL),
(-80, '2025-11-22', 'Black Friday Shopping', 'Credit Card', NULL, 1, 8, NULL),
(-35, '2025-11-25', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, NULL),

-- October 2025 Income
(800, '2025-10-01', 'Monthly Stipend', NULL, 'Salary', 1, 11, NULL),
(600, '2025-10-01', 'Part-time Job', NULL, 'Salary', 1, 11, NULL),
-- October 2025 Expenses
(-75, '2025-10-02', 'Grocery Store', 'Debit Card', NULL, 1, 1, NULL),
(-12, '2025-10-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-15, '2025-10-05', 'Netflix', 'Debit Card', NULL, 1, 2, NULL),
(-35, '2025-10-07', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, NULL),
(-150, '2025-10-10', 'Halloween Costume', 'Credit Card', NULL, 1, 8, NULL),
(-55, '2025-10-15', 'Restaurant', 'Debit Card', NULL, 1, 1, NULL),
(-30, '2025-10-20', 'Movie Night', 'Debit Card', NULL, 1, 2, NULL),
(-35, '2025-10-25', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, NULL),
(-45, '2025-10-28', 'Halloween Party Supplies', 'Cash', NULL, 1, 2, NULL),

-- September 2025 Income
(800, '2025-09-01', 'Monthly Stipend', NULL, 'Salary', 1, 11, NULL),
(600, '2025-09-01', 'Part-time Job', NULL, 'Salary', 1, 11, NULL),
(200, '2025-09-10', 'Birthday Money', NULL, 'Gift', 1, 11, NULL),
-- September 2025 Expenses
(-250, '2025-09-02', 'Textbooks', 'Debit Card', NULL, 1, 7, NULL),
(-12, '2025-09-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-15, '2025-09-05', 'Netflix', 'Debit Card', NULL, 1, 2, NULL),
(-100, '2025-09-08', 'School Supplies', 'Debit Card', NULL, 1, 7, NULL),
(-35, '2025-09-10', 'T Pass Monthly', 'Debit Card', NULL, 1, 4, NULL),
(-80, '2025-09-15', 'Grocery Store', 'Debit Card', NULL, 1, 1, NULL),
(-60, '2025-09-20', 'Pizza Night', 'Credit Card', NULL, 1, 1, NULL),
(-25, '2025-09-25', 'Coffee Dates', 'Cash', NULL, 1, 1, NULL),

-- August 2025 Income
(800, '2025-08-01', 'Monthly Stipend', NULL, 'Salary', 1, 11, NULL),
(700, '2025-08-01', 'Summer Job Final Pay', NULL, 'Salary', 1, 11, NULL),
-- August 2025 Expenses
(-12, '2025-08-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-15, '2025-08-05', 'Netflix', 'Debit Card', NULL, 1, 2, NULL),
(-200, '2025-08-10', 'Dorm Supplies', 'Credit Card', NULL, 1, 8, NULL),
(-150, '2025-08-12', 'Move-in Expenses', 'Debit Card', NULL, 1, 5, NULL),
(-70, '2025-08-15', 'Grocery Store', 'Debit Card', NULL, 1, 1, NULL),
(-45, '2025-08-20', 'Restaurant', 'Debit Card', NULL, 1, 1, NULL),
(-35, '2025-08-25', 'T Pass Weekly', 'Debit Card', NULL, 1, 4, NULL),

-- July 2025 Income
(1200, '2025-07-01', 'Summer Job', NULL, 'Salary', 1, 11, NULL),
(400, '2025-07-15', 'Freelance Work', NULL, 'Freelance', 1, 11, NULL),
-- July 2025 Expenses
(-12, '2025-07-03', 'Spotify Premium', 'Debit Card', NULL, 1, 10, NULL),
(-15, '2025-07-05', 'Netflix', 'Debit Card', NULL, 1, 2, NULL),
(-100, '2025-07-08', 'Beach Trip', 'Cash', NULL, 1, 2, NULL),
(-60, '2025-07-12', 'Grocery Store', 'Debit Card', NULL, 1, 1, NULL),
(-80, '2025-07-18', 'Summer Clothes', 'Credit Card', NULL, 1, 8, NULL),
(-50, '2025-07-22', 'BBQ Supplies', 'Debit Card', NULL, 1, 1, NULL),
(-35, '2025-07-28', 'Movie Theater', 'Debit Card', NULL, 1, 2, NULL);

-- Insert Transactions for Jamie (User 2)
INSERT INTO Transaction (amount, date, description, method, source, accountID, categoryID, budgetID) VALUES
-- Income
(8333, '2025-12-01', 'Monthly Salary', NULL, 'Salary', 3, 11, NULL),
(1200, '2025-12-15', 'Freelance Project', NULL, 'Freelance', 3, 11, NULL),
(150, '2025-12-10', 'Dividend Payment', NULL, 'Investment', 3, 11, NULL),
-- Expenses
(-2400, '2025-12-01', 'Mortgage Payment', 'Auto-pay', NULL, 3, 3, 9),
(-180, '2025-12-02', 'Electric Bill', 'Auto-pay', NULL, 3, 9, NULL),
(-120, '2025-12-03', 'Internet + Cable', 'Auto-pay', NULL, 3, 9, NULL),
(-450, '2025-12-05', 'Grocery Shopping', 'Credit Card', NULL, 3, 1, 7),
(-85, '2025-12-07', 'Gas Station', 'Credit Card', NULL, 3, 4, NULL),
(-200, '2025-12-08', 'Nice Dinner Out', 'Credit Card', NULL, 3, 1, 7),
(-65, '2025-12-10', 'Concert Tickets', 'Credit Card', NULL, 3, 2, 8),
(-150, '2025-12-12', 'New Clothes', 'Credit Card', NULL, 3, 8, NULL),
(-300, '2025-12-14', 'Weekend Trip Deposit', 'Debit Card', NULL, 3, 2, 10);

-- Insert Transactions for Jordan (User 3)
INSERT INTO Transaction (amount, date, description, method, source, accountID, categoryID, budgetID) VALUES
-- Income (Club funds)
(5000, '2025-09-01', 'Semester Allocation', NULL, 'Other', 5, 11, NULL),
(2500, '2025-10-15', 'Fundraiser Revenue', NULL, 'Other', 5, 11, NULL),
(1500, '2025-11-01', 'Member Dues', NULL, 'Other', 5, 11, NULL),
(3000, '2025-11-20', 'Sponsorship - Tech Corp', NULL, 'Other', 5, 11, NULL),
-- Expenses
(-800, '2025-10-20', 'Speaker Honorarium', 'Check', NULL, 5, 7, 12),
(-350, '2025-11-01', 'Event Catering', 'Debit Card', NULL, 5, 1, 12),
(-200, '2025-11-05', 'Marketing Materials', 'Debit Card', NULL, 5, 5, 13),
(-500, '2025-11-10', 'Software Licenses', 'Credit Card', NULL, 5, 10, 14),
(-1200, '2025-11-15', 'Conference Registration (5 members)', 'Credit Card', NULL, 5, 7, 12),
(-150, '2025-11-20', 'Office Supplies', 'Debit Card', NULL, 5, 5, NULL),
(-400, '2025-12-01', 'End of Year Event Venue', 'Debit Card', NULL, 5, 2, 12);

-- Insert Transactions for Sarah (User 4)
INSERT INTO Transaction (amount, date, description, method, source, accountID, categoryID, budgetID) VALUES
-- Income
(12500, '2025-12-01', 'Salary - Sarah', NULL, 'Salary', 6, 11, NULL),
(12500, '2025-12-01', 'Salary - Spouse', NULL, 'Salary', 8, 11, NULL),
-- Expenses
(-4000, '2025-12-01', 'Mortgage', 'Auto-pay', NULL, 8, 3, 18),
(-800, '2025-12-02', 'Grocery Shopping', 'Credit Card', NULL, 6, 1, 16),
(-420, '2025-12-03', 'Utilities Bundle', 'Auto-pay', NULL, 6, 9, NULL),
(-280, '2025-12-04', 'Car Insurance', 'Auto-pay', NULL, 6, 4, NULL),
(-150, '2025-12-05', 'Tommy Soccer Registration', 'Debit Card', NULL, 6, 2, 19),
(-200, '2025-12-06', 'Emma Dance Class', 'Debit Card', NULL, 6, 2, 19),
(-350, '2025-12-07', 'Family Dinner Out', 'Credit Card', NULL, 6, 1, 16),
(-500, '2025-12-08', 'Kids Clothing', 'Credit Card', NULL, 6, 8, NULL),
(-3000, '2025-12-10', 'Private School Tuition', 'Transfer', NULL, 8, 7, NULL),
(-250, '2025-12-12', 'Holiday Gifts', 'Credit Card', NULL, 6, 8, 20);

-- Insert Savings Goals
INSERT INTO Saving (goalName, targAmt, currAmt, targetDeadline, monthlyContribution, userID) VALUES
-- Alex
('Emergency Fund', 1000, 200, '2026-06-01', 50, 1),
('Spring Break Trip', 500, 150, '2026-03-15', 75, 1),
-- Jamie
('Emergency Fund', 20000, 15000, '2025-12-31', 500, 2),
('New Car', 35000, 12000, '2026-12-31', 800, 2),
('Vacation Fund', 5000, 2500, '2026-06-01', 400, 2),
-- Jordan (Club)
('Conference Fund', 3000, 1800, '2026-04-01', 200, 3),
('Equipment Upgrade', 2000, 500, '2026-08-01', 150, 3),
-- Sarah
('College Fund - Tommy', 100000, 45000, '2032-09-01', 500, 4),
('College Fund - Emma', 100000, 38000, '2034-09-01', 500, 4),
('Family Vacation', 8000, 3500, '2026-07-01', 400, 4),
('Home Renovation', 25000, 8000, '2027-01-01', 600, 4);

-- Insert Subscriptions
INSERT INTO Subscription (name, amount, frequency, startDate, nextBilling, accountID) VALUES
-- Alex
('Spotify', 12, 'monthly', '2025-01-01', '2025-12-15', 1),
('Netflix', 15, 'monthly', '2025-01-01', '2025-12-20', 1),
('Amazon Prime', 15, 'monthly', '2025-06-01', '2025-12-25', 1),
-- Jamie
('Netflix', 20, 'monthly', '2025-01-01', '2025-12-18', 3),
('Gym Membership', 50, 'monthly', '2025-01-01', '2025-12-01', 3),
('HBO Max', 16, 'monthly', '2025-03-01', '2025-12-22', 3),
('NYT Digital', 17, 'monthly', '2025-01-01', '2025-12-10', 3),
-- Jordan (Club)
('Zoom Pro', 150, 'monthly', '2025-09-01', '2025-12-01', 5),
('Canva Pro', 120, 'yearly', '2025-09-01', '2026-09-01', 5),
('Slack', 100, 'monthly', '2025-09-01', '2025-12-01', 5),
-- Sarah
('Disney+', 14, 'monthly', '2025-01-01', '2025-12-15', 6),
('Family Spotify', 17, 'monthly', '2025-01-01', '2025-12-20', 6),
('Netflix', 23, 'monthly', '2025-01-01', '2025-12-18', 6),
('Amazon Prime', 15, 'monthly', '2025-01-01', '2025-12-25', 6),
('Home Security', 45, 'monthly', '2025-01-01', '2025-12-01', 6);

-- Insert Loans
INSERT INTO Loan (name, purpose, amount, amountPaid, interestRate, minPayment, accountID) VALUES
-- Jamie
('Mortgage', 'Home Purchase', 350000, 45000, 6.5, 2400, 3),
('Car Loan', 'Vehicle', 25000, 8000, 5.9, 450, 3),
-- Sarah
('Mortgage', 'Home Purchase', 500000, 120000, 5.75, 4000, 6),
('Car Loan 1', 'SUV', 35000, 15000, 4.9, 550, 6),
('Car Loan 2', 'Sedan', 28000, 10000, 5.2, 480, 6);

-- Insert Investments
INSERT INTO Investment (name, accountType, balance, returnRate, userID) VALUES
-- Jamie
('401(k)', 'Retirement', 85000, 8.5, 2),
('Roth IRA', 'Retirement', 25000, 7.2, 2),
('Brokerage', 'Taxable', 15000, 12.1, 2),
-- Sarah
('401(k) - Sarah', 'Retirement', 150000, 7.8, 4),
('401(k) - Spouse', 'Retirement', 175000, 8.1, 4),
('529 - Tommy', 'Education', 45000, 6.5, 4),
('529 - Emma', 'Education', 38000, 6.5, 4),
('Brokerage', 'Taxable', 50000, 9.2, 4);

-- Insert Bills
INSERT INTO Bill (name, amount, dueDate, isPaid, isRecurring, frequency, accountID) VALUES
-- Alex
('Phone Bill', 45, '2025-12-15', FALSE, TRUE, 'monthly', 1),
('Rent', 400, '2025-12-01', TRUE, TRUE, 'monthly', 1),
-- Jamie
('Mortgage', 2400, '2025-12-01', TRUE, TRUE, 'monthly', 3),
('Car Insurance', 150, '2025-12-15', FALSE, TRUE, 'monthly', 3),
('Electric Bill', 180, '2025-12-10', FALSE, TRUE, 'monthly', 3),
('Internet', 120, '2025-12-05', TRUE, TRUE, 'monthly', 3),
-- Jordan (Club)
('Software Licenses', 370, '2025-12-01', TRUE, TRUE, 'monthly', 5),
-- Sarah
('Mortgage', 4000, '2025-12-01', TRUE, TRUE, 'monthly', 6),
('Car Insurance', 280, '2025-12-15', FALSE, TRUE, 'monthly', 6),
('Utilities', 420, '2025-12-10', FALSE, TRUE, 'monthly', 6),
('Private School', 3000, '2025-12-01', TRUE, TRUE, 'monthly', 8),
('Home Insurance', 200, '2025-12-20', FALSE, TRUE, 'monthly', 6);