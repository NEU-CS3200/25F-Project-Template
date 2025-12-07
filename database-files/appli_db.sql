DROP DATABASE IF EXISTS `appliTracker`;
CREATE DATABASE IF NOT EXISTS `appliTracker`;
USE `appliTracker`;

DROP TABLE IF EXISTS SystemAdmin;
CREATE TABLE SystemAdmin
(
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(75) NOT NULL UNIQUE,
    adminID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    INDEX indexAdminID (adminID)
);

DROP TABLE IF EXISTS SystemConfigurations;
CREATE TABLE SystemConfigurations
(
    daysToBackup INT NOT NULL,
    dataRetentionTime INT,
    backupSchedule DATETIME NOT NULL,
    alertThresholdCPU BOOLEAN NOT NULL DEFAULT FALSE,
    lastModifiedDate DATE,
    alertThresholdQueryTime BOOLEAN NOT NULL DEFAULT FALSE,
    maintenanceStartDateTime DATETIME,
    maintenanceEndDateTIme DATETIME,
    configID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT NOT NULL,
    CONSTRAINT fk_0 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexConfigID (configID)
);

DROP TABLE IF EXISTS ResourceUsage;
CREATE TABLE ResourceUsage
(
    timeStamp TIMESTAMP NOT NULL,
    activeUsers INT NOT NULL DEFAULT 0,
    numApplications INT NOT NULL DEFAULT 0,
    dbSize VARCHAR(50) NOT NULL,
    cpuUsagePct DOUBLE NOT NULL,
    usageID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT NOT NULL,
    CONSTRAINT fk_1 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexUsageID (usageID)
);

DROP TABLE IF EXISTS PerformanceMetric;
CREATE TABLE PerformanceMetric
(
    type VARCHAR(50) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    measurement DOUBLE NOT NULL,
    timeStamp TIMESTAMP NOT NULL,
    metricID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT NOT NULL,
    CONSTRAINT fk_2 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexMetricID (metricID)
);

DROP TABLE IF EXISTS Backup;
CREATE TABLE Backup
(
    size DOUBLE NOT NULL,
    status VARCHAR(50) NOT NULL,
    health VARCHAR(50) NOT NULL,
    datePerformed DATE,
    backupID INT PRIMARY KEY AUTO_INCREMENT,
    adminID INT NOT NULL,
    CONSTRAINT fk_3 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexBackupID (backupID)
);

DROP TABLE IF EXISTS SystemUpdate;
CREATE TABLE SystemUpdate
(
    updateDate DATE,
    status VARCHAR(50) NOT NULL,
    updatedVersion VARCHAR(50),
    currentVersion VARCHAR(50) NOT NULL,
    patchNotes VARCHAR(50),
    updateID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT NOT NULL,
    CONSTRAINT fk_4 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexUpdateID (updateID)
);

