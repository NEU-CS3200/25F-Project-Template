
DROP DATABASE IF EXISTS courtvision;
CREATE DATABASE courtvision;
USE courtvision;


DROP TABLE IF EXISTS CalculatedMetrics;
DROP TABLE IF EXISTS Annotations;
DROP TABLE IF EXISTS PlayerReports;
DROP TABLE IF EXISTS Scout_Activity;
DROP TABLE IF EXISTS Game_Stats;
DROP TABLE IF EXISTS Player_Stats;
DROP TABLE IF EXISTS Season_Stats;
DROP TABLE IF EXISTS PlayerSchedule;
DROP TABLE IF EXISTS ScheduledFor;
DROP TABLE IF EXISTS Footage;
DROP TABLE IF EXISTS RecruitingInterest;
DROP TABLE IF EXISTS Offers;
DROP TABLE IF EXISTS Verification;
DROP TABLE IF EXISTS ExportRequest;
DROP TABLE IF EXISTS UserReported;
DROP TABLE IF EXISTS Playsin;
DROP TABLE IF EXISTS Dashboard;
DROP TABLE IF EXISTS DashboardMetrics;
DROP TABLE IF EXISTS MetricsFormulas;
DROP TABLE IF EXISTS SystemAdmin;
DROP TABLE IF EXISTS Scout;
DROP TABLE IF EXISTS Game;
DROP TABLE IF EXISTS School;
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Players;


-- INDEPENDENT

-- Players Table
CREATE TABLE Players (
   playerID INT AUTO_INCREMENT PRIMARY KEY,
   firstName VARCHAR(50) NOT NULL,
   lastName VARCHAR(50) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   phone_Number VARCHAR(20),
   UserBio TEXT,
   DateofBirth DATE,
   height INT,
   weight INT,
   AcctStatus VARCHAR(20) DEFAULT 'active',
   INDEX idx_player_name (lastName, firstName),
   INDEX idx_player_email (email)
);


-- Team Table
CREATE TABLE Team (
   team_id INT AUTO_INCREMENT PRIMARY KEY,
   team_name VARCHAR(100) NOT NULL,
   city VARCHAR(50),
   team_abbrev VARCHAR(10),
   league VARCHAR(50),
   INDEX idx_team_name (team_name)
);


-- School Table
CREATE TABLE School (
   schoolID INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   city VARCHAR(50),
   state VARCHAR(50),
   INDEX idx_school_name (name)
);


-- Game Table
CREATE TABLE Game (
   gameID INT AUTO_INCREMENT PRIMARY KEY,
   date DATE NOT NULL,
   startTime TIME,
   endTime TIME,
   opponent VARCHAR(100),
   venue VARCHAR(100),
   tournament VARCHAR(100),
   score VARCHAR(20),
   INDEX idx_game_date (date)
);


-- Scout Table
CREATE TABLE Scout (
   scoutID INT AUTO_INCREMENT PRIMARY KEY,
   firstName VARCHAR(50) NOT NULL,
   lastName VARCHAR(50) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   dateOfBirth DATE,
   age INT,
   phoneNum VARCHAR(20),
   acctStatus VARCHAR(20) DEFAULT 'active',
   role VARCHAR(50),
   INDEX idx_scout_name (lastName, firstName)
);


-- SystemAdmin Table
CREATE TABLE SystemAdmin (
   adminID INT AUTO_INCREMENT PRIMARY KEY,
   firstName VARCHAR(50) NOT NULL,
   lastName VARCHAR(50) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL,
   dept VARCHAR(50),
   AcctStatus VARCHAR(20) DEFAULT 'active'
);


-- Dashboard Table
CREATE TABLE Dashboard (
   dashboardID INT AUTO_INCREMENT PRIMARY KEY,
   dashboardName VARCHAR(100),
   metricDisplayed VARCHAR(100),
   chartType VARCHAR(50),
   lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   filterCriteria TEXT
);