DROP TABLE IF EXISTS Alert;
CREATE TABLE Alert
(
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(50),
    message VARCHAR(50),
    isResolved BOOLEAN NOT NULL DEFAULT FALSE,
    timeStamp TIMESTAMP NOT NULL,
    alertID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT NOT NULL,
    usageID INT,
    backupID INT,
    metricID INT,
    updateID INT,
    CONSTRAINT fk_5 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_6 FOREIGN KEY (usageID)
        REFERENCES ResourceUsage (usageID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_7 FOREIGN KEY (backupID)
        REFERENCES Backup (backupID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_8 FOREIGN KEY (metricID)
        REFERENCES PerformanceMetric (metricID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_9 FOREIGN KEY (updateID)
        REFERENCES SystemUpdate (updateID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexAlertID (alertID)
);

DROP TABLE IF EXISTS CareerCoach;
CREATE TABLE CareerCoach
(
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    coachID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    INDEX indexCoachID (coachID)
);

DROP TABLE IF EXISTS Student;
CREATE TABLE Student
(
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    major VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    graduationDate DATE,
    studentID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    coachID INT NOT NULL,
    CONSTRAINT fk_14 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexStudentID (studentID)
);


DROP TABLE IF EXISTS HiringCoordinator;
CREATE TABLE HiringCoordinator
(
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    companyName VARCHAR(50) NOT NULL,
    coordinatorID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    INDEX indexCoordinatorID (coordinatorID)
);

DROP TABLE IF EXISTS Audit;
CREATE TABLE Audit
(
    summary VARCHAR(50) NOT NULL,
    tableName VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    timeStamp TIMESTAMP NOT NULL,
    recordID INT,
    auditID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    adminID INT,
    studentID INT,
    coordinatorID INT,
    coachID INT,
    CONSTRAINT fk_10 FOREIGN KEY (adminID)
        REFERENCES SystemAdmin (adminID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_11 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_12 FOREIGN KEY (coordinatorID)
        REFERENCES HiringCoordinator (coordinatorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_13 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexAuditID (auditID)
);

DROP TABLE IF EXISTS JobPosting;
CREATE TABLE JobPosting
(
    title VARCHAR(50) NOT NULL,
    roleType VARCHAR(50) NOT NULL,
    location VARCHAR(50) NOT NULL,
    department VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    datePosted DATE NOT NULL,
    dateClosed DATE,
    postingID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    coordinatorID INT NOT NULL,
    CONSTRAINT fk_15 FOREIGN KEY (coordinatorID)
        REFERENCES HiringCoordinator (coordinatorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexPostingID (postingID)
);

DROP TABLE IF EXISTS Platform;
CREATE TABLE Platform
(
    name VARCHAR(50) NOT NULL,
    platformType VARCHAR(50) NOT NULL,
    baseURL VARCHAR(50) NOT NULL,
    platformID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    INDEX indexPlatformID (platformID)
);

DROP TABLE IF EXISTS StudentProgressMetrics;
CREATE TABLE StudentProgressMetrics
(
    lastActivityDate DATE NOT NULL,
    offersReceived INT NOT NULL DEFAULT 0,
    interviewsScheduled INT NOT NULL DEFAULT 0,
    numJobApplied INT NOT NULL DEFAULT 0,
    progressID INT NOT NULL,
    studentID INT NOT NULL,
    PRIMARY KEY (progressID, studentID),
    CONSTRAINT fk_16 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX indexProgressIDStudentID (progressID, studentID),
    INDEX indexStudentID (studentID)
);

DROP TABLE IF EXISTS JobListing;
CREATE TABLE JobListing
(
    listingStatus VARCHAR(50) NOT NULL,
    datePublished DATE NOT NULL,
    expiresOn DATETIME ,
    lastChecked DATETIME,
    postingURL VARCHAR(50) NOT NULL,
    listingID INT NOT NULL,
    postingID INT NOT NULL,
    PRIMARY KEY (listingID, postingID),
    platformID INT NOT NULL,
    CONSTRAINT fk_17 FOREIGN KEY (platformID)
        REFERENCES Platform (platformID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_18 FOREIGN KEY (postingID)
        REFERENCES JobPosting (postingID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX indexListingIDPostingID (listingID, postingID),
    INDEX indexPostingID (postingID)
);

DROP TABLE IF EXISTS Report;
CREATE TABLE Report
(
    generatedDate DATE NOT NULL,
    summary VARCHAR(50) NOT NULL,
    reportID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    coachID INT NOT NULL,
    CONSTRAINT fk_19 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexReportID (reportID)
);

DROP TABLE IF EXISTS ReportItem;
CREATE TABLE ReportItem
(
    recommendations VARCHAR(50) NOT NULL,
    notes VARCHAR(50) NOT NULL,
    keyFindings VARCHAR(50) NOT NULL,
    itemID INT NOT NULL,
    reportID INT NOT NULL,
    PRIMARY KEY (itemID, reportID),
    studentID INT NOT NULL,
    CONSTRAINT fk_20 FOREIGN KEY (reportID)
        REFERENCES Report (reportID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_21 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexItemIDReportID (itemID, reportID),
    INDEX indexReportID (reportID)
);

DROP TABLE IF EXISTS coachSPM;
CREATE TABLE coachSPM
(
    coachID INT NOT NULL,
    progressID INT NOT NULL,
    studentID INT NOT NULL,
    PRIMARY KEY (coachID, progressID, studentID),
    CONSTRAINT fk_22 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_23 FOREIGN KEY (progressID, studentID)
        REFERENCES StudentProgressMetrics (progressID, studentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX indexCoachID (coachID),
    INDEX indexProgressIDStudentID (progressID, studentID)
);

DROP TABLE IF EXISTS Resume;
CREATE TABLE Resume
(
    imageURl VARCHAR(50) NOT NULL,
    label VARCHAR(50) NOT NULL,
    resumeID INT NOT NULL AUTO_INCREMENT,
    studentID INT NOT NULL,
    PRIMARY KEY (resumeID, studentID),
    CONSTRAINT fk_24 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    INDEX indexResumeIDStudentID (resumeID, studentID),
    INDEX indexStudentID (studentID)
);

DROP TABLE IF EXISTS JobApplication;
CREATE TABLE JobApplication
(
    companyName VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    stage VARCHAR(50),
    dateApplied DATE,
    lastUpdated DATETIME NOT NULL,
    applicationID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    jobBoard VARCHAR(50),
    studentID INT NOT NULL,
    listingID INT NOT NULL,
    postingID INT NOT NULL,
    resumeID INT NOT NULL,
    CONSTRAINT fk_25 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_26 FOREIGN KEY (listingID, postingID)
        REFERENCES JobListing (listingID, postingID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_27 FOREIGN KEY (resumeID, studentID)
        REFERENCES Resume (resumeID, studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexApplicationID (applicationID)
);

DROP TABLE IF EXISTS Notification;
CREATE TABLE Notification
(
    type VARCHAR(50) NOT NULL,
    isRead BOOLEAN NOT NULL DEFAULT FALSE,
    dateTimeSent DATETIME NOT NULL,
    notificationID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    coachID INT,
    studentID INT,
    applicationID INT,
    coordinatorID INT,
    listingID INT,
    postingID INT,
    CONSTRAINT fk_31 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_32 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_33 FOREIGN KEY (applicationID)
        REFERENCES JobApplication (applicationID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_34 FOREIGN KEY (coordinatorID)
        REFERENCES HiringCoordinator (coordinatorID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_35 FOREIGN KEY (listingID, postingID)
        REFERENCES JobListing (listingID, postingID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexNotificationID (notificationID)
);

DROP TABLE IF EXISTS Message;
CREATE TABLE Message
(
    content VARCHAR(50) NOT NULL,
    dateTimeSent DATETIME NOT NULL,
    messageID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    studentID INT NOT NULL,
    coachID INT NOT NULL,
    notificationID INT NOT NULL,
    CONSTRAINT fk_28 FOREIGN KEY (studentID)
        REFERENCES Student (studentID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_29 FOREIGN KEY (coachID)
        REFERENCES CareerCoach (coachID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_30 FOREIGN KEY (notificationID)
        REFERENCES Notification (notificationID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    INDEX indexMessageID (messageID)
);







-- NO EXTRA DATA NEEDED
INSERT INTO SystemAdmin (fName, lName, email)
VALUES ('John', 'Joe', 'johnjoe@gmail.com');


INSERT INTO CareerCoach (firstName, lastName, email)
VALUES ('Marcus', 'Smith', 'marcussmith@gmail.com'),
       ('Joe', 'Johnson', 'joeJohnson@gmail.com');

INSERT INTO CareerCoach (firstName, last_name, email) VALUES
('Angelo', 'Shalders', 'ashalders0@guardian.co.uk'),
('Cozmo', 'Balshen', 'cbalshen1@myspace.com'),
('Nelli', 'Rann', 'nrann2@usda.gov'),
('Alejoa', 'Saggs', 'asaggs3@oracle.com'),
('Freda', 'Tremble', 'ftremble4@yellowbook.com'),
('Lorrin', 'Inglish', 'linglish5@ning.com'),
('Agnella', 'Slyde', 'aslyde6@lycos.com'),
('Essy', 'Allibon', 'eallibon7@archive.org'),
('Joanne', 'Maken', 'jmaken8@unc.edu'),
('Hodge', 'Guiver', 'hguiver9@soundcloud.com'),
('Silvester', 'Crawford', 'scrawforda@google.ca'),
('Carlynne', 'Mablestone', 'cmablestoneb@twitpic.com'),
('Jarib', 'McCuaig', 'jmccuaigc@globo.com'),
('Torr', 'Sleaford', 'tsleafordd@youku.com'),
('Liana', 'Barrim', 'lbarrime@purevolume.com'),
('Mollee', 'Chessor', 'mchessorf@de.vu'),
('Agnola', 'Kinnach', 'akinnachg@diigo.com'),
('Magdalena', 'Paddeley', 'mpaddeleyh@163.com'),
('Nilson', 'Sunnucks', 'nsunnucksi@ovh.net'),
('Lydon', 'Trent', 'ltrentj@alibaba.com'),
('Floris', 'Guinan', 'fguinank@princeton.edu'),
('Bernete', 'Bispham', 'bbisphaml@narod.ru'),
('Englebert', 'Lombard', 'elombardm@mozilla.org'),
('Wallache', 'Kyngdon', 'wkyngdonn@trellian.com'),
('Maison', 'Robarts', 'mrobartso@mail.ru'),
('Leia', 'Abyss', 'labyssp@nsw.gov.au'),
('Hillyer', 'Blatherwick', 'hblatherwickq@youtube.com'),
('Chrisse', 'Hallward', 'challwardr@mapquest.com'),
('Cobby', 'Mardell', 'cmardells@tuttocitta.it'),
('Beatrix', 'Broadist', 'bbroadistt@goodreads.com'),
('Harmony', 'Conradie', 'hconradieu@addthis.com'),
('Phillis', 'Lockney', 'plockneyv@squidoo.com'),
('Tarra', 'Jancey', 'tjanceyw@whitehouse.gov'),
('Brittney', 'Aizkovitch', 'baizkovitchx@jigsy.com'),
('Zack', 'McGeaney', 'zmcgeaneyy@uol.com.br'),
('Ax', 'Emloch', 'aemlochz@nhs.uk'),
('Sasha', 'Croll', 'scroll10@amazon.de'),
('Anderson', 'Whichelow', 'awhichelow11@noaa.gov'),
('Zsazsa', 'Heckle', 'zheckle12@booking.com'),
('Lindon', 'Maving', 'lmaving13@dropbox.com');





INSERT INTO HiringCoordinator (fName, lName, email, companyName)
VALUES ('Sophia', 'Soap', 'sophiasoap@gmail.com', 'Amazon'),
       ('Dirt', 'Dog', 'dirtdog@gmail.com', 'Chewy');

INSERT INTO HiringCoordinator (fName, lName, email, CompanyName) VALUES
('Stephen', 'Hedylstone', 'shedylstone0@odnoklassniki.ru', 'Bluejam'),
('Sidnee', 'Dale', 'sdale1@examiner.com', 'Katz'),
('Dolley', 'Longforth', 'dlongforth2@eepurl.com', 'Thoughtbeat'),
('Fletch', 'Perch', 'fperch3@baidu.com', 'Zoozzy'),
('Anabelle', 'Dennett', 'adennett4@usnews.com', 'Npath'),
('Robert', 'Trew', 'rtrew5@123-reg.co.uk', 'Jayo'),
('Hestia', 'Linstead', 'hlinstead6@tripadvisor.com', 'Riffwire'),
('Tommi', 'Tuckerman', 'ttuckerman7@nsw.gov.au', 'Flipstorm'),
('Wilton', 'Harrild', 'wharrild8@toplist.cz', 'Twinder'),
('Don', 'Rabbage', 'drabbage9@pagesperso-orange.fr', 'Skimia'),
('Evan', 'Kelloch', 'ekellocha@irs.gov', 'Thoughtbeat'),
('Tove', 'Kitcatt', 'tkitcattb@chronoengine.com', 'Jetwire'),
('Shannan', 'Gemeau', 'sgemeauc@ycombinator.com', 'Kwinu'),
('Erina', 'Cluckie', 'ecluckied@senate.gov', 'Devshare'),
('Griz', 'Abram', 'gabrame@about.com', 'Twinder'),
('Cobb', 'Ricco', 'criccof@auda.org.au', 'Eayo'),
('Ellery', 'McConway', 'emcconwayg@prweb.com', 'Topiczoom'),
('Cammie', 'Robb', 'crobbh@reverbnation.com', 'Riffpedia'),
('Anthea', 'Rapi', 'arapii@com.com', 'Yakijo'),
('Cati', 'Corben', 'ccorbenj@tinyurl.com', 'Meetz'),
('Vikki', 'Dunsford', 'vdunsfordk@wordpress.com', 'Chatterbridge'),
('Sherry', 'Justice', 'sjusticel@1688.com', 'Yodoo'),
('Daphna', 'Billison', 'dbillisonm@prweb.com', 'Shuffletag'),
('Gui', 'Strike', 'gstriken@reference.com', 'Oyoloo'),
('Nancey', 'Ide', 'nideo@mac.com', 'Ainyx'),
('Timmy', 'MacCaghan', 'tmaccaghanp@1688.com', 'Trudoo'),
('Caresa', 'Sacks', 'csacksq@usnews.com', 'Browsetype'),
('Florry', 'Brun', 'fbrunr@dmoz.org', 'Layo'),
('Carri', 'Ravens', 'cravenss@godaddy.com', 'Zoovu'),
('Jeffry', 'Feria', 'jferiat@epa.gov', 'Voomm'),
('Trudie', 'McCleod', 'tmccleodu@sbwire.com', 'Omba'),
('Moises', 'Sessions', 'msessionsv@icq.com', 'Wikibox'),
('Gilbert', 'Hansel', 'ghanselw@qq.com', 'Eazzy'),
('Anna-diana', 'Thomasset', 'athomassetx@goodreads.com', 'Jayo'),
('Alfie', 'Stott', 'astotty@bandcamp.com', 'Topdrive'),
('Sara', 'Andryushin', 'sandryushinz@simplemachines.org', 'Tekfly'),
('Kerby', 'Perllman', 'kperllman10@liveinternet.ru', 'Ooba'),
('Theda', 'Collyer', 'tcollyer11@pinterest.com', 'Flashdog'),
('Gladys', 'Berrigan', 'gberrigan12@imdb.com', 'Shuffletag'),
('Humfried', 'Edis', 'hedis13@tmall.com', 'Yambee');




-- NO EXTRA DATA NEEDED
INSERT INTO Platform (name, platformType, baseURL)
VALUES ('LinkedIn', 'Online', 'https://www.linkedin.com/'),
       ('NUworks', 'Online', 'https://northeastern-csm.symplicity.com/students/');

INSERT INTO Student (firstName, lastName, email, major, graduationDate, coachID)
VALUES ('James', 'Jane', 'jamesjane@gmail.com', 'Computer Science', NULL, 1),
       ('Alice', 'Bob', 'alicebob@gmail.com', 'Math', NULL, 2);

INSERT INTO Student (firstName, last_name, email, major, `graduation Data`, coachID) VALUES
('Debee', 'Guilaem', 'dguilaem0@vistaprint.com', 'Data Science', '2027-06-21', 3),
('Clifford', 'Guile', 'cguile1@homestead.com', 'Healthcare Management', '2029-03-24', 4),
('Carlen', 'Ridgedell', 'cridgedell2@gizmodo.com', 'Geology', '2029-03-30', 5),
('Valentina', 'Doornbos', 'vdoornbos3@ycombinator.com', 'Geology', '2025-12-24', 6),
('Corrie', 'Dilloway', 'cdilloway4@youtube.com', 'Business Administration', '2029-09-26', 7),
('Laurene', 'Amps', 'lamps5@va.gov', 'Nursing', '2026-09-21', 8),
('Tallia', 'Woolcocks', 'twoolcocks6@ftc.gov', 'Nursing', '2028-03-07', 9),
('Freddy', 'Jinkin', 'fjinkin7@histats.com', 'Data Science', '2028-10-17', 10),
('Madlen', 'Pawsey', 'mpawsey8@gizmodo.com', 'Business Administration', '2027-08-13', 11),
('Zachery', 'Bull', 'zbull9@is.gd', 'Computer Science', '2027-10-19', 12),
('Sophronia', 'Wyse', 'swysea@kickstarter.com', 'Nursing', '2027-02-14', 13),
('Josselyn', 'Hanniger', 'jhannigerb@census.gov', 'Consulting', '2026-07-21', 14),
('Donia', 'Aubury', 'dauburyc@yale.edu', 'Consulting', '2026-07-08', 15),
('George', 'Hove', 'ghoved@army.mil', 'Business Administration', '2029-03-09', 16),
('Paxon', 'Whittier', 'pwhittiere@infoseek.co.jp', 'Data Science', '2027-03-18', 17),
('Jermayne', 'Emmines', 'jemminesf@gmpg.org', 'Nursing', '2026-02-27', 18),
('Pegeen', 'Cotterrill', 'pcotterrillg@feedburner.com', 'Computer Science', '2027-05-20', 19),
('Jamaal', 'Kiddy', 'jkiddyh@utexas.edu', 'Data Science', '2028-08-24', 20),
('Linnet', 'Anfossi', 'lanfossii@123-reg.co.uk', 'Data Science', '2026-08-15', 21),
('Halie', 'Kenaway', 'hkenawayj@nytimes.com', 'Nursing', '2027-02-26', 22),
('Ilario', 'Huriche', 'ihurichek@163.com', 'Business Administration', '2029-07-09', 23),
('Tim', 'Wardhough', 'twardhoughl@imdb.com', 'Computer Science', '2027-08-10', 24),
('Cedric', 'Whatson', 'cwhatsonm@storify.com', 'Data Science', '2026-10-26', 25),
('Phyllys', 'Spera', 'psperan@economist.com', 'Computer Science', '2026-01-25', 26),
('Thomasina', 'Waterstone', 'twaterstoneo@163.com', 'Consulting', '2027-11-19', 27),
('Gustave', 'Antonin', 'gantoninp@goo.gl', 'Data Science', '2027-07-10', 28),
('Tamma', 'Holbury', 'tholburyq@google.es', 'Data Science', '2027-05-26', 29),
('Wilone', 'Sorensen', 'wsorensenr@cyberchimps.com', 'Geology', '2028-11-24', 30),
('Kalinda', 'Teasdale-Markie', 'kteasdalemarkies@posterous.com', 'Nursing', '2027-08-22', 31),
('Duff', 'Whitebrook', 'dwhitebrookt@tinypic.com', 'Consulting', '2026-05-21', 32),
('Penrod', 'Matheson', 'pmathesonu@smh.com.au', 'Business Administration', '2026-06-16', 33),
('Gordie', 'Brabant', 'gbrabantv@trellian.com', 'Geology', '2028-03-19', 34),
('Maxie', 'Imms', 'mimmsw@umn.edu', 'Business Administration', '2029-10-31', 35),
('Catharine', 'Titchard', 'ctitchardx@whitehouse.gov', 'Healthcare Management', '2029-08-28', 36),
('Nessi', 'McBrearty', 'nmcbreartyy@typepad.com', 'Consulting', '2027-12-27', 37),
('Paul', 'Oldacres', 'poldacresz@quantcast.com', 'Healthcare Management', '2029-12-23', 38),
('Tarrance', 'Suter', 'tsuter10@miitbeian.gov.cn', 'Business Administration', '2027-08-27', 39),
('Carlyn', 'Willavoys', 'cwillavoys11@prlog.org', 'Nursing', '2028-11-04', 40),
('Crissie', 'Yurov', 'cyurov12@umn.edu', 'Nursing', '2029-02-10', 41),
('Titus', 'Lippi', 'tlippi13@forbes.com', 'Nursing', '2029-10-14', 42);


-- NO EXTRA DATA NEEDED
INSERT INTO SystemConfigurations (daysToBackup, dataRetentionTime, backupSchedule, 
                                  alertThresholdCPU, lastModifiedDate, alertThresholdQueryTime,
                                  maintenanceStartDateTime, maintenanceEndDateTIme, adminID)
VALUES (20, NULL, '2025-07-10 15:41:00', FALSE, NULL, FALSE, NULL, NULL, 1),
       (30, NULL, '2026-07-10 15:41:00', TRUE, NULL, FALSE, NULL, NULL, 1);


INSERT INTO ResourceUsage (timeStamp, activeUsers, numApplications, dbSize, cpuUsagePct, adminID)
VALUES ('2025-10-10 15:41:00', 1, 2, '100 GB', 0.67, 1),
       ('2025-10-10 15:41:00', 0, 0, '1 GB', 0.50, 1);

INSERT INTO ResourceUsage 
(timeStamp, activeUsers, numApplications, dbSize, cpuUsagePct, adminID)
VALUES
('2025-10-01 09:00:00', 45, 120,  '72 GB',  48.3, 1),
('2025-10-02 09:00:00', 52, 145,  '74 GB',  50.1, 1),
('2025-10-03 09:00:00', 61, 180,  '75 GB',  55.4, 1),
('2025-10-04 09:00:00', 58, 170,  '77 GB',  53.8, 1),
('2025-10-05 09:00:00', 64, 210,  '79 GB',  57.2, 1),
('2025-10-06 09:00:00', 71, 260,  '81 GB',  60.9, 1),
('2025-10-07 09:00:00', 85, 320,  '82 GB',  63.5, 1),
('2025-10-08 09:00:00', 92, 410,  '84 GB',  67.1, 1),
('2025-10-09 09:00:00', 88, 390,  '86 GB',  65.8, 1),
('2025-10-10 09:00:00', 97, 520,  '88 GB',  70.4, 1),
('2025-10-12 09:00:00', 105, 615, '90 GB',  72.9, 1),
('2025-10-14 09:00:00', 118, 740, '92 GB',  74.6, 1),
('2025-10-16 09:00:00', 130, 860, '94 GB',  77.2, 1),
('2025-10-18 09:00:00', 142, 990, '96 GB',  79.8, 1),
('2025-10-20 09:00:00', 155, 1100,'98 GB',  82.1, 1),
('2025-10-22 09:00:00', 168, 1210,'101 GB', 84.0, 1),
('2025-10-24 09:00:00', 175, 1290,'103 GB', 86.4, 1),
('2025-10-26 09:00:00', 182, 1410,'106 GB', 88.2, 1),
('2025-10-28 09:00:00', 190, 1520,'108 GB', 90.1, 1),
('2025-10-30 09:00:00', 205, 1650,'110 GB', 92.7, 1),
('2025-11-01 09:00:00', 220, 1780,'113 GB', 93.8, 1),
('2025-11-03 09:00:00', 235, 1890,'115 GB', 94.6, 1),
('2025-11-05 09:00:00', 248, 1975,'118 GB', 95.0, 1),
('2025-11-07 09:00:00', 260, 1850,'120 GB', 91.4, 1),
('2025-11-09 09:00:00', 245, 1740,'122 GB', 88.9, 1),
('2025-11-11 09:00:00', 230, 1620,'124 GB', 85.1, 1),
('2025-11-13 09:00:00', 218, 1505,'126 GB', 82.3, 1),
('2025-11-15 09:00:00', 205, 1390,'128 GB', 79.4, 1),
('2025-11-17 09:00:00', 190, 1275,'130 GB', 76.2, 1),
('2025-11-19 09:00:00', 175, 1150,'132 GB', 73.5, 1),
('2025-11-30 09:00:00', 98,  610, '148 GB', 58.2, 1);


INSERT INTO PerformanceMetric (type, unit, measurement, timeStamp, adminID)
VALUES 
('response time', 'ms', 122.4, NOW() - INTERVAL 18 HOUR, 1),
('response time', 'ms', 140.8, NOW() - INTERVAL 22 HOUR, 1),
('query frequency', 'queries/min', 600, NOW() - INTERVAL 10 HOUR, 1),
('query frequency', 'queries/min', 475, NOW() - INTERVAL 14 HOUR, 1),
('query frequency', 'queries/min', 510, NOW() - INTERVAL 20 HOUR, 1),
('cpu', 'percent', 68.9, NOW() - INTERVAL 15 HOUR, 1),
('cpu', 'percent', 75.6, NOW() - INTERVAL 19 HOUR, 1),
('latency', 'ms', 45.2, NOW() - INTERVAL 2 HOUR, 1),
('latency', 'ms', 52.8, NOW() - INTERVAL 6 HOUR, 1),
('latency', 'ms', 38.5, NOW() - INTERVAL 10 HOUR, 1),
('latency', 'ms', 48.9, NOW() - INTERVAL 13 HOUR, 1),
('latency', 'ms', 55.3, NOW() - INTERVAL 17 HOUR, 1),
('latency', 'ms', 42.1, NOW() - INTERVAL 21 HOUR, 1),
('response time', 'ms', 100.00, '2025-10-10 15:41:00', 1),
('query frequency', 'queries/min', 5.00, '2025-10-10 12:31:14', 1),
('response time', 'ms', 200.00, '2025-10-11 15:41:00', 1);

-- NO EXTRA DATA NEEDED
INSERT INTO Backup (size, status, health, datePerformed, adminID)
VALUES (100.00, 'Good', 'Healthy', NULL, 1),
       (50.00, 'Bad', 'Unhealthy', NULL, 1);

-- NO EXTRA DATA NEEDED
INSERT INTO SystemUpdate (updateDate, status, updatedVersion, currentVersion, patchNotes, adminID)
VALUES (NULL, 'Good', NULL, '1.0.0', NULL, 1),
       (NULL, 'BAD', NULL, '0.0.1', NULL, 1);

INSERT INTO Alert (type, severity, message, isResolved, timeStamp, adminID, usageID, backupID, metricID, updateID)
VALUES ('Backup', 'Low', NULL, TRUE, '2025-10-10 15:21:31', 1, NULL, 1, NULL, NULL),
       ('SystemUpdate', 'Low', NULL, TRUE, '2025-10-10 15:22:31', 1, NULL, NULL, NULL, 1);
INSERT INTO Alert
(type, severity, message, isResolved, timeStamp, adminID, usageID, backupID, metricID, updateID)
VALUES
('Backup',        'Low',      'Daily backup completed with minor warnings', TRUE,  '2025-10-15 08:10:00', 1,  3, 1,  2, 1),
('Backup',        'Medium',   'Backup size grew faster than expected',      FALSE, '2025-10-16 09:25:00', 1,  4, 2,  3, NULL),
('SystemUpdate',  'Low',      'New patch available for application stack',  FALSE, '2025-10-17 10:40:00', 1, NULL, NULL, NULL, 2),
('Performance',   'High',     'CPU usage exceeded 85 percent',              FALSE, '2025-10-18 11:15:00', 1,  5, NULL,  5, NULL),
('Database',      'Medium',   'Slow query detected on JobApplication table',TRUE,  '2025-10-19 13:05:00', 1,  6, NULL,  6, NULL),
('Security',      'High',     'Multiple failed login attempts detected',    FALSE, '2025-10-20 14:22:00', 1,  7, NULL, NULL, NULL),
('Performance',   'Low',      'Latency slightly above target threshold',    TRUE,  '2025-10-21 09:45:00', 1,  8, NULL,  7, NULL),
('Database',      'High',     'Lock contention on Student table detected',  FALSE, '2025-10-22 16:10:00', 1,  9, NULL,  8, NULL),
('SystemUpdate',  'Medium',   'Pending restart required to complete update',FALSE, '2025-10-23 07:55:00', 1, NULL, NULL, NULL, 1),
('Performance',   'High',     'Average response time exceeded 150 ms',      FALSE, '2025-11-01 10:10:00', 1, 15, NULL, 13, NULL),
('Database',      'Medium',   'Replica lag above acceptable threshold',     FALSE, '2025-11-02 11:25:00', 1, 16, NULL, 14, NULL),
('Security',      'Medium',   'User session timeout configuration changed', TRUE,  '2025-11-03 12:50:00', 1, NULL, NULL, NULL, NULL),
('Backup',        'Low',      'Incremental backup completed',               TRUE,  '2025-11-04 04:05:00', 1, 17, 1, 15, 1),
('Performance',   'Low',      'CPU usage returned to normal range',         TRUE,  '2025-11-05 09:35:00', 1, 18, NULL, 16, NULL),
('SystemUpdate',  'Medium',   'Application update scheduled for weekend',   FALSE, '2025-11-06 14:00:00', 1, NULL, NULL, NULL, 2),
('Database',      'High',     'Connection pool near maximum capacity',      FALSE, '2025-11-07 15:10:00', 1, 19, NULL, 17, NULL),
('Security',      'Low',      'New admin account created',                  TRUE,  '2025-11-08 16:40:00', 1, NULL, NULL, NULL, NULL),
('Performance',   'Medium',   'Latency variability increased slightly',     FALSE, '2025-11-09 18:05:00', 1, 20, NULL, 18, NULL),
('Backup',        'Medium',   'Old backups approaching retention limit',    FALSE, '2025-11-10 07:55:00', 1, 21, 2, 19, NULL);

INSERT INTO JobPosting (title, roleType, location, department, datePosted, dateClosed, coordinatorID)
VALUES ('Mcdonald flipper', 'Burger Flipper', 'Boston', 'Kitchen', '2025-07-10', NULL, 1),
       ('SWE', 'SWE', 'Seattle', 'AWS', '2020-06-11', NULL, 2);

INSERT INTO JobPosting (title, roleType, location, department, datePosted, dateClosed, coordinatorID) VALUES
('Business Systems Development Analyst', 'VP Product Management', 'Yashiro', 'Marketing', '2024-10-07', '8/31/2025', 1),
('Financial Analyst', 'Chief Design Engineer', 'Gorelki', 'Support', '2025-11-14', '6/30/2025', 2),
('Computer Systems Analyst IV', 'Product Engineer', 'São Vicente de Ferreira', 'Training', '2024-10-19', '8/20/2025', 3),
('Database Administrator II', 'Teacher', 'Gourcy', 'Marketing', '2024-11-11', '7/17/2025', 4),
('Help Desk Technician', 'Payment Adjustment Coordinator', 'Anta', 'Research and Development', '2024-11-17', '3/29/2025', 5),
('Electrical Engineer', 'Legal Assistant', 'Pomacocha', 'Business Development', '2024-11-10', '5/20/2025', 1),
('Administrative Officer', 'Computer Systems Analyst IV', 'San Carlos', 'Accounting', '2025-06-03', '8/7/2025', 2),
('Account Executive', 'Nuclear Power Engineer', 'Itapeva', 'Engineering', '2025-08-02', '3/2/2025', 3),
('Administrative Officer', 'VP Product Management', 'Cipaku', 'Research and Development', '2025-12-04', '5/9/2025', 4),
('Geological Engineer', 'Financial Advisor', 'Biyan', 'Sales', '2024-10-28', '2/9/2025', 5),
('Senior Sales Associate', 'Programmer II', 'Duekoué', 'Engineering', '2025-06-17', '8/27/2025', 1),
('Marketing Manager', 'VP Product Management', 'Opočno', 'Engineering', '2025-09-26', '9/28/2025', 2),
('Safety Technician IV', 'Cost Accountant', 'Losevo', 'Services', '2025-05-29', '3/17/2025', 3),
('Civil Engineer', 'Software Engineer III', 'Ikhtiman', 'Sales', '2025-05-02', '3/31/2025', 4),
('Senior Editor', 'Web Developer I', 'Nchelenge', 'Product Management', '2025-11-05', '8/11/2025', 5),
('Junior Executive', 'Quality Engineer', 'Yabēlo', 'Support', '2025-11-27', '11/27/2025', 1),
('Statistician II', 'Executive Secretary', 'Rýmařov', 'Legal', '2024-12-26', '7/2/2025', 2),
('Health Coach I', 'Media Manager II', 'Badeggi', 'Accounting', '2025-02-18', '8/19/2025', 3),
('Account Coordinator', 'Director of Sales', 'Shiqiao', 'Research and Development', '2025-06-02', '3/3/2025', 4),
('Recruiting Manager', 'Staff Accountant III', 'Parreira', 'Research and Development', '2025-08-20', '6/20/2025', 5),
('Project Manager', 'Assistant Manager', 'Lesozavodsk', 'Services', '2025-04-01', '10/10/2025', 1),
('Account Coordinator', 'Account Executive', 'Guohe', 'Human Resources', '2025-06-08', '4/28/2025', 2),
('Environmental Tech', 'Technical Writer', 'Khanabad', 'Sales', '2024-10-15', '9/8/2025', 3),
('Analyst Programmer', 'Actuary', 'Concepción Tutuapa', 'Human Resources', '2025-03-19', '2/4/2025', 4),
('Senior Cost Accountant', 'Quality Engineer', 'Batanovtsi', 'Business Development', '2025-03-25', '10/5/2025', 5),
('Statistician II', 'Help Desk Technician', 'Papringan', 'Support', '2025-05-05', '9/1/2025', 1),
('Mechanical Systems Engineer', 'Cost Accountant', 'San Felipe', 'Research and Development', '2025-06-09', '2/8/2025', 2),
('Social Worker', 'Programmer Analyst III', 'Wulan Haye', 'Services', '2025-07-23', '9/3/2025', 3),
('Mechanical Systems Engineer', 'Civil Engineer', 'Khilok', 'Research and Development', '2025-05-22', '6/20/2025', 4),
('Account Coordinator', 'Teacher', 'Mayisad', 'Marketing', '2025-07-28', '3/31/2025', 5),
('Automation Specialist IV', 'VP Accounting', 'Pawa', 'Research and Development', '2025-10-08', '12/3/2025', 1),
('VP Accounting', 'Executive Secretary', 'Svojat', 'Business Development', '2025-09-05', '6/22/2025', 2),
('Graphic Designer', 'Chief Design Engineer', 'Jingyang', 'Marketing', '2025-04-16', '6/29/2025', 3),
('Research Assistant I', 'Paralegal', 'Dzoraghbyur', 'Marketing', '2025-09-23', '5/23/2025', 4),
('Registered Nurse', 'Sales Representative', 'Bosilovo', 'Support', '2025-11-02', '9/29/2025', 5),
('Quality Control Specialist', 'Desktop Support Technician', 'Avallon', 'Support', '2025-06-30', '8/23/2025', 1),
('Project Manager', 'Nurse Practicioner', 'Fengyang', 'Marketing', '2025-03-29', '8/1/2025', 2),
('Business Systems Development Analyst', 'Help Desk Technician', 'Weiwangzhuang', 'Training', '2025-08-13', '7/30/2025', 3),
('Registered Nurse', 'Account Representative I', 'Blois', 'Sales', '2024-10-13', '5/14/2025', 4),
('Developer IV', 'Recruiter', 'Bang Kaeo', 'Services', '2025-11-21', '1/16/2025', 5);


INSERT INTO StudentProgressMetrics (progressID, studentID, lastActivityDate, offersReceived, interviewsScheduled, numJobApplied)
VALUES (155551, 1, '2024-06-10', 0, 0, 0),
       (155552, 2, '2025-06-10', 1, 1, 1);

INSERT INTO StudentProgressMetrics 
(progressID, studentID, lastActivityDate, offersReceived, interviewsScheduled, numJobApplied)
VALUES
(300001, 1,  '2024-03-12', 0, 1, 12),
(300002, 2,  '2024-04-02', 1, 2, 18),
(300003, 3,  '2024-04-18', 0, 0, 5),
(300004, 4,  '2024-05-01', 2, 3, 24),
(300005, 5,  '2024-05-22', 1, 1, 14),
(300006, 6,  '2024-06-10', 0, 2, 19),
(300007, 7,  '2024-06-28', 3, 6, 41),
(300008, 8,  '2024-07-15', 0, 1, 9),
(300009, 9,  '2024-08-03', 1, 2, 17),
(300010, 10, '2024-08-21', 0, 0, 6),
(300011, 11, '2024-09-10', 2, 4, 29),
(300012, 12, '2024-09-29', 1, 3, 22),
(300013, 13, '2024-10-15', 0, 1, 13),
(300014, 14, '2024-11-05', 2, 5, 34),
(300015, 15, '2024-11-28', 1, 2, 21),
(300016, 16, '2024-12-18', 0, 0, 8),
(300017, 17, '2025-01-10', 3, 7, 48),
(300018, 18, '2025-01-25', 1, 3, 26),
(300019, 19, '2025-02-12', 0, 1, 15),
(300020, 20, '2025-02-28', 2, 4, 33),
(300021, 21, '2025-03-14', 1, 2, 20),
(300022, 22, '2025-03-29', 0, 0, 11),
(300023, 23, '2025-04-11', 3, 8, 55),
(300024, 24, '2025-04-26', 1, 2, 23),
(300025, 25, '2025-05-10', 0, 1, 16),
(300026, 26, '2025-05-25', 2, 5, 37),
(300027, 27, '2025-06-08', 1, 3, 28),
(300028, 28, '2025-06-21', 0, 0, 9),
(300029, 29, '2025-07-06', 3, 6, 49),
(300030, 30, '2025-07-19', 1, 2, 24),
(300031, 31, '2025-08-02', 2, 4, 35),
(300032, 32, '2025-08-17', 0, 1, 14),
(300033, 33, '2025-09-01', 1, 3, 27),
(300034, 34, '2025-09-16', 0, 0, 10),
(300035, 35, '2025-10-02', 3, 7, 52),
(300036, 36, '2025-10-18', 1, 2, 25),
(300037, 37, '2025-11-03', 0, 1, 18),
(300038, 38, '2025-11-16', 2, 4, 36),
(300039, 39, '2025-12-01', 1, 3, 31),
(300040, 40, '2025-12-15', 0, 0, 7);


INSERT INTO JobListing (listingID, postingID, listingStatus, datePublished, expiresOn, 
                        lastChecked, postingURL, platformID)
VALUES (166661, 1, 'Up', '2024-06-10', NULL, NULL, 'https://www.linkedin.com/jobs/123', 1),
       (166662, 2, 'Down', '2024-06-10', '2024-06-10', NULL, 
        'https://northeastern.com/students/jobs/321', 2);

INSERT INTO JobListing 
(listingID, postingID, listingStatus, datePublished, expiresOn, lastChecked, postingURL, platformID)
VALUES
(200000, 1,  'Active',  '2024-02-14', '2025-02-14', '2025-03-01 10:15:00', 'https://jobs.example.com/200000', 1),
(200001, 2,  'Expired', '2024-05-20', '2025-01-10', '2025-02-18 09:30:00', 'https://jobs.example.com/200001', 2),
(200002, 3,  'Paused',  '2024-06-01', NULL,         '2025-04-04 14:22:00', 'https://jobs.example.com/200002', 3),
(200003, 4,  'Active',  '2024-08-11', '2025-08-11', '2025-05-01 16:50:00', 'https://jobs.example.com/200003', 4),
(200004, 5,  'Expired', '2024-01-09', '2024-12-30', '2025-01-15 08:40:00', 'https://jobs.example.com/200004', 5),
(200005, 6,  'Active',  '2024-03-18', NULL,         '2025-06-02 13:05:00', 'https://jobs.example.com/200005', 1),
(200006, 7,  'Paused',  '2024-09-07', '2025-09-07', '2025-07-20 11:45:00', 'https://jobs.example.com/200006', 2),
(200007, 8,  'Active',  '2024-10-02', '2025-10-01', '2025-08-01 09:10:00', 'https://jobs.example.com/200007', 3),
(200008, 9,  'Expired', '2024-04-25', '2025-02-01', '2025-02-02 17:00:00', 'https://jobs.example.com/200008', 4),
(200009, 10, 'Active',  '2025-01-12', NULL,         '2025-09-01 12:00:00', 'https://jobs.example.com/200009', 5),
(200010, 11, 'Paused',  '2024-06-10', '2025-06-10', '2025-05-30 10:33:00', 'https://jobs.example.com/200010', 1),
(200011, 12, 'Expired', '2024-02-04', '2024-11-20', '2025-01-05 09:00:00', 'https://jobs.example.com/200011', 2),
(200012, 13, 'Active',  '2024-11-15', NULL,         '2025-10-11 14:10:00', 'https://jobs.example.com/200012', 3),
(200013, 14, 'Expired', '2024-07-19', '2025-03-18', '2025-04-01 11:55:00', 'https://jobs.example.com/200013', 4),
(200014, 15, 'Paused',  '2024-12-01', '2025-12-01', '2025-11-20 16:40:00', 'https://jobs.example.com/200014', 5),
(200015, 16, 'Active',  '2025-02-01', NULL,         '2025-09-10 08:30:00', 'https://jobs.example.com/200015', 1),
(200016, 17, 'Expired', '2024-03-30', '2024-10-01', '2025-01-02 10:00:00', 'https://jobs.example.com/200016', 2),
(200017, 18, 'Paused',  '2024-05-05', '2025-05-05', '2025-06-01 12:20:00', 'https://jobs.example.com/200017', 3),
(200018, 19, 'Active',  '2024-09-22', NULL,         '2025-07-14 14:00:00', 'https://jobs.example.com/200018', 4),
(200019, 20, 'Expired', '2024-01-30', '2024-12-15', '2025-01-10 09:40:00', 'https://jobs.example.com/200019', 5),
(200020, 21, 'Active',  '2025-03-10', NULL,         '2025-09-18 15:12:00', 'https://jobs.example.com/200020', 1),
(200021, 22, 'Paused',  '2024-08-28', '2025-08-28', '2025-06-10 10:01:00', 'https://jobs.example.com/200021', 2),
(200022, 23, 'Expired', '2024-02-12', '2024-09-01', '2025-01-03 11:50:00', 'https://jobs.example.com/200022', 3),
(200023, 24, 'Active',  '2024-10-16', NULL,         '2025-08-08 13:00:00', 'https://jobs.example.com/200023', 4),
(200024, 25, 'Paused',  '2024-11-08', '2025-11-08', '2025-09-15 14:30:00', 'https://jobs.example.com/200024', 5),
(200025, 26, 'Active',  '2024-04-01', NULL,         '2025-06-22 12:45:00', 'https://jobs.example.com/200025', 1),
(200026, 27, 'Expired', '2024-06-18', '2025-01-15', '2025-02-05 10:30:00', 'https://jobs.example.com/200026', 2),
(200027, 28, 'Paused',  '2024-07-11', '2025-07-11', '2025-07-03 11:10:00', 'https://jobs.example.com/200027', 3),
(200028, 29, 'Active',  '2024-09-14', NULL,         '2025-08-22 16:20:00', 'https://jobs.example.com/200028', 4),
(200029, 30, 'Expired', '2024-03-06', '2024-11-01', '2025-01-20 09:05:00', 'https://jobs.example.com/200029', 5);


-- NO EXTRA DATA NEEDED
INSERT INTO Report (generatedDate, summary, coachID)
VALUES ('2024-06-10', 'I did not listen', 1),
       ('2025-06-10', 'Good guy', 2);

-- NO EXTRA DATA NEEDED
INSERT INTO ReportItem (itemID, reportID, studentID, recommendations, notes, keyFindings)
VALUES (188881, 1, 1, 'idk', 'none', 'none'),
       (188882, 2, 2, 'Apply to more', 'applied to little', 'needs to apply to more');

-- NO EXTRA DATA NEEDED
INSERT INTO coachSPM (coachID, progressID, studentID)
VALUES (1, 155551, 1),
       (2, 155552, 2);

INSERT INTO Resume (resumeID, studentID, imageURl, label)
VALUES (199991, 1, 'imageurl.com', 'Final Resume'),
       (199992, 2, 'word.com', 'Updated Resume'),
       (199993, 1, '/docs/resumes/student_888881.pdf', 'Software Engineer Focused');

INSERT INTO JobApplication (companyName, position, stage, dateApplied, lastUpdated, 
                            studentID, listingID, postingID, resumeID)
VALUES ('McDonald''s', 'burger flipper', 'applied', '2024-10-10', '2024-10-10', 
        1, 166661, 1, 199991),
       ('Amazon', 'SWE', 'Rejected', '2024-10-11', '2024-10-11', 
        2, 166662, 2, 199992);

INSERT INTO JobApplication 
    (companyName, position, stage, dateApplied, lastUpdated, jobBoard, 
     studentID, listingID, postingID, resumeID)
VALUES
('Amazon',       'Software Engineer Intern',      'Applied',      '2024-01-15', '2024-01-16 10:15:00', 'LinkedIn',     1, 200000,  1, 199991),
('Google',       'Backend Developer Intern',      'Interviewing', '2024-02-02', '2024-02-10 14:30:00', 'Handshake',    1, 200001,  2, 199991),
('Microsoft',    'Cloud Engineer Intern',         'Rejected',     '2024-02-20', '2024-03-01 09:05:00', 'LinkedIn',     1, 200002,  3, 199991),
('Meta',         'Full Stack Engineer Intern',    'Applied',      '2024-03-05', '2024-03-07 11:45:00', 'NUworks',      1, 200003,  4, 199991),
('Netflix',      'Data Engineer Intern',          'Ghosted',      '2024-03-18', '2024-04-01 16:20:00', 'Indeed',       1, 200004,  5, 199991),
('Stripe',       'Payments Engineer Co-op',       'Interviewing', '2024-04-02', '2024-04-12 13:10:00', 'LinkedIn',     1, 200005,  6, 199991),
('HubSpot',      'Software Engineer Co-op',       'Applied',      '2024-04-15', '2024-04-17 15:00:00', 'NUworks',      1, 200006,  7, 199991),
('Wayfair',      'Platform Engineer Intern',      'Rejected',     '2024-04-29', '2024-05-10 10:40:00', 'Handshake',    1, 200007,  8, 199991),
('Datadog',      'Monitoring Engineer Intern',    'Applied',      '2024-05-07', '2024-05-08 09:55:00', 'LinkedIn',     1, 200008,  9, 199991),
('Snowflake',    'Data Platform Engineer Intern', 'Interviewing', '2024-05-20', '2024-05-28 14:05:00', 'Company Site', 1, 200009, 10, 199991),
('Goldman Sachs','Quant Analyst Intern',          'Applied',      '2024-06-01', '2024-06-03 11:30:00', 'Handshake',    1, 200010, 11, 199993),
('JPMorgan',     'Technology Analyst Intern',     'Interviewing', '2024-06-10', '2024-06-20 15:45:00', 'LinkedIn',     1, 200011, 12, 199993),
('Morgan Stanley','DevOps Intern',                'Rejected',     '2024-06-22', '2024-07-02 10:10:00', 'Indeed',       1, 200012, 13, 199993),
('Citadel',      'Software Engineer Intern',      'Applied',      '2024-07-05', '2024-07-06 09:20:00', 'Company Site', 1, 200013, 14, 199993),
('Two Sigma',    'Platform Engineer Intern',      'Interviewing', '2024-07-18', '2024-07-25 13:55:00', 'LinkedIn',     1, 200014, 15, 199993),
('Jane Street',  'Software Dev Intern',           'Rejected',     '2024-08-01', '2024-08-12 16:40:00', 'Handshake',    1, 200015, 16, 199993),
('Robinhood',    'Backend Engineer Intern',       'Ghosted',      '2024-08-11', '2024-08-30 10:05:00', 'Indeed',       1, 200016, 17, 199993),
('Fidelity',     'Full Stack Co-op',             'Interviewing', '2024-08-25', '2024-09-05 14:25:00', 'NUworks',      1, 200017, 18, 199993),
('State Street', 'Technology Intern',             'Applied',      '2024-09-07', '2024-09-08 09:50:00', 'LinkedIn',     1, 200018, 19, 199993),
('Dell',         'Software Engineer Intern',      'Rejected',     '2024-09-19', '2024-09-29 17:00:00', 'Company Site', 1, 200019, 20, 199993),
('Apple',        'iOS Engineer Intern',           'Applied',      '2024-10-02', '2024-10-04 12:15:00', 'LinkedIn',     1, 200020, 21, 199991),
('Tesla',        'Autopilot Engineer Intern',     'Interviewing', '2024-10-15', '2024-10-25 11:00:00', 'Company Site', 1, 200021, 22, 199993),
('NVIDIA',       'GPU Software Intern',           'Offer',        '2024-10-28', '2024-11-05 15:30:00', 'LinkedIn',     1, 200022, 23, 199991),
('AMD',          'Driver Engineer Intern',        'Applied',      '2024-11-05', '2024-11-06 09:25:00', 'Handshake',    1, 200023, 24, 199993),
('Intel',        'Systems Software Intern',       'Rejected',     '2024-11-18', '2024-11-28 14:50:00', 'Indeed',       1, 200024, 25, 199991),
('Palantir',     'Forward Deployed Engineer Int', 'Applied',      '2024-12-01', '2024-12-03 10:35:00', 'LinkedIn',     1, 200025, 26, 199993),
('Snowflake',    'Data Engineer Intern',          'Interviewing', '2024-12-15', '2024-12-22 13:40:00', 'Company Site', 1, 200026, 27, 199991),
('Twilio',       'Platform Engineer Intern',      'Ghosted',      '2025-01-05', '2025-01-20 09:00:00', 'LinkedIn',     1, 200027, 28, 199993),
('Atlassian',    'Cloud Engineer Intern',         'Applied',      '2025-01-18', '2025-01-19 11:10:00', 'Handshake',    1, 200028, 29, 199991),
('Shopify',      'Backend Developer Intern',      'Interviewing', '2025-02-02', '2025-02-10 16:00:00', 'Company Site', 1, 200029, 30, 199993),
('Stripe',       'Software Engineer Intern',      'Applied',      '2025-02-15', '2025-02-16 09:30:00', 'LinkedIn',     1, 200000,  1, 199991),
('Google',       'Site Reliability Intern',       'Interviewing', '2025-02-27', '2025-03-05 14:45:00', 'NUworks',      1, 200001,  2, 199993),
('Meta',         'Security Engineer Intern',      'Rejected',     '2025-03-10', '2025-03-20 10:05:00', 'LinkedIn',     1, 200002,  3, 199991),
('Amazon',       'SDE Intern',                    'Applied',      '2025-03-22', '2025-03-23 11:55:00', 'Handshake',    1, 200003,  4, 199993),
('Microsoft',    'Data Engineer Intern',          'Ghosted',      '2025-04-01', '2025-04-18 15:20:00', 'Indeed',       1, 200004,  5, 199991),
('Uber',         'Maps Engineer Intern',          'Applied',      '2025-04-15', '2025-04-16 13:30:00', 'Company Site', 1, 200005,  6, 199993),
('Lyft',         'Backend Services Intern',       'Interviewing', '2025-04-28', '2025-05-05 10:40:00', 'LinkedIn',     1, 200006,  7, 199991),
('DoorDash',     'Logistics Engineer Intern',     'Rejected',     '2025-05-10', '2025-05-20 09:15:00', 'Handshake',    1, 200007,  8, 199993),
('OpenAI',       'Research Engineer Intern',      'Applied',      '2025-05-23', '2025-05-24 12:05:00', 'Company Site', 1, 200008,  9, 199991),
('Canva',        'Frontend Engineer Intern',      'Interviewing', '2025-06-01', '2025-06-08 14:50:00', 'LinkedIn',     1, 200009, 10, 199993),
('KPMG',         'Technology Consultant Intern',  'Applied',      '2024-03-01', '2024-03-03 10:10:00', 'Handshake',    2, 200010, 11, 199992),
('Deloitte',     'Risk Advisory Intern',          'Interviewing', '2024-03-18', '2024-03-25 15:35:00', 'LinkedIn',     2, 200011, 12, 199992),
('PwC',          'Tech Consulting Intern',        'Applied',      '2024-04-01', '2024-04-02 09:40:00', 'Company Site', 2, 200012, 13, 199992),
('EY',           'Technology Risk Intern',        'Rejected',     '2024-04-15', '2024-04-26 11:25:00', 'LinkedIn',     2, 200013, 14, 199992),
('McKinsey',     'Business Analyst Intern',       'Applied',      '2024-05-01', '2024-05-03 13:15:00', 'Company Site', 2, 200014, 15, 199992),
('BCG',          'Consulting Intern',             'Interviewing', '2024-05-18', '2024-05-28 14:55:00', 'LinkedIn',     2, 200015, 16, 199992),
('Bain',         'Associate Consultant Intern',   'Ghosted',      '2024-06-02', '2024-06-20 16:30:00', 'Handshake',    2, 200016, 17, 199992),
('Salesforce',   'Solution Engineer Intern',      'Applied',      '2024-06-20', '2024-06-21 09:05:00', 'Indeed',       2, 200017, 18, 199992),
('ServiceNow',   'Platform Engineer Intern',      'Rejected',     '2024-07-04', '2024-07-14 11:45:00', 'LinkedIn',     2, 200018, 19, 199992),
('SAP',          'Technical Consultant Intern',   'Applied',      '2024-07-18', '2024-07-19 10:30:00', 'Company Site', 2, 200019, 20, 199992),
('Oracle',       'Cloud Consultant Intern',       'Interviewing', '2024-08-01', '2024-08-10 15:20:00', 'LinkedIn',     2, 200020, 21, 199992),
('IBM',          'Technology Consultant Intern',  'Applied',      '2024-08-16', '2024-08-18 09:50:00', 'Handshake',    2, 200021, 22, 199992),
('Zendesk',      'Support Engineer Intern',       'Rejected',     '2024-09-01', '2024-09-12 12:40:00', 'Indeed',       2, 200022, 23, 199992),
('Slack',        'Developer Relations Intern',    'Applied',      '2024-09-18', '2024-09-20 14:00:00', 'LinkedIn',     2, 200023, 24, 199992),
('Notion',       'Product Engineer Intern',       'Interviewing', '2024-10-01', '2024-10-09 16:10:00', 'Company Site', 2, 200024, 25, 199992);


INSERT INTO Notification (type, dateTimeSent, coachID, studentID, applicationID, 
                          coordinatorID, listingID, postingID)
VALUES ('Job application', '2024-10-10 15:41:00', 1, 1, 1, NULL, 166661, 1),
       ('Message', '2024-10-11 15:41:00', 2, 2, NULL, NULL, NULL, NULL),
       ('Message', '2024-10-11 15:41:01', NULL, 2, NULL, NULL, NULL, NULL);

INSERT INTO Notification 
(type, isRead, dateTimeSent, coachID, studentID, applicationID, coordinatorID, listingID, postingID)
VALUES
('Job application', FALSE, '2025-07-02 09:15:00', 1, 1, 3,  1, 200000, 1),
('Job application', FALSE, '2025-07-03 10:20:00', 1, 1, 4,  2, 200001, 2),
('Job application', TRUE,  '2025-07-05 14:05:00', 1, 1, 5,  3, 200002, 3),
('Job application', FALSE, '2025-07-08 11:45:00', 1, 1, 6,  4, 200003, 4),
('Job application', FALSE, '2025-07-10 16:30:00',1, 1, 7,  5, 200004, 5),
('Status Update',  FALSE, '2025-07-12 09:00:00', 1, 1, 8,  NULL, 200005, 6),
('Status Update',  TRUE,  '2025-07-14 13:25:00', 1, 1, 9,  NULL, 200006, 7),
('Job application',FALSE, '2025-07-16 15:10:00',1, 1, 10, 6, 200007, 8),
('Job application',TRUE,  '2025-07-18 10:50:00',1, 1, 11, 7, 200008, 9),
('Status Update',  FALSE, '2025-07-20 17:05:00',1, 1, 12, 8, 200009,10),
('Expiring Listing Alert', FALSE, '2025-07-22 08:35:00', 1, 1, 13, NULL, 200004, 5),
('Expiring Listing Alert', FALSE, '2025-07-23 09:10:00', 1, 1, 14, NULL, 200008, 9),
('Status Update',          TRUE,  '2025-07-25 12:40:00',1, 1, 15,  9, 200010,11),
('Job application',        FALSE, '2025-07-27 15:55:00',1, 1, 16, 10, 200011,12),
('Message',                FALSE, '2025-07-29 18:10:00',1, 1, NULL, NULL, NULL, NULL),
('Message',                FALSE, '2025-08-01 09:20:00',1, 1, NULL, NULL, NULL, NULL),
('Job application',        TRUE,  '2025-08-02 11:05:00',1, 1, 17, 11, 200012,13),
('Status Update',          FALSE, '2025-08-03 13:45:00',1, 1, 18, 12, 200013,14),
('Job application',        FALSE, '2025-08-05 16:25:00',1, 1, 19, 13, 200014,15),
('Expiring Listing Alert', TRUE,  '2025-08-07 08:55:00',1, 1, 20, NULL, 200015,16),
('Job application',        FALSE, '2025-08-10 10:15:00',1, 1, 21, 14, 200016,17),
('Status Update',          FALSE, '2025-08-12 12:35:00',1, 1, 22, 15, 200017,18),
('Job application',        TRUE,  '2025-08-15 14:40:00',1, 1, 23, 16, 200018,19),
('Message',                FALSE, '2025-08-17 18:05:00',1, 1, NULL, NULL, NULL, NULL),
('Expiring Listing Alert', FALSE, '2025-08-20 09:50:00',1, 1, 24, NULL, 200019,20),
('Status Update',          TRUE,  '2025-08-22 11:15:00',1, 1, 25, 17, 200020,21),
('Job application',        FALSE, '2025-08-25 13:30:00',1, 1, 26, 18, 200021,22),
('Job application',        FALSE, '2025-08-28 16:00:00',1, 1, 27, 19, 200022,23),
('Message',                FALSE, '2025-08-30 19:10:00',1, 1, NULL, NULL, NULL, NULL),
('Expiring Listing Alert', TRUE,  '2025-09-02 08:45:00',1, 1, 28, NULL, 200023,24),
('Job application',        FALSE, '2025-09-04 09:25:00',1, 2, 29, 20, 200024,25),
('Status Update',          FALSE, '2025-09-06 11:40:00',1, 2, 30, 21, 200025,26),
('Message',                TRUE,  '2025-09-08 14:05:00',1, 2, NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-09-10 16:50:00',1, 2, 31, 22, 200026,27),
('Expiring Listing Alert', FALSE, '2025-09-12 18:20:00',1, 2, 32, NULL, 200027,28),
('Job application',        FALSE, '2025-09-15 09:30:00',1, 3, 33, 23, 200028,29),
('Status Update',          TRUE,  '2025-09-17 11:55:00',1, 3, 34, 24, 200029,30),
('Message',                FALSE, '2025-09-19 13:40:00',1, 3, NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-09-21 15:10:00',1, 4, 35, 25, 200000,1),
('Expiring Listing Alert', FALSE, '2025-09-23 17:25:00',1, 4, 36, NULL, 166661,1),
('Job application',        FALSE, '2025-09-25 09:05:00', 2, 5,  37, 5, 200001,2),
('Status Update',          TRUE,  '2025-09-27 10:45:00', 2, 5,  38, 6, 200002,3),
('Message',                FALSE, '2025-09-29 12:30:00', 2, 5,  NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-10-01 14:20:00', 3, 6,  39, 7, 200003,4),
('Expiring Listing Alert', FALSE, '2025-10-02 18:00:00', 3, 6,  40, NULL, 166662,2),
('Job application',        FALSE, '2025-10-04 09:40:00', 4, 7,  41, 8, 200004,5),
('Status Update',          TRUE,  '2025-10-06 11:20:00', 4, 7,  42, 9, 200005,6),
('Message',                FALSE, '2025-10-08 13:55:00', 4, 7,  NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-10-10 16:35:00', 5, 8,  43,10, 200006,7),
('Expiring Listing Alert', FALSE, '2025-10-12 19:05:00', 5, 8,  44, NULL, 200007,8),
('Job application',        FALSE, '2025-10-14 08:55:00', 6, 9,  45,11, 200008,9),
('Status Update',          TRUE,  '2025-10-16 10:30:00', 6, 9,  46,12, 200009,10),
('Message',                FALSE, '2025-10-18 12:10:00', 6, 9,  NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-10-20 14:45:00', 7,10,  47,13, 200010,11),
('Expiring Listing Alert', FALSE, '2025-10-22 17:15:00', 7,10,  48, NULL, 200011,12), 
('Job application',        FALSE, '2025-11-01 09:05:00', 1, 1, 49, 14, 200012,13),
('Status Update',          FALSE, '2025-11-03 11:25:00', 1, 2, 50, 15, 200013,14),
('Message',                FALSE, '2025-11-05 13:40:00', 1, 1, NULL, NULL, NULL, NULL),
('Job application',        TRUE,  '2025-11-07 15:55:00', 2, 3, 51, 16, 200014,15),
('Expiring Listing Alert', FALSE, '2025-11-09 18:20:00', 1, 1, 52, NULL, 200015,16), 
('Job application',        FALSE, '2025-11-12 09:30:00', 1, 1, 30, 17, 200016,17),
('Status Update',          TRUE,  '2025-11-15 11:10:00', 3, 4, 12, 18, 200017,18),
('Message',                FALSE, '2025-11-18 14:00:00', 1, 2, NULL, NULL, NULL, NULL),
('Job application',        FALSE, '2025-11-20 16:35:00', 1, 1, 22, 19, 200018,19),
('Status Update',          FALSE, '2025-11-25 19:05:00', 1, 1, 27, 20, 200019,20);


INSERT INTO Message (content, dateTimeSent, studentID, coachID, notificationID)
VALUES ('coach is right', '2024-10-11 15:41:00', 2, 2, 2),
       ('hello', '2024-10-11 15:41:01', 2, 2, 3);

INSERT INTO Message (content, dateTimeSent, studentID, coachID, notificationID)
VALUES
('Hey James, how is your search going?',        '2025-07-02 09:20:00', 1, 1, 4),
('Remember to log your latest applications.',   '2025-07-02 09:25:00', 1, 1, 4),
('Nice work applying to Amazon and Google.',    '2025-07-03 10:30:00', 1, 1, 5),
('Let''s talk about your upcoming interview.',  '2025-07-03 10:45:00', 1, 1, 5),
('Please update your application list tonight.', '2025-07-05 14:10:00',1, 1, 6),
('Congrats on getting an interview at Stripe!', '2025-07-08 11:50:00', 1, 1, 7),
('How do you feel about the interview prep?',   '2025-07-08 12:05:00', 1, 1, 7),
('Try adding a STAR story for each project.',   '2025-07-10 16:35:00', 1, 1, 8),
('Send me your updated resume when you can.',   '2025-07-10 16:50:00', 1, 1, 8),
('I left comments on your resume draft.',       '2025-07-12 09:05:00', 1, 1, 9),
('Let''s schedule a quick check-in next week.', '2025-07-12 09:15:00', 1, 1, 9),
('Nice progress on interviews this month.',     '2025-07-14 13:30:00', 1, 1,10),
('Don''t forget to send thank-you emails.',     '2025-07-14 13:45:00', 1, 1,10),
('Any updates from NVIDIA or Meta yet?',        '2025-07-16 15:15:00', 1, 1,11),
('You''re doing great, keep applying steadily.', '2025-07-16 15:25:00',1, 1,11),
('Try to set a goal of 5 apps per week.',       '2025-07-18 10:55:00', 1, 1,12),
('How did the Datadog interview feel?',         '2025-07-18 11:10:00', 1, 1,12),
('Remember to track rejections too.',           '2025-07-20 17:10:00', 1, 1,13),
('Rejections are data, not judgement.',         '2025-07-20 17:25:00', 1, 1,13),
('Can you share the job description for NVIDIA?','2025-07-22 08:40:00',1, 1,14),
('I like how you framed your project impact.',  '2025-07-22 08:55:00', 1, 1,14),
('Let''s refine your answer to "Tell me about yourself."', '2025-07-23 09:15:00', 1, 1,15),
('Try practicing with a friend tonight.',       '2025-07-23 09:30:00', 1, 1,15),
('Ping me if you get an offer update.',         '2025-07-25 12:45:00', 1, 1,16),
('You''re very close to landing something good.', '2025-07-25 12:55:00',1, 1,16), 
('Hi Alice, how is your consulting search going?', '2025-09-04 09:35:00', 2, 1,27),
('Try adding more metrics to your resume bullets.', '2025-09-04 09:50:00', 2, 1,27),
('Great job applying to KPMG and Deloitte.',       '2025-09-06 11:45:00', 2, 1,28),
('Have you heard back from McKinsey yet?',         '2025-09-06 11:55:00', 2, 1,28),
('Please update NUworks after each new app.',      '2025-09-08 14:10:00', 2, 1,29),
('Let''s schedule a mock case interview.',         '2025-09-10 16:55:00', 2, 1,30),
('I can send you a case prep guide.',              '2025-09-10 17:05:00', 2, 1,30),
('Nice progress on your cover letter.',            '2025-09-12 18:25:00', 2, 1,31),
('Don''t forget to tailor each cover letter.',     '2025-09-12 18:35:00', 2, 1,31),
('You''re building a really strong profile.',      '2025-09-15 09:40:00', 2, 1,32), 
('Hi, I noticed you haven''t logged activity recently.', '2025-09-15 09:55:00', 3, 1,33),
('Can you add your latest applications today?',          '2025-09-17 12:00:00', 3, 1,34),
('Let''s talk about broadening your search a bit.',      '2025-09-19 13:45:00', 4, 1,35),
('Try applying to a mix of big and mid-sized firms.',    '2025-09-19 14:00:00', 4, 1,35),
('I recommend setting weekly goals for applications.',   '2025-09-21 15:15:00', 5, 1,36), 
('Nice work attending the career fair.',                 '2025-09-23 17:30:00', 5, 1,36),
('Did you get any recruiter contact info?',             '2025-09-25 09:10:00', 6, 1,37),
('Please log those conversations in the app.',          '2025-09-25 09:20:00', 6, 1,37),
('Your interview pipeline looks much better now.',      '2025-09-27 10:50:00', 7, 1,38),
('We can focus on negotiation skills next.',            '2025-09-27 11:05:00', 7, 1,38), 
('This looks like a good fit for your skills.',         '2025-10-04 09:45:00', 8, 2, 41),
('Be sure to research the company culture.',            '2025-10-04 09:55:00', 8, 2, 41),
('I liked the way you answered the behavioral questions.','2025-10-06 11:25:00',9, 3, 42),
('Keep practicing the technical portion.',              '2025-10-06 11:35:00', 9, 3, 42),
('Let''s debrief after your next round.',               '2025-10-08 14:00:00',10, 4, 43), 
('Thanks for sending your updated resume.',             '2025-10-08 14:10:00',10, 4, 43),
('I just pushed a new set of recommendations for you.', '2025-10-10 16:40:00',11, 5, 44),
('Check the dashboard for your latest progress metrics.','2025-10-10 16:55:00',11, 5, 44),
('You''re making steady progress—keep going!',          '2025-10-12 19:10:00',12, 6, 45),
('We can revise your strategy if you don''t hear back soon.','2025-10-12 19:20:00',12, 6, 45);


INSERT INTO Audit (summary, tableName, action, timeStamp, recordID, adminID, studentID, coordinatorID, coachID)
VALUES ('Good', 'Student', 'Applied Job', '2025-10-10 15:41:31', 0, 1, 1, NULL, NULL),
       ('Good activity', 'Coach', 'Helping Student', '2025-10-10 16:31:41', 1, 1, NULL, NULL, 1);

INSERT INTO Audit
(summary, tableName, action, timeStamp, recordID,
 adminID, studentID, coordinatorID, coachID)
VALUES
('Student created via onboarding flow',        'Student',       'INSERT', '2025-10-01 09:05:00',  101, 1,  1,  NULL,  1),
('Student profile updated status field',       'Student',       'UPDATE', '2025-10-01 09:15:00',  102, 1,  2,  NULL,  2),
('New job posting added by coordinator',       'JobPosting',    'INSERT', '2025-10-01 10:20:00',  201, 1, NULL,  5,   NULL),
('Job posting status set to closed',           'JobPosting',    'UPDATE', '2025-10-01 11:05:00',  202, 1, NULL,  6,   NULL),
('Resume uploaded by student',                 'Resume',        'INSERT', '2025-10-01 11:35:00',  301, 1,  1,  NULL,  1),
('Job application created from NUworks sync',  'JobApplication','INSERT', '2025-10-02 08:55:00',  401, 1,  1,  NULL,  1),
('Job application stage changed to interview', 'JobApplication','UPDATE', '2025-10-02 09:30:00',  402, 1,  1,  NULL,  1),
('Notification sent for new interview',        'Notification',  'INSERT', '2025-10-02 09:35:00',  501, 1,  1,  NULL,  1),
('Coach message sent to student',              'Message',       'INSERT', '2025-10-02 09:40:00',  601, 1,  1,  NULL,  1),
('Student logged into portal',                 'Student',       'LOGIN',  '2025-10-02 10:05:00',  103, 1,  1,  NULL,  NULL),
('Student logged out of portal',               'Student',       'LOGOUT', '2025-10-02 10:45:00',  104, 1,  1,  NULL,  NULL),
('New student created from import',            'Student',       'INSERT', '2025-10-05 09:35:00',  106, 1,  5,  NULL,  NULL),
('Notification preference updated',            'Notification',  'UPDATE', '2025-10-05 10:10:00',  504, 1,  5,  NULL,  NULL),
('Resume record removed by student',           'Resume',        'DELETE', '2025-10-05 11:25:00',  303, 1,  6,  NULL,  NULL),
('Job application stage set to offer',         'JobApplication','UPDATE', '2025-10-05 11:55:00',  404, 1,  6,  NULL,  1),
('Hiring coordinator logged in',              'HiringCoordinator','LOGIN','2025-10-06 08:40:00', 801, 1, NULL,  3,   NULL),
('Hiring coordinator logged out',             'HiringCoordinator','LOGOUT','2025-10-06 09:05:00',802, 1, NULL,  3,   NULL),
('Resume parsed from uploaded PDF',           'Resume',        'INSERT', '2025-10-07 11:45:00',  304, 1,  9,  NULL,  NULL),
('Student updated graduation date',           'Student',       'UPDATE', '2025-10-07 12:05:00',  108, 1,  9,  NULL,  NULL),
('Coach assignment changed for student',      'Student',       'UPDATE', '2025-10-08 09:10:00',  109, 1, 10,  NULL,  3),
('Job posting department field updated',      'JobPosting',    'UPDATE', '2025-10-08 09:35:00',  206, 1, NULL, 10,   NULL),
('Notification marked as read',               'Notification',  'UPDATE', '2025-10-08 09:50:00',  506, 1, 10,  NULL,  NULL),
('Student logged into mobile app',            'Student',       'LOGIN',  '2025-10-08 10:05:00',  110, 1, 11,  NULL,  NULL),
('Student logged out of mobile app',          'Student',       'LOGOUT', '2025-10-08 10:20:00',  111, 1, 11,  NULL,  NULL);