-- MetricsFormulas Table
CREATE TABLE MetricsFormulas (
   formulaID INT AUTO_INCREMENT PRIMARY KEY,
   formulaName VARCHAR(100) NOT NULL,
   createdBy TEXT,
   dateCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
   INDEX idx_formula_name (formulaName)
);


-- ExportRequest Table
CREATE TABLE ExportRequest (
   exportID INT AUTO_INCREMENT PRIMARY KEY,
   requestedBy INT,
   requestedUserType VARCHAR(20),
   format VARCHAR(20),
   dataType VARCHAR(50),
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   status VARCHAR(20) DEFAULT 'pending',
   completedAt DATETIME,
   CONSTRAINT fk_export_admin
       FOREIGN KEY (requestedBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_export_status (status)
);


-- ============================================
-- JUNCTION TABLES (M:N Relationships)
-- ============================================


-- Playsin - Players to Teams (M:N)
CREATE TABLE Playsin (
   playerID INT NOT NULL,
   team_id INT NOT NULL,
   startDate DATE,
   endDate DATE,
   jerseyNumber INT,
   position VARCHAR(20),
   PRIMARY KEY (playerID, team_id),
   CONSTRAINT fk_playsin_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_playsin_team
       FOREIGN KEY (team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- PlayerSchedule - Players to Games (M:N)
CREATE TABLE PlayerSchedule (
   playerID INT NOT NULL,
   gameID INT NOT NULL,


   PRIMARY KEY (playerID, gameID),
   CONSTRAINT fk_playersched_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_playersched_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- Scout_Activity - Scouts to Games (M:N)
CREATE TABLE Scout_Activity (
   scoutID INT NOT NULL,
   gameID INT NOT NULL,
   gamesAttended INT DEFAULT 1,
   notes TEXT,
   PRIMARY KEY (scoutID, gameID),
   CONSTRAINT fk_scoutactivity_scout
       FOREIGN KEY (scoutID) REFERENCES Scout(scoutID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_scoutactivity_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- ScheduledFor - Games to Teams (M:N)
CREATE TABLE ScheduledFor (
   gameID INT NOT NULL,
   team_id INT NOT NULL,
   PRIMARY KEY (gameID, team_id),
   CONSTRAINT fk_scheduled_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_scheduled_team
       FOREIGN KEY (team_id) REFERENCES Team(team_id)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- RecruitingInterest - Players to Schools (M:N)
CREATE TABLE RecruitingInterest (
   playerID INT NOT NULL,
   schoolID INT NOT NULL,
   interestLevel VARCHAR(20),
   dateAdded DATE,
   notes TEXT,
   PRIMARY KEY (playerID, schoolID),
   CONSTRAINT fk_recruiting_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_recruiting_school
       FOREIGN KEY (schoolID) REFERENCES School(schoolID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- ============================================
-- DEPENDENT TABLES (Stats and Reports)
-- ============================================


-- Season_Stats - Player season statistics
CREATE TABLE Season_Stats (
   statID INT AUTO_INCREMENT PRIMARY KEY,
   playerID INT NOT NULL,
   season VARCHAR(20) NOT NULL,
   gamesPlayed INT,
   totalMinsPlayed INT,
   avgPts DECIMAL(5,2),
   ptsPerGame DECIMAL(5,2),
   rebPerGame DECIMAL(5,2),
   astPerGame DECIMAL(5,2),
   avgRebounds DECIMAL(5,2),
   avgAsts DECIMAL(5,2),
   avgStls DECIMAL(5,2),
   three_pointers INT,
   threePPercent DECIMAL(5,2),
   fieldGoalPercent DECIMAL(5,2),
   freeThrowPercent DECIMAL(5,2),
   lastUpdated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   CONSTRAINT fk_season_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   UNIQUE INDEX idx_player_season (playerID, season)
);


-- Player_Stats - Player stats per team
CREATE TABLE Player_Stats (
   playerID INT NOT NULL,
   team_id INT NOT NULL,
   PtsPerGame DECIMAL(5,2),
   rebounds DECIMAL(5,2),
   assists DECIMAL(5,2),
   steals DECIMAL(5,2),
   blocks DECIMAL(5,2),
   turnovers DECIMAL(5,2),
   fouls DECIMAL(5,2),
   three_pt_percentage DECIMAL(5,2),
   PRIMARY KEY (playerID, team_id),
   CONSTRAINT fk_playerstats_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- Game_Stats - Player stats per game
CREATE TABLE Game_Stats (
   gameID INT NOT NULL,
   playerID INT NOT NULL,
   minutes INT,
   points INT,
   rebounds INT,
   assists INT,
   steals INT,
   blocks INT,
   turnovers INT,
   fouls INT,
   three_pt INT,
   PRIMARY KEY (gameID, playerID),
   CONSTRAINT fk_gamestats_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_gamestats_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- PlayerReports - Scout reports on players
CREATE TABLE PlayerReports (
   reportID INT AUTO_INCREMENT PRIMARY KEY,
   playerID INT NOT NULL,
   scoutID INT NOT NULL,
   summary TEXT,
   strengths TEXT,
   weaknesses TEXT,
   CONSTRAINT fk_playerreport_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_playerreport_scout
       FOREIGN KEY (scoutID) REFERENCES Scout(scoutID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   INDEX idx_report_player (playerID)
);


-- Offers - School offers to players
CREATE TABLE Offers (
   offerID INT AUTO_INCREMENT PRIMARY KEY,
   playerID INT NOT NULL,
   schoolID INT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   offerDate DATE,
   responseDate DATE,
   scholarshipType VARCHAR(50),
   scholarshipAmount DECIMAL(10,2),
   CONSTRAINT fk_offers_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_offers_school
       FOREIGN KEY (schoolID) REFERENCES School(schoolID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   INDEX idx_offer_status (status),
   INDEX idx_offer_date (offerDate)
);


-- Footage - Game footage/video
CREATE TABLE Footage (
   footageID INT AUTO_INCREMENT PRIMARY KEY,
   gameID INT NOT NULL,
   playerID INT,
   URL VARCHAR(255) NOT NULL,
   duration INT,
   CONSTRAINT fk_footage_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_footage_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_footage_game (gameID),
   INDEX idx_footage_player (playerID)
);


-- Annotations - Notes/timestamps on footage
CREATE TABLE Annotations (
   annotationID INT AUTO_INCREMENT PRIMARY KEY,
   reportID INT,
   annotatedBy INT,
   text TEXT,
   timestamp TIME,
   CONSTRAINT fk_annotations_report
       FOREIGN KEY (reportID) REFERENCES PlayerReports(reportID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   CONSTRAINT fk_annotations_scout
       FOREIGN KEY (annotatedBy) REFERENCES Scout(scoutID)
       ON UPDATE CASCADE
       ON DELETE SET NULL
);


-- CalculatedMetrics - Metrics calculated from formulas
CREATE TABLE CalculatedMetrics (
   metricID INT AUTO_INCREMENT PRIMARY KEY,
   gameID INT NOT NULL,
   playerID INT,
   formulaID INT NOT NULL,
   metricName VARCHAR(100),
   calcTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   CONSTRAINT fk_calcmetrics_game
       FOREIGN KEY (gameID) REFERENCES Game(gameID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_calcmetrics_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   CONSTRAINT fk_calcmetrics_formula
       FOREIGN KEY (formulaID) REFERENCES MetricsFormulas(formulaID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   INDEX idx_metric_game (gameID),
   INDEX idx_metric_player (playerID)
);


-- DashboardMetrics - Links dashboards to calculated metrics
CREATE TABLE DashboardMetrics (
   dashboardID INT NOT NULL,
   metricID INT NOT NULL,
   PRIMARY KEY (dashboardID, metricID),
   CONSTRAINT fk_dashmetrics_dashboard
       FOREIGN KEY (dashboardID) REFERENCES Dashboard(dashboardID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_dashmetrics_metric
       FOREIGN KEY (metricID) REFERENCES CalculatedMetrics(metricID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- UserReported - Tracking reported users/content
CREATE TABLE UserReported (
   reportID INT AUTO_INCREMENT PRIMARY KEY,
   reportedBy INT NOT NULL,
   reportedUserID INT NOT NULL,
   reportedUserType ENUM('player', 'scout', 'admin') NOT NULL,
   reason TEXT,
   severity VARCHAR(20) DEFAULT 'medium',
   status VARCHAR(20) DEFAULT 'pending',
   reportDate DATETIME DEFAULT CURRENT_TIMESTAMP,
   reviewedBy INT,
   reviewedDate DATETIME,
   resolution TEXT,
   CONSTRAINT fk_userreported_reporter
       FOREIGN KEY (reportedBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_userreported_reviewer
       FOREIGN KEY (reviewedBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_report_status (status),
   INDEX idx_report_type (reportedUserType)
);


-- Verification - Player account verification
CREATE TABLE Verification (
   validationID INT AUTO_INCREMENT PRIMARY KEY,
   playerID INT NOT NULL,
   verificationType VARCHAR(50),
   documentType VARCHAR(50),
   status VARCHAR(20) DEFAULT 'pending',
   submittedDate DATE,
   verifiedBy INT,
   verifiedDate DATE,
   notes TEXT,
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   CONSTRAINT fk_verification_player
       FOREIGN KEY (playerID) REFERENCES Players(playerID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_verification_admin
       FOREIGN KEY (verifiedBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_verification_status (status)
);


-- Validation - Data validation records
CREATE TABLE Validation (
   validationID INT AUTO_INCREMENT PRIMARY KEY,
   entityType VARCHAR(50) NOT NULL,
   entityID INT NOT NULL,
   fieldName VARCHAR(50),
   validationRule TEXT,
   isValid BOOLEAN,
   errorMessage TEXT,
   validatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
   validatedBy INT,
   CONSTRAINT fk_validation_admin
       FOREIGN KEY (validatedBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_validation_entity (entityType, entityID)
);


-- Reports - General system reports (different from PlayerReports)
CREATE TABLE Reports (
   reportID INT AUTO_INCREMENT PRIMARY KEY,
   reportName VARCHAR(100) NOT NULL,
   reportType VARCHAR(50),
   createdBy INT,
   createdDate DATETIME DEFAULT CURRENT_TIMESTAMP,
   description TEXT,
   status VARCHAR(20) DEFAULT 'active',
   CONSTRAINT fk_reports_admin
       FOREIGN KEY (createdBy) REFERENCES SystemAdmin(adminID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_report_type (reportType)
);


-- Exports - Completed export files
CREATE TABLE Exports (
   exportID INT AUTO_INCREMENT PRIMARY KEY,
   exportRequestID INT,
   fileName VARCHAR(255),
   filePath VARCHAR(255),
   fileSize INT,
   exportType VARCHAR(50),
   generatedDate DATETIME DEFAULT CURRENT_TIMESTAMP,
   expirationDate DATETIME,
   downloadCount INT DEFAULT 0,
   CONSTRAINT fk_exports_request
       FOREIGN KEY (exportRequestID) REFERENCES ExportRequest(exportID)
       ON UPDATE CASCADE
       ON DELETE SET NULL,
   INDEX idx_export_date (generatedDate)
);


-- Metric_Export - Junction table linking MetricsFormulas to Exports
CREATE TABLE Metric_Export (
   formulaID INT NOT NULL,
   exportID INT NOT NULL,
   includeRawData BOOLEAN DEFAULT FALSE,
   PRIMARY KEY (formulaID, exportID),
   CONSTRAINT fk_metricexport_formula
       FOREIGN KEY (formulaID) REFERENCES MetricsFormulas(formulaID)
       ON UPDATE CASCADE
       ON DELETE CASCADE,
   CONSTRAINT fk_metricexport_export
       FOREIGN KEY (exportID) REFERENCES Exports(exportID)
       ON UPDATE CASCADE
       ON DELETE CASCADE
);


-- Display all tables
SHOW TABLES;


USE courtvision;


SET FOREIGN_KEY_CHECKS = 0;


TRUNCATE TABLE Metric_Export;
TRUNCATE TABLE Exports;
TRUNCATE TABLE UserReported;
TRUNCATE TABLE DashboardMetrics;
TRUNCATE TABLE CalculatedMetrics;
TRUNCATE TABLE Annotations;
TRUNCATE TABLE Footage;
TRUNCATE TABLE Offers;
TRUNCATE TABLE PlayerReports;
TRUNCATE TABLE Game_Stats;
TRUNCATE TABLE Player_Stats;
TRUNCATE TABLE Season_Stats;
TRUNCATE TABLE RecruitingInterest;
TRUNCATE TABLE ScheduledFor;
TRUNCATE TABLE Scout_Activity;
TRUNCATE TABLE PlayerSchedule;
TRUNCATE TABLE Playsin;
TRUNCATE TABLE ExportRequest;
TRUNCATE TABLE MetricsFormulas;
TRUNCATE TABLE Dashboard;
TRUNCATE TABLE Verification;
TRUNCATE TABLE Validation;
TRUNCATE TABLE Reports;
TRUNCATE TABLE Scout;
TRUNCATE TABLE SystemAdmin;
TRUNCATE TABLE Game;
TRUNCATE TABLE School;
TRUNCATE TABLE Team;
TRUNCATE TABLE Players;


SET FOREIGN_KEY_CHECKS = 1;


-- =========================
-- Core reference data
-- =========================


-- Players
INSERT INTO Players (firstName, lastName, email, phone_Number, UserBio, DateofBirth, height, weight, AcctStatus) VALUES
('LeBron', 'James', 'lebron.james@email.com', '555-0101', 'Experienced forward with strong leadership skills', '2003-12-30', 78, 250, 'active'),
('Stephen', 'Curry', 'steph.curry@email.com', '555-0102', 'Elite shooter, excellent ball handler', '2004-03-14', 75, 185, 'active'),
('Kevin', 'Durant', 'kd@email.com', '555-0103', 'Versatile scorer, 7-foot forward', '2003-09-29', 82, 240, 'active'),
('Giannis', 'Antetokounmpo', 'giannis@email.com', '555-0104', 'Athletic forward, defensive specialist', '2004-12-06', 83, 242, 'active'),
('Luka', 'Doncic', 'luka.doncic@email.com','555-0105', 'Young talent, excellent court vision', '2005-02-28', 79, 230, 'active');


-- Teams
INSERT INTO Team (team_name, city, team_abbrev, league) VALUES
('Lakers', 'Los Angeles', 'LAL', 'AAU'),
('Warriors', 'Oakland', 'GSW', 'AAU'),
('Nets', 'Brooklyn', 'BKN', 'AAU'),
('Bucks', 'Milwaukee', 'MIL', 'NBA'),
('Celtics', 'Boston', 'BOS', 'NBA');


-- Schools
INSERT INTO School (name, city, state) VALUES
('Duke University', 'Durham', 'NC'),
('University of Kentucky', 'Lexington', 'KY');


-- Games
INSERT INTO Game (date, startTime, endTime, opponent, venue, tournament, score) VALUES
('2024-11-15', '18:00:00', '20:00:00', 'Warriors', 'Staples Center', 'AAU Championship', '95-88'),
('2024-11-16', '19:00:00', '21:00:00', 'Nets', 'Barclays Center', 'AAU Championship', '102-98');


-- Scouts
INSERT INTO Scout (firstName, lastName, email, dateOfBirth, age, phoneNum, acctStatus, role) VALUES
('Michael', 'Thompson', 'mthompson@scout.com', '1985-04-12', 38, '657-555-1001', 'active', 'Senior Scout'),
('Sarah', 'Johnson', 'sjohnson@scout.com', '1990-08-22', 33, '433-555-1002', 'active', 'Regional Scout');


-- SystemAdmins
INSERT INTO SystemAdmin (firstName, lastName, email, dept, AcctStatus) VALUES
('John', 'Anderson', 'jadmin@courtvision.com', 'IT', 'active'),
('Lisa', 'Chen', 'lchen@courtvision.com', 'Operations', 'active');


-- Dashboards
INSERT INTO Dashboard (dashboardName, metricDisplayed, chartType, filterCriteria) VALUES
('Player Performance Overview', 'Points Per Game', 'Bar Chart', 'season=2024'),
('Team Analytics', 'Win Rate', 'Line Chart', 'league=AAU');


-- Metric formulas
INSERT INTO MetricsFormulas (formulaName, createdBy, dateCreated) VALUES
('Player Efficiency Rating', 'System', '2024-01-15 10:00:00'),
('True Shooting Percentage', 'System', '2024-01-15 10:30:00');


-- Export requests
INSERT INTO ExportRequest (requestedBy, requestedUserType, format, dataType, status, completedAt) VALUES
(1, 'admin', 'CSV', 'Player Stats', 'completed', '2024-11-20 15:30:00'),
(2, 'admin', 'PDF', 'Scout Reports', 'completed', '2024-11-21 10:00:00');


-- =========================
-- Relationships / junctions
-- =========================


-- Players on teams
INSERT INTO Playsin (playerID, team_id, startDate, endDate, jerseyNumber, position) VALUES
(1, 1, '2024-01-01', NULL, 23, 'Forward'),
(2, 2, '2024-01-01', NULL, 30, 'Guard'),
(3, 3, '2024-01-01', NULL, 7, 'Forward');


-- Player schedule (only existing games)
INSERT INTO PlayerSchedule (playerID, gameID) VALUES
(1, 1), (1, 2),
(2, 1), (2, 2);


-- Scout activity (only existing games)
INSERT INTO Scout_Activity (scoutID, gameID, notes) VALUES
(1, 1, 'Excellent performance by #23, strong defensive presence'),
(1, 2, 'Team showed great chemistry, need to watch #7 more'),
(2, 2, 'Athletic display, several NBA-level prospects');


-- Games scheduled for teams (only valid game/team IDs)
INSERT INTO ScheduledFor (gameID, team_id) VALUES
(1, 1), (1, 2),
(2, 3), (2, 4);


-- Recruiting interest (only valid school IDs)
INSERT INTO RecruitingInterest (playerID, schoolID, interestLevel, dateAdded, notes) VALUES
(1, 1, 'High', '2024-09-01', 'Top prospect, multiple campus visits'),
(1, 2, 'High', '2024-09-05', 'Strong interest, family connections'),
(2, 2, 'Medium', '2024-09-10', 'Considering multiple programs');


-- =========================
-- Stats tables
-- =========================


-- Season stats
INSERT INTO Season_Stats (playerID, season, gamesPlayed, totalMinsPlayed, avgPts, ptsPerGame, rebPerGame, astPerGame, avgRebounds, avgAsts, avgStls, three_pointers, threePPercent, fieldGoalPercent, freeThrowPercent) VALUES
(1, '2024', 25, 800, 28.5, 28.5, 8.2, 7.1, 8.2, 7.1, 1.8, 45, 36.5, 51.2, 78.5),
(2, '2024', 28, 900, 32.1, 32.1, 5.1, 6.8, 5.1, 6.8, 1.5, 120, 43.2, 48.7, 91.3);


-- Player stats per team
INSERT INTO Player_Stats (playerID, team_id, PtsPerGame, rebounds, assists, steals, blocks, turnovers, fouls, three_pt_percentage) VALUES
(1, 1, 28.5, 8.2, 7.1, 1.8, 0.9, 3.2, 2.1, 36.5),
(2, 2, 32.1, 5.1, 6.8, 1.5, 0.3, 2.8, 1.9, 43.2);


-- Game stats
INSERT INTO Game_Stats (gameID, playerID, minutes, points, rebounds, assists, steals, blocks, turnovers, fouls, three_pt) VALUES
(1, 1, 35, 32, 9, 8, 2, 1, 3, 2, 2),
(1, 2, 38, 28, 5, 7, 1, 0, 2, 2, 5),
(1, 3, 28, 19, 4, 6, 1, 0, 2, 3, 3);


-- =========================
-- Scouting / reports / offers
-- =========================


-- Player scouting reports
INSERT INTO PlayerReports (playerID, scoutID, summary, strengths, weaknesses) VALUES
(1, 1, 'Elite all-around player with NBA-ready skills', 'Leadership, basketball IQ, versatility', 'Three-point consistency'),
(2, 1, 'Best shooter in the class, elite range', 'Shooting, ball handling', 'Defensive intensity, size'),
(3, 2, 'Skilled scorer with length advantage', 'Shooting, length', 'Lateral quickness on defense');


-- Offers (only valid school IDs)
INSERT INTO Offers (playerID, schoolID, status, offerDate, responseDate, scholarshipType, scholarshipAmount) VALUES
(1, 1, 'accepted', '2024-10-01', '2024-10-15', 'Full Scholarship', 500.00),
(2, 2, 'pending', '2024-10-05', NULL, 'Full Scholarship', 1000000.00);


-- Data validation records
INSERT INTO Validation (entityType, entityID, fieldName, validationRule, isValid, errorMessage, validatedBy) VALUES
('Player', 1, 'email', 'Valid email format', TRUE, NULL, 1),
('Player', 2, 'DateofBirth', 'Must be between 14-25 years old', TRUE, NULL, 1);


-- System-level reports
INSERT INTO Reports (reportName, reportType, createdBy, description, status) VALUES
('November Recruiting Summary', 'Recruiting', 1, 'Summary of all recruiting activities in November', 'active'),
('Top Prospects Report', 'Scouting', 2, 'Analysis of top 50 prospects for 2027 class', 'inactive');


-- Footage
INSERT INTO Footage (gameID, playerID, URL, duration) VALUES
(1, 1, 'https://footage.courtvision.com/game1_player1.mp4', 180),
(1, 2, 'https://footage.courtvision.com/game1_player2.mp4', 165);


-- Annotations (only existing scouts)
INSERT INTO Annotations (reportID, annotatedBy, text, timestamp) VALUES
(1, 1, 'Excellent defensive possession', '00:05:23'),
(1, 2, 'Great court vision on assist', '00:12:45');


-- Calculated metrics
INSERT INTO CalculatedMetrics (gameID, playerID, formulaID, metricName, calcTimestamp) VALUES
(1, 1, 1, 'Player Efficiency Rating', '2024-11-15 22:00:00'),
(1, 2, 1, 'Player Efficiency Rating', '2024-11-15 22:00:00');


-- Dashboard ↔ metrics
INSERT INTO DashboardMetrics (dashboardID, metricID) VALUES
(1, 1),
(1, 2);


-- UserReported (moderation)
INSERT INTO UserReported (reportedBy, reportedUserID, reportedUserType, reason, severity, status, reviewedBy, reviewedDate, resolution) VALUES
(1, 5, 'player', 'Inappropriate communication with scouts', 'medium', 'resolved', 2, '2024-11-20 14:00:00', 'Warning issued, monitoring account'),
(2, 3, 'scout', 'Violation of scouting ethics', 'high', 'under_review', NULL, NULL, NULL);


-- Exports (only valid ExportRequest IDs 1 and 2)
INSERT INTO Exports (exportRequestID, fileName, filePath, fileSize, exportType, expirationDate, downloadCount) VALUES
(1, 'player_stats_nov2024.csv', '/exports/2024/11/player_stats_nov2024.csv', 245678, 'CSV', '2024-12-20 23:59:59', 5),
(2, 'scout_reports_nov2024.pdf', '/exports/2024/11/scout_reports_nov2024.pdf', 1234567, 'PDF', '2024-12-21 23:59:59', 3);


-- Metric_Export (link formulas to exports)
INSERT INTO Metric_Export (formulaID, exportID, includeRawData) VALUES
(1, 1, TRUE),
(2, 1, TRUE);


SHOW TABLES;
SELECT * FROM Players;
SELECT * FROM Game_Stats;
