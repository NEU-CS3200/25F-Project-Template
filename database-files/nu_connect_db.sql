DROP DATABASE IF EXISTS nu_connect;
CREATE DATABASE IF NOT EXISTS nu_connect;
USE nu_connect;

-- Location table
DROP TABLE IF EXISTS location;
CREATE TABLE IF NOT EXISTS location (
   location_id INT PRIMARY KEY AUTO_INCREMENT,
   city VARCHAR(100) NOT NULL,
   state VARCHAR(100),
   country VARCHAR(100) NOT NULL
);

-- Major table
DROP TABLE IF EXISTS major;
CREATE TABLE IF NOT EXISTS major (
   major_id INT PRIMARY KEY AUTO_INCREMENT,
   major_name VARCHAR(100) NOT NULL UNIQUE,
   department VARCHAR(100)
);

-- Company table
DROP TABLE IF EXISTS company;
CREATE TABLE IF NOT EXISTS company (
   company_id INT PRIMARY KEY AUTO_INCREMENT,
   company_name VARCHAR(150) NOT NULL,
   industry VARCHAR(100)
);

-- Admin table
DROP TABLE IF EXISTS admin;
CREATE TABLE IF NOT EXISTS admin (
   admin_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   role VARCHAR(50)
);

-- Analyst table
DROP TABLE IF EXISTS analyst;
CREATE TABLE IF NOT EXISTS analyst (
   analyst_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   department VARCHAR(100)
);

-- Student table
DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student (
   student_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   major_id INT,
   location_id INT,
   graduation_year INT,
   profile_summary TEXT,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (major_id) REFERENCES major(major_id) ON DELETE SET NULL,
   FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE SET NULL
);

-- Alumni table
DROP TABLE IF EXISTS alumni;
CREATE TABLE IF NOT EXISTS alumni (
   alumni_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   email VARCHAR(100) NOT NULL UNIQUE,
   graduation_year INT,
   current_role VARCHAR(100),
   company_id INT,
   field VARCHAR(100),
   bio TEXT,
   location_id INT,
   availability_status VARCHAR(20) DEFAULT 'available',
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (company_id) REFERENCES company(company_id) ON DELETE SET NULL,
   FOREIGN KEY (location_id) REFERENCES location(location_id) ON DELETE SET NULL
);

-- Connection table
DROP TABLE IF EXISTS connection;
CREATE TABLE IF NOT EXISTS connection (
   connection_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   alumni_id INT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   date_connected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE,
   UNIQUE KEY unique_connection (student_id, alumni_id)
);

-- Session table
DROP TABLE IF EXISTS session;
CREATE TABLE IF NOT EXISTS session (
   session_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   alumni_id INT NOT NULL,
   session_date DATE NOT NULL,
   session_time TIME,
   topic VARCHAR(200),
   notes TEXT,
   status VARCHAR(20) DEFAULT 'scheduled',
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Application table
DROP TABLE IF EXISTS application;
CREATE TABLE IF NOT EXISTS application (
   application_id INT PRIMARY KEY AUTO_INCREMENT,
   student_id INT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   admin_id INT,
   FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

-- Report table
DROP TABLE IF EXISTS report;
CREATE TABLE IF NOT EXISTS report (
   report_id INT PRIMARY KEY AUTO_INCREMENT,
   reporter_id INT NOT NULL,
   reporter_type VARCHAR(20) NOT NULL,
   reported_user_id INT NOT NULL,
   reported_user_type VARCHAR(20) NOT NULL,
   reason TEXT NOT NULL,
   status VARCHAR(20) DEFAULT 'pending',
   date_reported TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   admin_id INT,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL
);

-- Community Guideline table
DROP TABLE IF EXISTS community_guideline;
CREATE TABLE IF NOT EXISTS community_guideline (
   guideline_id INT PRIMARY KEY AUTO_INCREMENT,
   guideline_text TEXT NOT NULL,
   created_by_admin_id INT NOT NULL,
   date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (created_by_admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE
);

-- Announcement table
DROP TABLE IF EXISTS announcement;
CREATE TABLE IF NOT EXISTS announcement (
   announcement_id INT PRIMARY KEY AUTO_INCREMENT,
   admin_id INT NOT NULL,
   title VARCHAR(200) NOT NULL,
   message TEXT NOT NULL,
   target_audience VARCHAR(20) DEFAULT 'all',
   date_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE CASCADE
);

-- Availability Schedule table
DROP TABLE IF EXISTS availability_schedule;
CREATE TABLE IF NOT EXISTS availability_schedule (
   schedule_id INT PRIMARY KEY AUTO_INCREMENT,
   alumni_id INT NOT NULL,
   day_of_week VARCHAR(20) NOT NULL,
   start_time TIME NOT NULL,
   end_time TIME NOT NULL,
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Job Posting table
DROP TABLE IF EXISTS job_posting;
CREATE TABLE IF NOT EXISTS job_posting (
   posting_id INT PRIMARY KEY AUTO_INCREMENT,
   alumni_id INT NOT NULL,
   title VARCHAR(200) NOT NULL,
   description TEXT,
   preferred_major VARCHAR(100),
   preferred_year INT,
   date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   status VARCHAR(20) DEFAULT 'active',
   FOREIGN KEY (alumni_id) REFERENCES alumni(alumni_id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_student_email ON student(email);
CREATE INDEX idx_alumni_email ON alumni(email);
CREATE INDEX idx_alumni_field ON alumni(field);
CREATE INDEX idx_connection_status ON connection(status);
CREATE INDEX idx_session_date ON session(session_date);
CREATE INDEX idx_session_status ON session(status);
CREATE INDEX idx_application_status ON application(status);
CREATE INDEX idx_report_status ON report(status);

-- Sample data for location 
insert into location (city, state, country) values ('Irvine', 'California', 'United States');
insert into location (city, state, country) values ('Seattle', 'Washington', 'United States');
insert into location (city, state, country) values ('Washington', 'District of Columbia', 'United States');
insert into location (city, state, country) values ('Pensacola', 'Florida', 'United States');
insert into location (city, state, country) values ('Homestead', 'Florida', 'United States');
insert into location (city, state, country) values ('Houston', 'Texas', 'United States');
insert into location (city, state, country) values ('Washington', 'District of Columbia', 'United States');
insert into location (city, state, country) values ('Oakland', 'California', 'United States');
insert into location (city, state, country) values ('Las Cruces', 'New Mexico', 'United States');
insert into location (city, state, country) values ('San Francisco', 'California', 'United States');
insert into location (city, state, country) values ('Frederick', 'Maryland', 'United States');
insert into location (city, state, country) values ('Racine', 'Wisconsin', 'United States');
insert into location (city, state, country) values ('New Orleans', 'Louisiana', 'United States');
insert into location (city, state, country) values ('Asheville', 'North Carolina', 'United States');
insert into location (city, state, country) values ('Baltimore', 'Maryland', 'United States');
insert into location (city, state, country) values ('Vancouver', 'Washington', 'United States');
insert into location (city, state, country) values ('Berkeley', 'California', 'United States');
insert into location (city, state, country) values ('Lancaster', 'California', 'United States');
insert into location (city, state, country) values ('Colorado Springs', 'Colorado', 'United States');
insert into location (city, state, country) values ('Tucson', 'Arizona', 'United States');
insert into location (city, state, country) values ('Norman', 'Oklahoma', 'United States');
insert into location (city, state, country) values ('Tulsa', 'Oklahoma', 'United States');
insert into location (city, state, country) values ('Huntington', 'West Virginia', 'United States');
insert into location (city, state, country) values ('Evansville', 'Indiana', 'United States');
insert into location (city, state, country) values ('Laredo', 'Texas', 'United States');
insert into location (city, state, country) values ('Buffalo', 'New York', 'United States');
insert into location (city, state, country) values ('Des Moines', 'Iowa', 'United States');
insert into location (city, state, country) values ('Norfolk', 'Virginia', 'United States');
insert into location (city, state, country) values ('Lansing', 'Michigan', 'United States');
insert into location (city, state, country) values ('Falls Church', 'Virginia', 'United States');

-- Sample data for major
insert into major (major_name, department) values ('Computer Science', 'School of Engineering');
insert into major (major_name, department) values ('Data Science', 'School of Engineering');
insert into major (major_name, department) values ('Software Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Information Systems', 'School of Information');
insert into major (major_name, department) values ('Business Administration', 'School of Business');
insert into major (major_name, department) values ('Accounting', 'School of Business');
insert into major (major_name, department) values ('Finance', 'School of Business');
insert into major (major_name, department) values ('Marketing', 'School of Business');
insert into major (major_name, department) values ('Economics', 'School of Social Science');
insert into major (major_name, department) values ('Management', 'School of Social Science');
insert into major (major_name, department) values ('Psychology', 'School of Social Science');
insert into major (major_name, department) values ('Sociology', 'School of Humanities');
insert into major (major_name, department) values ('Political Science', 'School of Physical Science');
insert into major (major_name, department) values ('History', 'School of Biological Science');
insert into major (major_name, department) values ('Mathematics', 'School of Physical Science');
insert into major (major_name, department) values ('Statistics', 'School of Social Science');
insert into major (major_name, department) values ('Biology', 'School of Humanities');
insert into major (major_name, department) values ('Chemistry', 'School of Physical Sciences');
insert into major (major_name, department) values ('Physics', 'School of Biological Sciences');
insert into major (major_name, department) values ('Mechanical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Electrical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Civil Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Industrial Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Biomedical Engineering', 'School of Engineering');
insert into major (major_name, department) values ('Communication Studies', 'School of Communication');
insert into major (major_name, department) values ('Journalism', 'School of Communication');
insert into major (major_name, department) values ('Public Health', 'School of Public Health');
insert into major (major_name, department) values ('Education', 'School of Education');
insert into major (major_name, department) values ('Environmental Science', 'School of Social Studies');
insert into major (major_name, department) values ('Design & Media Arts', 'School of Arts');

-- Sample data for company
insert into company (company_name, industry) values ('Twitterworks', 'Data & Analytics');
insert into company (company_name, industry) values ('Twinder', 'Transportation & Logistics');
insert into company (company_name, industry) values ('Abata', 'Healthcare');
insert into company (company_name, industry) values ('Digitube', 'Cybersecurity');
insert into company (company_name, industry) values ('Avamba', 'Finance');
insert into company (company_name, industry) values ('Jabbertype', 'Technology');
insert into company (company_name, industry) values ('Youopia', 'Automotive');
insert into company (company_name, industry) values ('Jayo', 'Venture Capital');
insert into company (company_name, industry) values ('Divavu', 'Nonprofit');
insert into company (company_name, industry) values ('Trilith', 'Marketing');
insert into company (company_name, industry) values ('Trudeo', 'Technology');
insert into company (company_name, industry) values ('Kazio', 'Energy');
insert into company (company_name, industry) values ('Voonyx', 'Environmental Services');
insert into company (company_name, industry) values ('Chatterpoint', 'Data & Analytics');
insert into company (company_name, industry) values ('Kwideo', 'Automotive');
insert into company (company_name, industry) values ('Topdrive', 'Healthcare');
insert into company (company_name, industry) values ('Skyba', 'Environmental Services');
insert into company (company_name, industry) values ('Reallinks', 'Sports & Recreation');
insert into company (company_name, industry) values ('Realfire', 'Nonprofit');
insert into company (company_name, industry) values ('Dynazzy', 'Healthcare');
insert into company (company_name, industry) values ('Riffpedia', 'Consumer Products');
insert into company (company_name, industry) values ('Kwilith', 'Professional Services');
insert into company (company_name, industry) values ('Linktype', 'Healthcare');
insert into company (company_name, industry) values ('Browsedrive', 'E-commerce');
insert into company (company_name, industry) values ('Topdrive', 'Sports & Recreation');
insert into company (company_name, industry) values ('Plajo', 'Energy');
insert into company (company_name, industry) values ('Jetpulse', 'Retail');
insert into company (company_name, industry) values ('Realpoint', 'Finance');
insert into company (company_name, industry) values ('Roombo', 'Technology');
insert into company (company_name, industry) values ('Dablist', 'Legal Services');
insert into company (company_name, industry) values ('Snaptags', 'Automotive');
insert into company (company_name, industry) values ('Thoughtmix', 'Finance');
insert into company (company_name, industry) values ('Ntag', 'Marketing');
insert into company (company_name, industry) values ('Ozu', 'Gaming');
insert into company (company_name, industry) values ('Brainsphere', 'Manufacturing');

-- Sample data for admin
insert into admin (name, email, role) values ('Selby McKean', 'smckean0@cnn.com', 'Compliance Admin');
insert into admin (name, email, role) values ('Fiann Shurey', 'fshurey1@slashdot.org', 'Program Coordinator');
insert into admin (name, email, role) values ('Dolorita Warrington', 'dwarrington2@jiathis.com', 'Data Admin');
insert into admin (name, email, role) values ('Waverly Gantz', 'wgantz3@topsy.com', 'Moderator');
insert into admin (name, email, role) values ('Carl Polotti', 'cpolotti4@devhub.com', 'Data Admin');
insert into admin (name, email, role) values ('Dorian Lomen', 'dlomen5@bbc.co.uk', 'Operations Admin');
insert into admin (name, email, role) values ('Cly Vina', 'cvina6@cnbc.com', 'Student Success Admin');
insert into admin (name, email, role) values ('Darwin Sawter', 'dsawter7@addthis.com', 'Data Admin');
insert into admin (name, email, role) values ('Marsh Slatter', 'mslatter8@discuz.net', 'Data Admin');
insert into admin (name, email, role) values ('Osmund O''Kuddyhy', 'ookuddyhy9@loc.gov', 'Operations Admin');
insert into admin (name, email, role) values ('Jessee Walczynski', 'jwalczynskia@wikipedia.org', 'Data Admin');
insert into admin (name, email, role) values ('Darill Hearle', 'dhearleb@reuters.com', 'Support Specialist');
insert into admin (name, email, role) values ('Michel Laviste', 'mlavistec@buzzfeed.com', 'Program Coordinator');
insert into admin (name, email, role) values ('Jimmie Robb', 'jrobbd@europa.eu', 'Program Coordinator');
insert into admin (name, email, role) values ('Kassia Costellow', 'kcostellowe@slideshare.net', 'Moderator');
insert into admin (name, email, role) values ('Quintus Stennet', 'qstennetf@topsy.com', 'Moderator');
insert into admin (name, email, role) values ('Florella Dominighi', 'fdominighig@merriam-webster.com', 'Program Coordinator');
insert into admin (name, email, role) values ('Whitney McShea', 'wmcsheah@ebay.co.uk', 'Operations Admin');
insert into admin (name, email, role) values ('Kennie Bengall', 'kbengalli@vkontakte.ru', 'Operations Admin');
insert into admin (name, email, role) values ('Issy Pasek', 'ipasekj@github.io', 'Compliance Admin');
insert into admin (name, email, role) values ('Ethelred Mackelworth', 'emackelworthk@berkeley.edu', 'Support Specialist');
insert into admin (name, email, role) values ('Percival Crayker', 'pcraykerl@ihg.com', 'Student Success Admin');
insert into admin (name, email, role) values ('Redd Maro', 'rmarom@de.vu', 'Community Manager');
insert into admin (name, email, role) values ('Drona Darrington', 'ddarringtonn@tamu.edu', 'Compliance Admin');
insert into admin (name, email, role) values ('Charlene Dack', 'cdacko@illinois.edu', 'Data Admin');
insert into admin (name, email, role) values ('Yasmeen Bishop', 'ybishopp@berkeley.edu', 'Data Admin');
insert into admin (name, email, role) values ('Alyss Siman', 'asimanq@instagram.com', 'Student Success Admin');
insert into admin (name, email, role) values ('Roi Stede', 'rsteder@latimes.com', 'Alumni Relations Admin');
insert into admin (name, email, role) values ('Juliane Wheadon', 'jwheadons@fema.gov', 'Data Admin');
insert into admin (name, email, role) values ('Freddie Jandl', 'fjandlt@google.pl', 'Moderator');

-- Sample data for analyst
insert into analyst (name, email, department) values ('Reuben Newall', 'rnewall0@shop-pro.jp', 'Business Intelligence');
insert into analyst (name, email, department) values ('Augustine Beyn', 'abeyn1@parallels.com', 'Student Success Analytics');
insert into analyst (name, email, department) values ('Flory Cud', 'fcud2@columbia.edu', 'Business Intelligence');
insert into analyst (name, email, department) values ('Sascha Payfoot', 'spayfoot3@chicagotribune.com', 'Marketing Analytics');
insert into analyst (name, email, department) values ('Farleigh Fausset', 'ffausset4@phpbb.com', 'Platform Analytics');
insert into analyst (name, email, department) values ('Sephira Tennewell', 'stennewell5@hao123.com', 'Student Success Analytics');
insert into analyst (name, email, department) values ('Baxie Iacobo', 'biacobo6@sogou.com', 'Data Analytics');
insert into analyst (name, email, department) values ('Israel Culter', 'iculter7@imgur.com', 'Risk & Compliance Analytics');
insert into analyst (name, email, department) values ('Benedick Rumble', 'brumble8@typepad.com', 'Operations Analytics');
insert into analyst (name, email, department) values ('Sloane Shottin', 'sshottin9@odnoklassniki.ru', 'Insights Analytics');
insert into analyst (name, email, department) values ('Sonnnie Koppelmann', 'skoppelmanna@amazonaws.com', 'Data Analytics');
insert into analyst (name, email, department) values ('Marris Legrice', 'mlegriceb@army.mil', 'Product Analytics');
insert into analyst (name, email, department) values ('Audie Ciccoloi', 'aciccoloic@over-blog.com', 'Risk & Compliance Analytics');
insert into analyst (name, email, department) values ('Sascha Shotbolt', 'sshotboltd@shareasale.com', 'Student Success Analytics');
insert into analyst (name, email, department) values ('Emelita Beesey', 'ebeeseye@ycombinator.com', 'Operations Analytics');
insert into analyst (name, email, department) values ('Hilde Klaesson', 'hklaessonf@blinklist.com', 'Operations Analytics');
insert into analyst (name, email, department) values ('Yolanda Duggon', 'yduggong@google.ru', 'Data Analytics');
insert into analyst (name, email, department) values ('Clair Oneile', 'coneileh@histats.com', 'Platform Analytics');
insert into analyst (name, email, department) values ('Ronna Pasmore', 'rpasmorei@digg.com', 'Product Analytics');
insert into analyst (name, email, department) values ('Leroi Alcock', 'lalcockj@independent.co.uk', 'Operations Analytics');
insert into analyst (name, email, department) values ('West Rennock', 'wrennockk@accuweather.com', 'Business Intelligence');
insert into analyst (name, email, department) values ('Jocelyne Trenear', 'jtrenearl@google.pl', 'Risk & Compliance Analytics');
insert into analyst (name, email, department) values ('Gibby Grand', 'ggrandm@elegantthemes.com', 'Platform Analytics');
insert into analyst (name, email, department) values ('Claresta Falkner', 'cfalknern@youtube.com', 'Insights Analytics');
insert into analyst (name, email, department) values ('Allissa Oertzen', 'aoertzeno@domainmarket.com', 'Business Intelligence');
insert into analyst (name, email, department) values ('Trevor Bannister', 'tbannisterp@wikimedia.org', 'Risk & Compliance Analytics');
insert into analyst (name, email, department) values ('Sharai Martinello', 'smartinelloq@bbc.co.uk', 'Operations Analytics');
insert into analyst (name, email, department) values ('Marlane Craighall', 'mcraighallr@home.pl', 'Operations Analytics');
insert into analyst (name, email, department) values ('Kelley McIlmorow', 'kmcilmorows@cloudflare.com', 'Alumni Engagement Analytics');
insert into analyst (name, email, department) values ('Kara Crapper', 'kcrappert@sciencedirect.com', 'Data Analytics');

-- Sample data for student
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Timmy Anderson', 'timmya6@gmail.com', 24, 13, 2028, 'Thinking about switching majors and want to talk to someone who made a similar transition.', '2025/02/27');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Joe Smith', 'jsmitty@icloud.com', 2, 26, 2028, 'Looking for guidance on networking with alumni and using LinkedIn effectively.', '2024/11/26');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Malinde Malyon', 'mmalyon2@usatoday.com', 27, 8, 2026, 'Exploring marketing and brand strategy and want feedback on personal projects and resumes.', '2025/11/24');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Lola Sharland', 'lsharland3@phpbb.com', 15, 1, 2026, 'Looking for help translating my class projects into experience I can put on a resume.', '2024/09/07');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Erskine Gettins', 'egettins4@shop-pro.jp', 27, 15, 2027, 'Interested in finance and want help understanding internships', '2025/02/07');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Denna Livesey', 'dlivesey5@ft.com', null, 10, 2026, 'Interested in internships outside my home city and need help understanding relocation and planning.', '2025/05/14');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Chancey Paskins', 'cpaskins6@google.co.uk', 21, 7, 2027, 'Focused on improving my communication and leadership skills and want practical tips.', '2025/03/26');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Nichols Reddish', 'nreddish7@deliciousdays.com', 8, 22, 2027, 'work', '2025/01/05');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Paton Bickell', 'pbickell8@comsenz.com', 12, 29, 2028, 'Exploring data science and analytics and want help with projects and internship applications.', '2024/10/04');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Willis Dwine', 'wdwine9@bigcartel.com', 10, 20, 2028, 'recruiting timelines', '2025/03/13');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Linet Shadrack', 'lshadracka@chron.com', null, 23, 2028, 'Interested in AI and machine learning and want advice on what skills and projects to focus on.', '2024/08/30');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Kelli Gauge', 'kgaugeb@sphinn.com', 14, 5, 2027, 'Focused on improving my communication and leadership skills and want practical tips.', '2025/10/14');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Justin Castletine', 'jcastletinec@elpais.com', 18, 21, 2029, 'Interested in AI and machine learning and want advice on what skills and projects to focus on.', '2025/09/17');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Susy Hamp', 'shampd@ehow.com', 1, 8, 2028, 'Trying to decide between grad school and going straight into industry and want honest advice.', '2025/01/30');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Godart Denziloe', 'gdenziloee@mozilla.org', 28, 20, 2029, 'Hoping to break into software engineering and need support with interview prep and coding practice.', '2025/06/17');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Stefano Jewkes', 'sjewkesf@opera.com', 25, 29, 2029, 'Interested in product management and looking for guidance on internships and building experience.', '2025/07/10');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Rennie Schuricke', 'rschurickeg@howstuffworks.com', 2, 5, 2028, 'and clubs and looking for someone who can help me prioritize my goals.', '2024/11/18');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Deb Mityashin', 'dmityashinh@de.vu', 28, 27, 2027, 'Exploring marketing and brand strategy and want feedback on personal projects and resumes.', '2025/03/08');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Norean Stephenson', 'nstephensoni@istockphoto.com', 14, 27, 2028, 'Interested in public health and social impact and want help finding meaningful opportunities.', '2025/09/08');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Vito Oatley', 'voatleyj@clickbank.net', null, 17, 2028, 'Exploring careers at early-stage startups and need advice on where to start.', '2025/02/25');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Launce Hambers', 'lhambersk@hubpages.com', 19, 3, 2028, 'Trying to decide between grad school and going straight into industry and want honest advice.', '2025/02/01');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Gabi Coatman', 'gcoatmanl@blinklist.com', 24, 21, 2028, 'Exploring careers at early-stage startups and need advice on where to start.', '2024/11/29');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Loralee Ransome', 'lransomem@themeforest.net', 22, 1, 2026, 'Interested in finance and want help understanding internships', '2025/03/03');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Mandel Reardon', 'mreardonn@ucla.edu', 13, 14, 2027, 'Interested in internships outside my home city and need help understanding relocation and planning.', '2024/10/24');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Kingston Stallworth', 'kstallwortho@state.gov', 29, 1, 2029, 'Interested in UX and UI design and need help building a strong portfolio and online presence.', '2025/08/31');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Nikolos Chrippes', 'nchrippesp@behance.net', 30, 10, 2026, 'Interested in UX and UI design and need help building a strong portfolio and online presence.', '2025/06/05');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Candra Laver', 'claverq@ehow.com', 16, 30, 2029, 'Thinking about switching majors and want to talk to someone who made a similar transition.', '2025/03/13');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Julianne Barrington', 'jbarringtonr@yahoo.co.jp', 26, 3, 2027, 'Thinking about switching majors and want to talk to someone who made a similar transition.', '2025/01/21');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Harlen Sooper', 'hsoopers@un.org', null, 8, 2028, 'Interested in internships outside my home city and need help understanding relocation and planning.', '2024/12/30');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Romola Fishbourn', 'rfishbournt@wordpress.com', 5, 14, 2027, 'Trying to decide between grad school and going straight into industry and want honest advice.', '2025/09/05');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Clarance Bench', 'cbenchu@macromedia.com', null, 14, 2029, 'Interested in public health and social impact and want help finding meaningful opportunities.', '2024/12/11');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Rand Luna', 'rlunav@newsvine.com', null, 5, 2029, 'Interested in finance and want help understanding internships', '2024/09/09');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Ludvig Wipfler', 'lwipflerw@shareasale.com', 23, 11, 2029, 'First-generation student trying to figure out career paths in business and tech. Curious about consulting and looking for a mentor who can explain recruiting and case interviews.', '2025/06/01');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Barbi Andrick', 'bandrickx@blog.com', 21, 2, 2028, 'Exploring marketing and brand strategy and want feedback on personal projects and resumes.', '2024/08/28');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Gertie Glaister', 'gglaistery@narod.ru', 21, 20, 2029, 'Interested in UX and UI design and need help building a strong portfolio and online presence.', '2024/10/29');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Marika McMyler', 'mmcmylerz@ihg.com', 7, 23, 2027, 'Hoping to break into software engineering and need support with interview prep and coding practice.', '2024/10/10');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Lionello Rassmann', 'lrassmann10@feedburner.com', null, 1, 2026, 'Exploring careers at early-stage startups and need advice on where to start.', '2025/09/18');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Emelyne Goathrop', 'egoathrop11@sourceforge.net', 4, 16, 2029, 'Interested in public health and social impact and want help finding meaningful opportunities.', '2024/11/09');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Mechelle Rizzardi', 'mrizzardi12@businessinsider.com', 14, 7, 2028, 'work', '2024/11/22');
insert into student (name, email, major_id, location_id, graduation_year, profile_summary, created_at) values ('Nicky Kildea', 'nkildea13@webnode.com', 11, 10, 2029, 'Preparing for my first career fair and want a mentor to help me feel more confident and prepared.', '2025/11/16');

-- Sample data for alumni
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Leah Kinchin', 'lkinchin0@ucsd.edu', 2020, 'Actuary', 32, 'Gaming', 'I enjoy mentoring students who are exploring careers in tech and product and I’m happy to review resumes and projects.', 9, 'busy', '2023-10-25');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Brendon Habbin', 'bhabbin1@spiegel.de', 2020, 'VP Marketing', 28, 'Consulting', 'I transitioned careers after graduation and like helping students who feel unsure about their current major or path.', 8, 'available', '2023-04-10');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Isa Cranke', 'icranke2@soup.io', 2022, 'Quality Engineer', 10, 'Automotive', 'communication', 22, 'inactive', '2024-12-29');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Clarisse Rennels', 'crennels3@weibo.com', 2014, 'Biostatistician III', 10, 'Media & Entertainment', 'I like helping students translate class projects', 11, 'inactive', '2025-07-12');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Ashlan Cornill', 'acornill4@delicious.com', 2020, 'Junior Executive', 5, 'Cybersecurity', 'I’m in healthcare/biotech and enjoy mentoring students who are curious about mission-driven and impact-focused work.', 19, 'inactive', '2025-02-23');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Luce Gilfillan', 'lgilfillan5@businesswire.com', 2016, 'Health Coach IV', 17, 'Cybersecurity', 'I went to grad school after NU and can talk about whether it’s worth it and how to plan for it.', 15, 'available', '2025-02-02');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Emmy Basile', 'ebasile6@people.com.cn', 2022, 'Office Assistant I', 24, 'E-commerce', 'I transitioned careers after graduation and like helping students who feel unsure about their current major or path.', 12, 'busy', '2023-01-31');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Cosmo Leif', 'cleif7@cyberchimps.com', 2009, 'VP Quality Control', 13, 'Government', 'and early career growth strategy.', 15, 'inactive', '2025-11-29');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Judy Anning', 'janning8@jigsy.com', 2015, 'Marketing Assistant', 3, 'Biotech', 'I work in finance and can share insight into recruiting timelines', 9, 'inactive', '2023-04-20');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Byram Dornin', 'bdornin9@nps.gov', 2011, 'Administrative Officer', 4, 'Marketing', 'I went to grad school after NU and can talk about whether it’s worth it and how to plan for it.', 21, 'inactive', '2024-05-19');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Davina Pounsett', 'dpounsetta@yellowpages.com', 2021, 'Research Assistant III', 21, 'Energy', 'and storytelling for interviews.', 30, 'inactive', '2023-02-18');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Philomena Gellately', 'pgellatelyb@noaa.gov', 2011, 'Editor', 13, 'Education', 'I focus on product and UX and can help with portfolios', 10, 'busy', '2023-08-23');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Gregory Elder', 'gelderc@example.com', 2008, 'Staff Scientist', 17, 'Data & Analytics', 'I transitioned careers after graduation and like helping students who feel unsure about their current major or path.', 13, 'available', '2025-08-21');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Salli Drage', 'sdraged@omniture.com', 2007, 'Paralegal', 20, 'Cybersecurity', 'and part-time jobs into strong resume bullet points.', 2, 'busy', '2024-01-08');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Lacy Stuer', 'lstuere@sbwire.com', 2022, 'Structural Engineer', 28, 'Automotive', 'I focus on product and UX and can help with portfolios', 30, 'available', '2024-11-12');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Antonetta Maydwell', 'amaydwellf@about.com', 2022, 'Administrative Officer', 23, 'Media & Entertainment', 'Python', 29, 'busy', '2024-02-17');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Ingeborg Whittaker', 'iwhittakerg@sun.com', 2020, 'Staff Accountant III', 15, 'Healthcare', 'I’ve worked at both startups and big companies and can share honest pros and cons of each path.', 15, 'busy', '2023-06-25');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Masha Dobrovolny', 'mdobrovolnyh@un.org', 2015, 'Account Executive', 17, 'Nonprofit', 'I focus on product and UX and can help with portfolios', 23, 'busy', '2023-09-22');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Farleigh Brittles', 'fbrittlesi@cyberchimps.com', 2006, 'Payment Adjustment Coordinator', 3, 'Human Resources', 'I enjoy mentoring students who are exploring careers in tech and product and I’m happy to review resumes and projects.', 19, 'busy', '2025-01-22');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Carlita Goodread', 'cgoodreadj@issuu.com', 2008, 'Software Engineer I', 10, 'Marketing', 'I transitioned careers after graduation and like helping students who feel unsure about their current major or path.', 28, 'inactive', '2025-02-24');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Emmerich Severy', 'eseveryk@360.cn', 2021, 'Budget/Accounting Analyst II', 17, 'Government', 'Python', 5, 'available', '2024-08-09');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Rickie Stansfield', 'rstansfieldl@nih.gov', 2020, 'Analog Circuit Design manager', 33, 'Transportation & Logistics', 'I love talking about how to network effectively and build genuine relationships with people in your industry.', 2, 'available', '2024-08-05');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Carlin Vida', 'cvidam@mediafire.com', 2021, 'Web Designer I', 14, 'Automotive', 'I work in data and analytics and enjoy helping students with SQL', 14, 'available', '2023-06-19');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Alphard MacCaull', 'amaccaulln@gizmodo.com', 2006, 'Librarian', 16, 'Human Resources', 'I went to grad school after NU and can talk about whether it’s worth it and how to plan for it.', 9, 'busy', '2024-03-16');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Adelbert Borell', 'aborello@abc.net.au', 2020, 'Financial Advisor', 3, 'Healthcare', 'I’m passionate about supporting first-generation and underrepresented students as they navigate internships and early careers.', 18, 'inactive', '2025-11-05');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Hadria Senecaux', 'hsenecauxp@purevolume.com', 2013, 'Marketing Assistant', 28, 'Manufacturing', 'I’ve worked at both startups and big companies and can share honest pros and cons of each path.', 11, 'inactive', '2025-02-10');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Lolita Fonso', 'lfonsoq@wordpress.com', 2005, 'Help Desk Technician', 5, 'Education', 'I’m passionate about supporting first-generation and underrepresented students as they navigate internships and early careers.', 29, 'inactive', '2024-05-14');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Cris O''Callaghan', 'cocallaghanr@nba.com', 2020, 'Assistant Media Planner', 2, 'Healthcare', 'case studies', 9, 'busy', '2023-08-26');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Shantee Leipnik', 'sleipniks@infoseek.co.jp', 2019, 'Research Assistant III', 24, 'Media & Entertainment', 'I focus on product and UX and can help with portfolios', 30, 'inactive', '2025-01-23');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Jobi Fairn', 'jfairnt@goo.ne.jp', 2007, 'Community Outreach Specialist', 28, 'Real Estate', 'technical prep', 4, 'busy', '2024-05-23');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Kristoforo Stratford', 'kstratfordu@blogspot.com', 2005, 'Environmental Specialist', 19, 'Government', 'and how to talk about their projects.', 15, 'available', '2025-07-07');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Phelia Kilduff', 'pkilduffv@hibu.com', 2015, 'Chemical Engineer', 24, 'Government', 'I’m in healthcare/biotech and enjoy mentoring students who are curious about mission-driven and impact-focused work.', 25, 'available', '2025-02-05');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Benedick Queen', 'bqueenw@technorati.com', 2009, 'Associate Professor', 21, 'Transportation & Logistics', 'I enjoy doing mock interviews and helping students feel more confident going into technical or behavioral rounds.', 16, 'available', '2024-04-24');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Dehlia MacFie', 'dmacfiex@virginia.edu', 2018, 'Office Assistant I', 19, 'Biotech', 'and how to stand out as a candidate.', 16, 'available', '2023-06-17');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Chiquita Gaskoin', 'cgaskoiny@goodreads.com', 2008, 'Recruiting Manager', 15, 'Biotech', 'and part-time jobs into strong resume bullet points.', 16, 'busy', '2025-10-12');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Merci Given', 'mgivenz@time.com', 2005, 'Product Engineer', 5, 'Legal Services', 'I love talking about how to network effectively and build genuine relationships with people in your industry.', 2, 'available', '2024-10-24');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Ailene Glaister', 'aglaister10@mashable.com', 2014, 'Chief Design Engineer', 2, 'Nonprofit', 'I transitioned careers after graduation and like helping students who feel unsure about their current major or path.', 29, 'available', '2024-12-09');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Everett Jeschner', 'ejeschner11@networkadvertising.org', 2014, 'Structural Analysis Engineer', 12, 'Marketing', 'I focus on product and UX and can help with portfolios', 29, 'available', '2025-03-23');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Patricia Hrinchishin', 'phrinchishin12@unesco.org', 2022, 'Chief Design Engineer', 27, 'E-commerce', 'and storytelling for interviews.', 11, 'available', '2024-07-09');
insert into alumni (name, email, graduation_year, current_role, company_id, field, bio, location_id, availability_status, created_at) values ('Bernetta Wolfarth', 'bwolfarth13@google.pl', 2012, 'Account Executive', 4, 'Media & Entertainment', 'and how to talk about their projects.', 21, 'available', '2023-01-26');

-- Sample data for connection
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 23, 'pending', '2025/03/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (37, 12, 'pending', '2025/11/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (18, 35, 'closed', '2025/03/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 12, 'pending', '2025/03/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (20, 38, 'active', '2025/01/10');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (16, 15, 'pending', '2025/01/27');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 21, 'pending', '2025/09/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 36, 'pending', '2024/12/20');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (12, 21, 'closed', '2025/06/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (6, 22, 'active', '2024/09/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (17, 38, 'active', '2025/11/22');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 32, 'active', '2024/10/27');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (8, 14, 'active', '2025/04/04');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (23, 10, 'pending', '2025/10/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (25, 33, 'active', '2024/10/16');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (20, 36, 'closed', '2024/09/15');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (34, 40, 'active', '2024/11/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (25, 16, 'pending', '2024/12/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (14, 29, 'pending', '2024/12/31');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (26, 13, 'pending', '2025/03/22');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (21, 1, 'pending', '2025/06/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (13, 13, 'pending', '2025/06/12');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (4, 19, 'active', '2025/01/16');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (3, 31, 'pending', '2025/04/26');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 27, 'pending', '2024/12/29');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (3, 35, 'closed', '2025/02/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (20, 29, 'pending', '2025/04/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 35, 'pending', '2025/11/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (32, 9, 'closed', '2025/02/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (39, 6, 'pending', '2024/09/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (16, 15, 'pending', '2025/04/23');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 6, 'closed', '2025/05/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (24, 38, 'closed', '2025/11/24');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 11, 'closed', '2025/09/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 5, 'pending', '2025/03/05');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (22, 39, 'closed', '2025/06/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (38, 31, 'pending', '2024/09/22');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (14, 18, 'closed', '2025/06/22');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (38, 1, 'pending', '2024/10/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (35, 3, 'pending', '2025/08/27');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 22, 'closed', '2025/11/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 12, 'closed', '2025/11/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 4, 'pending', '2025/08/29');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (24, 33, 'closed', '2025/08/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (27, 14, 'closed', '2024/09/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (14, 5, 'pending', '2025/07/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 11, 'closed', '2024/12/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 37, 'pending', '2025/03/26');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 28, 'closed', '2025/07/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (28, 4, 'closed', '2024/10/04');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (4, 16, 'pending', '2025/03/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (17, 9, 'pending', '2025/10/12');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (20, 17, 'closed', '2025/05/16');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (20, 12, 'closed', '2025/11/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (5, 15, 'pending', '2025/10/26');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 9, 'pending', '2025/02/12');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 34, 'closed', '2025/03/27');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 7, 'pending', '2025/11/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (15, 16, 'active', '2025/06/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 2, 'closed', '2025/06/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (22, 29, 'pending', '2025/09/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 9, 'closed', '2025/09/15');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (11, 39, 'closed', '2024/09/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 18, 'closed', '2025/09/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (26, 6, 'pending', '2024/11/24');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (13, 11, 'closed', '2025/07/12');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (34, 18, 'pending', '2025/05/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (23, 30, 'pending', '2025/05/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (15, 23, 'active', '2024/10/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 2, 'active', '2025/02/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (37, 20, 'pending', '2025/02/03');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (38, 39, 'closed', '2025/02/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (24, 27, 'closed', '2025/11/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (23, 22, 'pending', '2024/09/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (11, 31, 'closed', '2025/02/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (35, 5, 'closed', '2024/12/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (12, 33, 'active', '2024/11/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (6, 10, 'closed', '2024/11/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (34, 22, 'pending', '2025/10/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 40, 'pending', '2025/03/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (5, 11, 'pending', '2025/02/25');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 25, 'active', '2025/10/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (12, 3, 'closed', '2025/01/10');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (10, 6, 'pending', '2025/06/04');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (18, 35, 'active', '2025/05/19');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 5, 'closed', '2025/07/25');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (33, 13, 'active', '2025/01/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 18, 'pending', '2025/01/15');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (33, 39, 'pending', '2024/11/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (10, 34, 'pending', '2025/09/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (10, 17, 'closed', '2025/01/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (18, 22, 'pending', '2025/02/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (11, 17, 'closed', '2025/01/25');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (18, 31, 'closed', '2025/02/24');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (24, 16, 'pending', '2025/02/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (13, 24, 'active', '2024/10/27');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (25, 37, 'pending', '2025/05/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (27, 6, 'closed', '2025/07/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (34, 32, 'pending', '2025/01/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (17, 14, 'pending', '2025/08/11');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 20, 'pending', '2024/11/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 12, 'pending', '2025/09/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (5, 9, 'pending', '2024/11/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (2, 2, 'closed', '2025/05/25');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (26, 40, 'active', '2025/04/16');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 14, 'pending', '2025/10/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (8, 33, 'pending', '2025/07/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 3, 'pending', '2025/06/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (37, 21, 'active', '2024/10/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 29, 'pending', '2025/06/10');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (12, 29, 'closed', '2025/08/11');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 40, 'closed', '2025/05/06');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (4, 36, 'pending', '2025/05/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (15, 21, 'pending', '2024/09/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (4, 38, 'pending', '2024/12/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (13, 28, 'pending', '2024/12/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (10, 22, 'pending', '2025/10/05');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (36, 20, 'active', '2025/02/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (19, 10, 'pending', '2025/01/30');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (40, 33, 'pending', '2025/03/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (3, 22, 'active', '2024/09/18');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 24, 'closed', '2025/04/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 14, 'pending', '2025/11/26');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 15, 'pending', '2025/06/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (33, 10, 'pending', '2024/09/10');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (29, 33, 'pending', '2025/02/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (21, 21, 'closed', '2025/07/08');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (32, 5, 'active', '2025/09/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (13, 9, 'pending', '2025/11/17');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (27, 23, 'pending', '2025/08/26');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (3, 35, 'pending', '2025/11/01');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (26, 2, 'pending', '2025/10/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (1, 18, 'pending', '2025/04/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (21, 4, 'pending', '2025/04/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (15, 4, 'pending', '2025/03/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (3, 31, 'active', '2024/09/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (36, 27, 'closed', '2024/12/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (17, 19, 'active', '2025/05/07');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (6, 38, 'pending', '2025/10/21');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (38, 12, 'active', '2025/09/02');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 22, 'closed', '2024/10/12');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (25, 22, 'closed', '2025/07/05');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 5, 'pending', '2024/10/13');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (17, 15, 'pending', '2025/03/22');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (5, 37, 'pending', '2025/08/29');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (9, 37, 'active', '2025/08/09');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (25, 5, 'closed', '2025/10/28');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (4, 20, 'pending', '2025/08/20');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (7, 12, 'pending', '2025/09/14');
insert ignore into connection (student_id, alumni_id, status, date_connected) values (31, 35, 'closed', '2025/06/11');

-- Sample data for availability_schedule
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (24, 'Saturday', '13:10', '18:05');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (7, 'Monday', '13:16', '19:37');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Sunday', '12:34', '19:42');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (12, 'Saturday', '11:04', '18:57');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (19, 'Tuesday', '10:44', '18:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (18, 'Wednesday', '14:48', '18:27');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (38, 'Friday', '13:04', '20:13');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (35, 'Saturday', '12:52', '18:31');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Sunday', '9:06', '19:09');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (27, 'Wednesday', '15:00', '19:06');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (18, 'Saturday', '14:13', '20:46');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (5, 'Monday', '10:04', '20:00');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (37, 'Wednesday', '13:32', '19:09');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (30, 'Monday', '10:19', '18:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (24, 'Thursday', '13:42', '20:40');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (12, 'Saturday', '11:38', '19:41');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (8, 'Tuesday', '11:44', '20:24');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Thursday', '9:55', '19:12');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (22, 'Tuesday', '12:45', '20:49');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (30, 'Saturday', '13:30', '18:38');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (7, 'Monday', '15:24', '19:36');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (37, 'Sunday', '13:42', '19:28');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (30, 'Sunday', '14:14', '20:29');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (1, 'Tuesday', '14:54', '19:05');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (36, 'Wednesday', '16:47', '19:20');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Thursday', '14:41', '18:18');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (24, 'Monday', '9:18', '20:35');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (6, 'Friday', '14:50', '19:11');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (1, 'Thursday', '11:36', '20:24');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (15, 'Saturday', '16:02', '20:44');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (22, 'Wednesday', '15:27', '20:37');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (8, 'Wednesday', '9:16', '18:53');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (18, 'Wednesday', '12:27', '19:17');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (18, 'Friday', '16:56', '18:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (20, 'Sunday', '14:32', '19:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (24, 'Tuesday', '14:07', '20:46');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (35, 'Sunday', '9:51', '20:24');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (26, 'Monday', '9:52', '18:21');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (8, 'Sunday', '15:48', '19:22');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (30, 'Friday', '13:40', '19:18');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (25, 'Wednesday', '9:16', '18:37');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (30, 'Thursday', '14:56', '19:00');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (28, 'Wednesday', '16:41', '18:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (21, 'Friday', '11:52', '20:41');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (19, 'Saturday', '11:13', '19:28');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Monday', '13:57', '20:54');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (12, 'Friday', '11:33', '19:51');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (1, 'Monday', '12:02', '18:19');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (3, 'Monday', '9:52', '19:35');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (22, 'Wednesday', '16:37', '19:26');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (37, 'Monday', '10:00', '20:53');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (28, 'Tuesday', '9:16', '20:01');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (17, 'Wednesday', '10:00', '19:54');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (34, 'Monday', '16:19', '19:26');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (22, 'Friday', '11:47', '18:38');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (2, 'Friday', '12:09', '20:14');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (28, 'Monday', '12:00', '18:13');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (10, 'Saturday', '13:41', '20:37');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (15, 'Monday', '13:38', '18:58');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (27, 'Friday', '10:27', '20:38');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (12, 'Monday', '14:56', '20:26');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (7, 'Wednesday', '13:53', '19:40');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (29, 'Monday', '14:23', '18:48');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (24, 'Saturday', '13:52', '20:52');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (10, 'Friday', '10:49', '19:31');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (38, 'Tuesday', '16:57', '20:23');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (13, 'Tuesday', '13:10', '20:58');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (18, 'Thursday', '11:33', '19:39');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (6, 'Tuesday', '11:39', '20:46');
insert into availability_schedule (alumni_id, day_of_week, start_time, end_time) values (35, 'Tuesday', '12:34', '18:03');

-- Sample data for job_posting
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (2, 'Marketing Intern', 'Experienced HR manager with a focus on employee development and creating a positive work culture.', 'Information Systems', 3, '2024/09/14', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (36, 'Program Assistant', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Communication Studies', 2, '2025/08/25', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (23, 'Operations Intern', 'Experienced software engineer specializing in front-end development with a passion for creating user-friendly interfaces.', 'Mechanical Engineering', 3, '2024/05/23', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (35, 'Project Coordinator Intern', 'Detail-oriented project manager with a proven track record of delivering projects on time and within budget.', 'Marketing', 3, '2024/05/30', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (36, 'Public Policy Intern', 'Customer service representative with a friendly demeanor and a commitment to providing excellent service.', 'Finance', 4, '2025/10/19', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (17, 'Content Creator Intern', 'Results-driven marketing specialist with expertise in digital marketing strategies and campaign management.', 'Economics', 3, '2025/10/15', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (4, 'Growth Intern', 'Experienced software engineer specializing in front-end development with a passion for creating user-friendly interfaces.', 'Marketing', 3, '2024/04/24', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (40, 'Business Analyst Intern', 'Creative graphic designer with a knack for turning ideas into visually appealing designs.', 'Communication Studies', 4, '2024/07/09', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (8, 'Customer Success Intern', 'Creative video producer with a talent for storytelling and bringing ideas to life through visual content.', 'Psychology', 2, '2024/03/26', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (10, 'Product Management Intern', 'Passionate social media manager with a talent for growing online communities and engaging with followers.', 'Software Engineering', 2, '2024/01/26', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (26, 'Research Assistant', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Data Science', 3, '2024/05/09', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (40, 'Program Assistant', 'Detail-oriented project manager with a proven track record of delivering projects on time and within budget.', 'Information Systems', 3, '2024/12/18', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (39, 'Sales Development Intern', 'Motivated administrative assistant with strong organizational skills and a dedication to supporting team members.', 'Marketing', 2, '2025/08/08', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (13, 'Software Engineering Intern', 'Creative interior designer with an eye for detail and a talent for transforming spaces into beautiful environments.', 'Economics', 2, '2024/09/23', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (3, 'IT Support Intern', 'Skilled teacher with a talent for creating engaging lesson plans and fostering a positive learning environment.', 'Economics', 2, '2024/07/21', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (21, 'UX/UI Design Intern', 'Detail-oriented legal assistant with a strong understanding of legal procedures and documentation.', 'Software Engineering', 3, '2024/01/25', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (18, 'Customer Success Intern', 'Tech-savvy IT specialist with expertise in troubleshooting technical issues and implementing solutions.', 'Software Engineering', 3, '2025/06/08', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (7, 'Consulting Intern', 'Detail-oriented project manager with a proven track record of delivering projects on time and within budget.', 'Economics', 3, '2025/11/17', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (15, 'IT Support Intern', 'Customer service representative with a friendly demeanor and a commitment to providing excellent service.', 'Finance', 4, '2025/08/23', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (17, 'Product Design Intern', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Public Health', 2, '2025/09/16', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (34, 'Content Creator Intern', 'Customer-focused sales representative with excellent communication skills and a strong ability to build relationships.', 'Software Engineering', 4, '2024/05/05', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (12, 'Content Creator Intern', 'Experienced HR manager with a focus on employee development and creating a positive work culture.', 'Economics', 4, '2025/02/03', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (6, 'Project Coordinator Intern', 'Passionate social media manager with a talent for growing online communities and engaging with followers.', 'Psychology', 2, '2025/11/24', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (18, 'Finance Intern', 'Experienced HR manager with a focus on employee development and creating a positive work culture.', 'Economics', 3, '2024/10/21', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (20, 'Program Assistant', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Economics', 4, '2024/06/21', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (39, 'Customer Success Intern', 'Results-driven marketing specialist with expertise in digital marketing strategies and campaign management.', 'Mechanical Engineering', 4, '2025/09/10', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (6, 'Project Coordinator Intern', 'Creative interior designer with an eye for detail and a talent for transforming spaces into beautiful environments.', 'Statistics', 2, '2025/04/26', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (31, 'Project Coordinator Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Electrical Engineering', 2, '2025/07/14', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (27, 'Data Analyst Intern', 'Motivated administrative assistant with strong organizational skills and a dedication to supporting team members.', 'Mathematics', 4, '2024/06/07', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (20, 'Project Coordinator Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Information Systems', 4, '2024/06/01', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (9, 'Program Assistant', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Electrical Engineering', 3, '2024/10/30', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (28, 'Public Policy Intern', 'Creative graphic designer with a knack for turning ideas into visually appealing designs.', 'Psychology', 4, '2025/11/15', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (35, 'Data Analyst Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Marketing', 2, '2024/09/16', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (4, 'Research Assistant', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Finance', 3, '2024/04/09', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (4, 'Customer Success Intern', 'Detail-oriented legal assistant with a strong understanding of legal procedures and documentation.', 'Data Science', 2, '2025/03/18', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (7, 'Data Analyst Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Information Systems', 2, '2024/07/29', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (40, 'Data Analyst Intern', 'Creative graphic designer with a knack for turning ideas into visually appealing designs.', 'Public Health', 4, '2024/07/03', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (16, 'Program Assistant', 'Creative interior designer with an eye for detail and a talent for transforming spaces into beautiful environments.', 'Public Health', 3, '2024/08/10', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (29, 'Business Analyst Intern', 'Customer-focused sales representative with excellent communication skills and a strong ability to build relationships.', 'Information Systems', 4, '2024/12/13', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (35, 'Sales Development Intern', 'Motivated real estate agent with a knack for matching clients with their dream homes and negotiating deals.', 'Software Engineering', 4, '2025/08/08', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (19, 'Data Analyst Intern', 'Experienced software engineer specializing in front-end development with a passion for creating user-friendly interfaces.', 'Electrical Engineering', 4, '2024/07/11', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (5, 'Product Design Intern', 'Creative graphic designer with a knack for turning ideas into visually appealing designs.', 'Psychology', 4, '2025/03/09', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (28, 'Software Engineering Intern', 'Experienced HR manager with a focus on employee development and creating a positive work culture.', 'Mathematics', 4, '2024/04/23', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (6, 'Software Engineering Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Information Systems', 2, '2024/03/18', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (7, 'Consulting Intern', 'Detail-oriented legal assistant with a strong understanding of legal procedures and documentation.', 'Electrical Engineering', 4, '2025/07/27', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (4, 'Growth Intern', 'Dynamic event planner with a flair for creating memorable experiences and managing logistics with precision.', 'Software Engineering', 4, '2024/09/04', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (17, 'Product Management Intern', 'Dynamic event planner with a flair for creating memorable experiences and managing logistics with precision.', 'Mechanical Engineering', 3, '2025/03/05', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (24, 'Consulting Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Electrical Engineering', 4, '2025/02/13', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (21, 'UX/UI Design Intern', 'Motivated administrative assistant with strong organizational skills and a dedication to supporting team members.', 'Data Science', 2, '2025/09/02', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (2, 'Project Coordinator Intern', 'Skilled teacher with a talent for creating engaging lesson plans and fostering a positive learning environment.', 'Business Administration', 4, '2025/02/14', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (13, 'UX/UI Design Intern', 'Experienced HR manager with a focus on employee development and creating a positive work culture.', 'Mathematics', 2, '2025/07/09', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (35, 'Operations Intern', 'Skilled content writer with a flair for crafting engaging and informative content across various platforms.', 'Communication Studies', 3, '2025/10/25', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (14, 'Strategy Intern', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Electrical Engineering', 3, '2025/01/05', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (2, 'Software Engineering Intern', 'Motivated administrative assistant with strong organizational skills and a dedication to supporting team members.', 'Data Science', 3, '2025/11/12', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (10, 'IT Support Intern', 'Experienced software engineer specializing in front-end development with a passion for creating user-friendly interfaces.', 'Public Health', 2, '2024/08/08', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (26, 'Product Management Intern', 'Detail-oriented financial analyst with a strong understanding of financial markets and investment strategies.', 'Marketing', 4, '2025/04/28', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (32, 'Operations Intern', 'Dynamic event planner with a flair for creating memorable experiences and managing logistics with precision.', 'Finance', 2, '2024/03/27', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (35, 'Finance Intern', 'Detail-oriented project manager with a proven track record of delivering projects on time and within budget.', 'Public Health', 2, '2025/03/11', 'closed');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (33, 'UX/UI Design Intern', 'Creative video producer with a talent for storytelling and bringing ideas to life through visual content.', 'Mechanical Engineering', 3, '2024/05/27', 'active');
insert into job_posting (alumni_id, title, description, preferred_major, preferred_year, date_posted, status) values (16, 'Project Coordinator Intern', 'Tech-savvy IT specialist with expertise in troubleshooting technical issues and implementing solutions.', 'Software Engineering', 3, '2025/04/27', 'active');

-- Sample data for community_guideline
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Help create a welcoming environment for all', 6, '2024/01/10');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 22, '2025/02/15');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Contribute positively to the community', 9, '2024/09/19');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Follow the rules outlined in the community guidelines', 23, '2024/10/17');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect other members of the community', 7, '2025/06/20');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Think before you post to avoid misunderstandings', 16, '2024/08/05');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Be mindful of cultural differences', 29, '2024/06/23');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Listen to others'' perspectives with an open mind', 13, '2025/10/05');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Help create a welcoming environment for all', 26, '2024/04/09');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Report any inappropriate behavior to moderators', 26, '2024/12/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Engage in meaningful and respectful conversations', 7, '2025/07/20');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Engage in meaningful and respectful conversations', 26, '2025/05/09');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Be patient and understanding with new members', 8, '2024/04/21');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Follow the rules outlined in the community guidelines', 27, '2024/08/06');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Contribute positively to the community', 8, '2025/04/26');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 5, '2025/01/06');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Listen to others'' perspectives with an open mind', 21, '2025/10/03');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Contribute positively to the community', 26, '2024/02/07');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Do not share personal information of others', 15, '2024/03/19');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 7, '2025/01/12');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Help create a welcoming environment for all', 29, '2025/05/15');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Support and encourage fellow community members', 18, '2024/12/13');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Keep conversations civil and constructive', 17, '2024/09/14');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Keep conversations civil and constructive', 26, '2024/07/01');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Do not share personal information of others', 13, '2024/10/02');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Use respectful language at all times', 16, '2025/03/25');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Keep conversations civil and constructive', 16, '2024/05/27');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Keep conversations civil and constructive', 8, '2024/04/17');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Engage in meaningful and respectful conversations', 21, '2025/02/11');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Take responsibility for your words and actions', 13, '2024/03/15');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Avoid spamming or excessive self-promotion', 28, '2025/03/23');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Be mindful of cultural differences', 3, '2025/09/24');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Ask for clarification if you don''t understand something', 8, '2024/09/22');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Use respectful language at all times', 29, '2025/08/14');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 25, '2024/02/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 29, '2024/03/31');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Think before you post to avoid misunderstandings', 13, '2025/04/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Be mindful of cultural differences', 11, '2024/06/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Contribute positively to the community', 6, '2025/10/31');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Avoid hate speech and discriminatory language', 12, '2024/04/24');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Contribute positively to the community', 8, '2025/05/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Engage in meaningful and respectful conversations', 30, '2024/07/23');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Ask for clarification if you don''t understand something', 27, '2024/01/05');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Help create a welcoming environment for all', 8, '2025/02/02');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect other members of the community', 17, '2025/07/19');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Ask for clarification if you don''t understand something', 17, '2024/10/17');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Use respectful language at all times', 5, '2025/02/25');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Think before you post to avoid misunderstandings', 10, '2024/07/14');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Support and encourage fellow community members', 6, '2025/07/29');
insert into community_guideline (guideline_text, created_by_admin_id, date_created) values ('Respect the diversity of opinions within the community', 24, '2024/01/08');

-- Sample data for announcement
insert into announcement (admin_id, title, message, target_audience, date_sent) values (21, 'Upcoming Career Workshop Series', 'Important announcement regarding our latest project', 'students', '2025/03/01');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (20, 'Alumni Office Hours Sign-Up', 'Exciting updates on the horizon - stay tuned', 'students', '2024/07/23');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (20, 'Student–Alumni Networking Event', 'Important announcement regarding our new website', 'all', '2025/05/23');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (26, 'Virtual Info Session: How NU Connect Works', 'Important announcement regarding our new website', 'alumni', '2024/05/23');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (5, 'Holiday Schedule and Availability', 'Big news coming your way - stay tuned!', 'all', '2024/04/14');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (12, 'Thank You to Our Mentors Mid-Semester Check-In', 'Exciting news about our latest innovation', 'all', '2025/03/15');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (17, 'New Job and Internship Postings', 'Join us for a fun event next week', 'students', '2025/09/12');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (29, 'Alumni Office Hours Sign-Up', 'Important update regarding our new product launch', 'alumni', '2025/08/23');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (16, 'Virtual Info Session: How NU Connect Works', 'Big news coming your way - stay tuned!', 'alumni', '2024/01/25');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (30, 'Upcoming Career Workshop Series', 'An exciting opportunity for our customers', 'alumni', '2025/05/07');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (6, 'Alumni Office Hours Sign-Up', 'Exciting news about our partnership with a new company', 'all', '2024/12/17');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (21, 'Important Policy Reminder', 'Join us for a special event celebrating our anniversary', 'all', '2024/05/01');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (12, 'Reminder to Complete Your Profile', 'Exciting updates on the horizon - stay tuned', 'all', '2024/03/03');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (8, 'New Job and Internship Postings', 'Big changes coming to our company - don''t miss out!', 'all', '2024/02/24');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (7, 'New Features Available in NU Connect', 'Important update about our upcoming sale', 'students', '2025/06/13');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (8, 'Reminder to Complete Your Profile', 'Exciting updates on the horizon - stay tuned', 'all', '2025/07/13');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (13, 'Survey: Help Us Improve NU Connect', 'Join us for a fun event next week', 'students', '2024/05/31');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (26, 'Final Week to Apply for Mentorship', 'An exciting opportunity to get involved with our community', 'students', '2025/05/05');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (11, 'Holiday Schedule and Availability', 'Big changes coming to our company - don''t miss out!', 'students', '2025/06/14');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (11, 'Important Policy Reminder', 'Big changes coming to our company - don''t miss out!', 'alumni', '2024/03/10');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (6, 'Holiday Schedule and Availability', 'Important announcement regarding our latest project', 'all', '2025/06/15');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (27, 'New Job and Internship Postings', 'An exciting opportunity awaits - details coming soon', 'all', '2025/04/27');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (10, 'Updates to Community Guidelines', 'Stay tuned for a special announcement from our CEO', 'alumni', '2025/01/26');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (29, 'Thank You to Our Mentors Mid-Semester Check-In', 'An important message from our team', 'students', '2025/09/29');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (28, 'Important Policy Reminder', 'Get ready for some exciting news!', 'alumni', '2024/08/12');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (2, 'Reminder to Complete Your Profile', 'Join us for a fun event next week', 'students', '2025/05/02');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (3, 'Student–Alumni Networking Event', 'Join us for a special event celebrating our anniversary', 'students', '2024/11/05');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (1, 'Virtual Info Session: How NU Connect Works', 'Big changes coming to our company - don''t miss out!', 'alumni', '2024/07/09');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (14, 'New Success Stories from the Community', 'Important update about our upcoming sale', 'students', '2025/07/12');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (24, 'Student–Alumni Networking Event', 'Join us for a special event celebrating our anniversary', 'students', '2025/08/25');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (23, 'End-of-Term Wrap-Up and Feedback', 'Big changes coming to our company - don''t miss out!', 'students', '2025/11/19');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (29, 'Fall Mentorship Program Kickoff', 'Get ready for some exciting news!', 'students', '2024/05/01');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (20, 'Final Week to Apply for Mentorship', 'Exciting news about our latest innovation', 'students', '2024/08/07');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (22, 'Platform Maintenance and Downtime Notice', 'Important announcement regarding our latest project', 'students', '2024/02/05');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (17, 'Platform Maintenance and Downtime Notice', 'Get ready for some exciting updates from our team', 'students', '2025/07/19');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (5, 'Platform Maintenance and Downtime Notice', 'Exciting news about our partnership with a new company', 'alumni', '2025/04/16');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (5, 'New Job and Internship Postings', 'An exciting opportunity awaits - details coming soon', 'students', '2025/09/21');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (9, 'Thank You to Our Mentors Mid-Semester Check-In', 'Exciting news about our latest innovation', 'students', '2025/03/18');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (19, 'Updates to Community Guidelines', 'Exciting news about our upcoming event!', 'alumni', '2025/06/24');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (19, 'End-of-Term Wrap-Up and Feedback', 'Exciting updates on the horizon - stay tuned', 'alumni', '2024/03/24');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (15, 'Final Week to Apply for Mentorship', 'Get ready for some exciting news!', 'alumni', '2025/11/03');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (20, 'Reminder to Complete Your Profile', 'Stay tuned for a special announcement from our CEO', 'all', '2024/02/05');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (25, 'Updates to Community Guidelines', 'An exciting opportunity for our customers', 'alumni', '2024/11/11');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (8, 'Student–Alumni Networking Event', 'An exciting opportunity for our customers', 'alumni', '2024/10/29');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (21, 'Final Week to Apply for Mentorship', 'Join us for a fun event next week', 'all', '2024/02/05');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (20, 'Survey: Help Us Improve NU Connect', 'Important update about our upcoming sale', 'students', '2024/04/28');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (17, 'New Job and Internship Postings', 'Big news coming your way - stay tuned!', 'students', '2025/02/22');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (16, 'New Success Stories from the Community', 'An exciting opportunity for our customers', 'alumni', '2025/09/03');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (22, 'Updates to Community Guidelines', 'Important update regarding our new product launch', 'students', '2024/01/10');
insert into announcement (admin_id, title, message, target_audience, date_sent) values (21, 'Fall Mentorship Program Kickoff', 'Join us for a fun event next week', 'alumni', '2025/06/16');

-- Sample data for report
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (62, 'alumni', 64, 'student', 'The user is promoting violence', 'pending', '2024/10/30', 26);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (20, 'student', 8, 'student', 'The user is engaging in hate speech', 'pending', '2025/10/07', 11);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (76, 'alumni', 19, 'alumni', 'The user is bullying others', 'pending', '2024/11/22', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (29, 'alumni', 45, 'alumni', 'The user is using inappropriate language', 'solved', '2024/09/09', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (66, 'student', 79, 'alumni', 'The user is sharing inappropriate images', 'solved', '2025/04/29', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (13, 'alumni', 20, 'alumni', 'The user is violating community guidelines', 'pending', '2024/09/18', 29);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (65, 'alumni', 10, 'alumni', 'The user is posting spam content', 'pending', '2025/10/17', 26);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (54, 'alumni', 38, 'alumni', 'The user is impersonating someone else', 'pending', '2025/05/11', 22);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (13, 'student', 23, 'alumni', 'The user is harassing others', 'solved', '2024/11/01', 13);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (50, 'student', 40, 'alumni', 'The user is being disruptive', 'pending', '2024/09/16', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (63, 'student', 34, 'student', 'The user is being aggressive', 'pending', '2025/04/07', 15);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (76, 'alumni', 6, 'student', 'The user is being offensive', 'pending', '2024/12/25', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (40, 'student', 45, 'student', 'The user is being aggressive', 'solved', '2025/03/30', 12);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (51, 'student', 70, 'alumni', 'The user is sharing personal information without consent', 'pending', '2025/02/13', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (16, 'student', 67, 'student', 'The user is using inappropriate language', 'pending', '2025/10/27', 24);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (46, 'student', 28, 'alumni', 'The user is violating community guidelines', 'pending', '2025/08/05', 11);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (69, 'student', 77, 'alumni', 'The user is harassing others', 'pending', '2024/12/05', 7);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (63, 'alumni', 33, 'alumni', 'The user is being discriminatory', 'reviewed', '2025/05/26', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (76, 'alumni', 65, 'student', 'The user is being aggressive', 'solved', '2024/12/30', 28);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (79, 'alumni', 75, 'student', 'The user is posting spam content', 'pending', '2024/12/16', 6);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (48, 'alumni', 21, 'student', 'The user is posting spam content', 'pending', '2024/11/23', 22);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (53, 'alumni', 71, 'alumni', 'The user is sharing inappropriate images', 'reviewed', '2025/01/12', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (70, 'alumni', 32, 'student', 'The user is sharing personal information without consent', 'pending', '2025/07/17', 8);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (40, 'student', 42, 'student', 'The user is bullying others', 'solved', '2025/08/01', 3);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (69, 'student', 43, 'student', 'The user is engaging in illegal activities', 'pending', '2024/12/03', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (40, 'student', 27, 'student', 'The user is spreading misinformation', 'reviewed', '2025/10/17', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (26, 'alumni', 4, 'alumni', 'The user is being disruptive', 'pending', '2025/02/08', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (59, 'alumni', 6, 'student', 'The user is posting spam content', 'pending', '2024/12/18', 24);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (48, 'alumni', 26, 'alumni', 'The user is being rude', 'pending', '2024/10/06', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (49, 'alumni', 68, 'student', 'The user is being dishonest', 'pending', '2024/11/04', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (44, 'alumni', 26, 'student', 'The user is being disrespectful', 'pending', '2024/10/03', 10);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (77, 'alumni', 61, 'alumni', 'The user is impersonating someone else', 'pending', '2025/05/21', 7);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (68, 'student', 3, 'alumni', 'The user is being disrespectful', 'pending', '2025/02/26', 12);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (60, 'alumni', 55, 'student', 'The user is being aggressive', 'pending', '2024/12/20', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (47, 'alumni', 73, 'student', 'The user is promoting violence', 'pending', '2025/08/06', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (60, 'alumni', 23, 'alumni', 'The user is using inappropriate language', 'pending', '2025/08/17', 30);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (78, 'student', 36, 'student', 'The user is sharing false information', 'reviewed', '2025/08/09', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (52, 'alumni', 44, 'student', 'The user is being dishonest', 'solved', '2025/08/22', 17);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (29, 'alumni', 74, 'alumni', 'The user is sharing personal information without consent', 'pending', '2025/01/19', 25);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (78, 'student', 74, 'alumni', 'The user is being dishonest', 'pending', '2024/12/27', 6);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (9, 'alumni', 71, 'alumni', 'The user is engaging in illegal activities', 'reviewed', '2025/01/01', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (39, 'alumni', 64, 'student', 'The user is using inappropriate language', 'pending', '2025/09/18', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (45, 'student', 73, 'student', 'The user is using inappropriate language', 'pending', '2024/11/20', 8);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (30, 'alumni', 34, 'alumni', 'The user is spreading misinformation', 'pending', '2024/12/13', 7);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (14, 'alumni', 43, 'alumni', 'The user is being rude', 'pending', '2024/12/16', 1);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (72, 'alumni', 49, 'alumni', 'The user is sharing false information', 'solved', '2024/12/13', 2);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (43, 'alumni', 27, 'alumni', 'The user is sharing inappropriate images', 'solved', '2025/02/22', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (4, 'student', 72, 'alumni', 'The user is sharing personal information without consent', 'pending', '2024/12/18', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (38, 'alumni', 34, 'student', 'The user is sharing personal information without consent', 'pending', '2025/01/07', 5);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (62, 'alumni', 50, 'alumni', 'The user is engaging in hate speech', 'pending', '2025/11/11', 19);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (4, 'student', 9, 'student', 'The user is bullying others', 'pending', '2024/11/28', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (36, 'student', 40, 'student', 'The user is engaging in illegal activities', 'reviewed', '2025/07/09', 29);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (23, 'student', 50, 'student', 'The user is using inappropriate language', 'pending', '2024/10/01', 11);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (8, 'alumni', 39, 'student', 'The user is being rude', 'solved', '2025/03/10', 19);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (62, 'student', 26, 'alumni', 'The user is violating community guidelines', 'reviewed', '2025/05/20', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (72, 'alumni', 25, 'student', 'The user is engaging in hate speech', 'reviewed', '2025/10/30', 19);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (38, 'student', 33, 'alumni', 'The user is engaging in hate speech', 'solved', '2024/11/05', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (68, 'student', 71, 'student', 'The user is harassing others', 'pending', '2025/03/15', null);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (48, 'student', 54, 'alumni', 'The user is sharing false information', 'solved', '2025/08/05', 25);
insert into report (reporter_id, reporter_type, reported_user_id, reported_user_type, reason, status, date_reported, admin_id) values (13, 'alumni', 67, 'student', 'The user is bullying others', 'pending', '2025/08/06', 11);

-- Sample data for application
insert into application (student_id, status, submission_date, admin_id) values (10, 'pending', '2024/11/17', null);
insert into application (student_id, status, submission_date, admin_id) values (35, 'approved', '2025/02/05', 12);
insert into application (student_id, status, submission_date, admin_id) values (24, 'approved', '2025/07/11', 10);
insert into application (student_id, status, submission_date, admin_id) values (31, 'pending', '2024/12/19', null);
insert into application (student_id, status, submission_date, admin_id) values (29, 'rejected', '2025/09/17', 12);
insert into application (student_id, status, submission_date, admin_id) values (1, 'rejected', '2025/02/06', 16);
insert into application (student_id, status, submission_date, admin_id) values (3, 'approved', '2025/02/19', null);
insert into application (student_id, status, submission_date, admin_id) values (27, 'approved', '2025/08/19', 9);
insert into application (student_id, status, submission_date, admin_id) values (2, 'approved', '2025/01/09', 16);
insert into application (student_id, status, submission_date, admin_id) values (1, 'approved', '2025/01/03', null);
insert into application (student_id, status, submission_date, admin_id) values (18, 'pending', '2025/02/25', 7);
insert into application (student_id, status, submission_date, admin_id) values (24, 'approved', '2025/03/21', null);
insert into application (student_id, status, submission_date, admin_id) values (39, 'pending', '2025/11/26', null);
insert into application (student_id, status, submission_date, admin_id) values (36, 'approved', '2025/04/26', null);
insert into application (student_id, status, submission_date, admin_id) values (34, 'approved', '2025/11/24', 4);
insert into application (student_id, status, submission_date, admin_id) values (28, 'pending', '2025/06/22', 12);
insert into application (student_id, status, submission_date, admin_id) values (38, 'rejected', '2025/08/05', null);
insert into application (student_id, status, submission_date, admin_id) values (9, 'pending', '2024/11/24', 21);
insert into application (student_id, status, submission_date, admin_id) values (6, 'pending', '2025/05/09', null);
insert into application (student_id, status, submission_date, admin_id) values (39, 'rejected', '2025/04/10', null);
insert into application (student_id, status, submission_date, admin_id) values (14, 'rejected', '2025/06/23', 19);
insert into application (student_id, status, submission_date, admin_id) values (34, 'approved', '2025/11/08', 13);
insert into application (student_id, status, submission_date, admin_id) values (11, 'rejected', '2024/12/29', 24);
insert into application (student_id, status, submission_date, admin_id) values (23, 'pending', '2025/03/16', 18);
insert into application (student_id, status, submission_date, admin_id) values (2, 'pending', '2024/12/18', 24);
insert into application (student_id, status, submission_date, admin_id) values (6, 'rejected', '2024/09/08', 9);
insert into application (student_id, status, submission_date, admin_id) values (29, 'approved', '2024/11/10', null);
insert into application (student_id, status, submission_date, admin_id) values (13, 'pending', '2025/02/18', 17);
insert into application (student_id, status, submission_date, admin_id) values (25, 'approved', '2025/08/21', 23);
insert into application (student_id, status, submission_date, admin_id) values (31, 'rejected', '2025/07/10', null);
insert into application (student_id, status, submission_date, admin_id) values (18, 'pending', '2024/12/21', 15);
insert into application (student_id, status, submission_date, admin_id) values (33, 'pending', '2025/06/27', 18);
insert into application (student_id, status, submission_date, admin_id) values (10, 'rejected', '2025/09/23', 11);
insert into application (student_id, status, submission_date, admin_id) values (1, 'pending', '2024/12/19', null);
insert into application (student_id, status, submission_date, admin_id) values (35, 'rejected', '2024/08/03', null);
insert into application (student_id, status, submission_date, admin_id) values (37, 'rejected', '2024/08/26', null);
insert into application (student_id, status, submission_date, admin_id) values (40, 'approved', '2025/07/26', null);
insert into application (student_id, status, submission_date, admin_id) values (38, 'approved', '2025/10/01', null);
insert into application (student_id, status, submission_date, admin_id) values (27, 'pending', '2025/02/20', null);
insert into application (student_id, status, submission_date, admin_id) values (36, 'pending', '2025/03/04', 30);
insert into application (student_id, status, submission_date, admin_id) values (38, 'pending', '2024/09/20', null);
insert into application (student_id, status, submission_date, admin_id) values (2, 'approved', '2025/10/06', 14);
insert into application (student_id, status, submission_date, admin_id) values (1, 'approved', '2025/07/24', null);
insert into application (student_id, status, submission_date, admin_id) values (14, 'rejected', '2025/01/17', 30);
insert into application (student_id, status, submission_date, admin_id) values (30, 'approved', '2025/01/26', null);
insert into application (student_id, status, submission_date, admin_id) values (20, 'approved', '2025/01/14', null);
insert into application (student_id, status, submission_date, admin_id) values (8, 'approved', '2025/10/24', null);
insert into application (student_id, status, submission_date, admin_id) values (13, 'pending', '2025/01/14', 4);
insert into application (student_id, status, submission_date, admin_id) values (25, 'approved', '2024/10/23', 8);
insert into application (student_id, status, submission_date, admin_id) values (33, 'approved', '2025/03/22', null);
insert into application (student_id, status, submission_date, admin_id) values (24, 'approved', '2025/07/18', 3);
insert into application (student_id, status, submission_date, admin_id) values (17, 'pending', '2025/05/05', null);
insert into application (student_id, status, submission_date, admin_id) values (20, 'approved', '2025/08/14', 23);
insert into application (student_id, status, submission_date, admin_id) values (36, 'approved', '2025/03/26', 23);
insert into application (student_id, status, submission_date, admin_id) values (15, 'pending', '2025/01/09', null);
insert into application (student_id, status, submission_date, admin_id) values (17, 'approved', '2025/02/14', 7);
insert into application (student_id, status, submission_date, admin_id) values (25, 'pending', '2024/09/21', 15);
insert into application (student_id, status, submission_date, admin_id) values (9, 'pending', '2025/05/17', 8);
insert into application (student_id, status, submission_date, admin_id) values (29, 'approved', '2025/10/10', 6);
insert into application (student_id, status, submission_date, admin_id) values (19, 'approved', '2025/05/05', 8);

-- Sample data for session
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (40, 32, '2025/08/19', '20:25', 'Reviewing outreach messages to recruiters or alumni', 'The student''s participation in the discussion was excellent; they contributed valuable insights.', 'scheduled', '2024/10/15');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (37, 6, '2025/02/25', '15:58', 'Planning next semester with career in mind', 'The student''s enthusiasm for the topic was evident throughout our discussion.', 'scheduled', '2025/11/03');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (12, 26, '2025/11/22', '18:05', 'Internship search planning', 'The student demonstrated a strong understanding of the material we covered in our session.', 'scheduled', '2025/07/21');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (21, 10, '2025/04/18', '16:07', 'Time management and balance', 'and the student''s input was valuable.', 'completed', '2025/02/23');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (5, 35, '2025/04/09', '19:07', 'First week on the job advice', 'The student''s input during our discussion was valuable and helped deepen our understanding of the topic.', 'completed', '2025/06/17');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (14, 9, '2025/01/19', '20:18', 'Mock interview practice', 'The student''s engagement with the session topic was impressive.', 'scheduled', '2025/07/30');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (33, 22, '2024/11/13', '10:07', 'Internship search planning', 'The student shared some insightful perspectives during our session.', 'scheduled', '2024/12/05');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (12, 32, '2024/12/30', '20:34', 'First week on the job advice', 'and the student''s input was valuable.', 'scheduled', '2024/09/16');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (40, 1, '2025/06/05', '14:28', 'First week on the job advice', 'The student seemed engaged and interested in the topic we discussed today.', 'scheduled', '2025/05/18');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (37, 19, '2025/05/30', '15:45', 'Job offer or negotiation questions', 'The student''s participation in the discussion was excellent; they contributed valuable insights.', 'scheduled', '2024/10/12');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (7, 11, '2024/12/19', '18:33', 'Technical interview prep', 'The student''s questions during our discussion were perceptive and showed a deep interest in the topic.', 'completed', '2025/02/07');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (23, 20, '2024/12/06', '14:30', 'Talking through imposter feelings and confidence', 'The student asked thoughtful questions and showed a genuine interest in the topic.', 'completed', '2024/10/08');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (33, 27, '2025/03/01', '16:36', 'Grad school vs industry discussion', 'The student shared some insightful perspectives during our session.', 'cancelled', '2024/09/16');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (19, 13, '2025/03/16', '15:32', 'Reviewing outreach messages to recruiters or alumni', 'The student''s participation in the discussion was excellent; they contributed valuable insights.', 'completed', '2024/12/31');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (24, 8, '2024/11/17', '9:44', 'First week on the job advice', 'It was a pleasure discussing the session topic with the student; they had some interesting insights.', 'cancelled', '2024/10/02');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (21, 40, '2025/10/28', '15:04', 'Talking through imposter feelings and confidence', 'The student''s questions during our discussion were perceptive and showed a deep interest in the topic.', 'completed', '2025/03/23');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (35, 11, '2025/08/12', '16:25', 'Time management and balance', 'The student seemed engaged and interested in the topic we discussed today.', 'completed', '2025/10/10');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (30, 19, '2025/06/27', '14:49', 'Job offer or negotiation questions', 'The student''s questions during our discussion were perceptive and showed a deep interest in the topic.', 'cancelled', '2025/11/30');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (17, 24, '2024/11/07', '13:35', 'Mock interview practice', 'and the student''s input was valuable.', 'cancelled', '2025/01/07');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (29, 6, '2025/08/18', '18:11', 'Time management and balance', 'We had a great discussion about the session topic', 'completed', '2025/09/09');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (18, 38, '2024/11/03', '14:20', 'Grad school vs industry discussion', 'We had a productive conversation about the session topic and the student seemed to grasp the concepts well.', 'scheduled', '2025/02/07');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (18, 31, '2025/11/26', '18:23', 'Networking strategy and LinkedIn review', 'The student''s enthusiasm for the topic was evident throughout our discussion.', 'completed', '2025/10/30');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (5, 2, '2024/12/11', '11:21', 'Exploring non-traditional career paths', 'The student''s input during our discussion was valuable and helped deepen our understanding of the topic.', 'scheduled', '2024/09/11');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (18, 18, '2025/06/29', '13:19', 'Reviewing outreach messages to recruiters or alumni', 'The student''s engagement with the session topic was impressive.', 'scheduled', '2025/06/28');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (21, 19, '2025/03/23', '18:16', 'Mock interview practice', 'The student''s analysis of the session topic was thorough and well-reasoned.', 'completed', '2025/04/13');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (23, 2, '2025/05/13', '19:19', 'Networking strategy and LinkedIn review', 'The student''s feedback on the session topic was thoughtful and well-articulated.', 'cancelled', '2025/10/05');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (34, 30, '2025/08/08', '15:03', 'Portfolio or project feedback', 'The student shared some insightful perspectives during our session.', 'cancelled', '2024/08/13');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (34, 13, '2025/11/25', '20:27', 'Technical interview prep', 'and the student''s input was valuable.', 'scheduled', '2025/08/16');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (15, 24, '2025/11/08', '14:40', 'Time management and balance', 'The student shared some insightful perspectives during our session.', 'scheduled', '2025/09/11');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (32, 10, '2025/02/02', '17:00', 'General career exploration', 'We had a great discussion about the session topic', 'completed', '2025/08/08');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (33, 17, '2025/08/18', '18:43', 'Grad school vs industry discussion', 'The student shared some insightful perspectives during our session.', 'completed', '2024/11/07');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (22, 8, '2025/02/22', '11:40', 'Technical interview prep', 'The student''s engagement with the session topic was commendable.', 'completed', '2025/03/12');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (30, 37, '2025/02/06', '20:55', 'Exploring non-traditional career paths', 'It was a positive session with the student; they showed a good understanding of the topic.', 'completed', '2025/07/20');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (5, 34, '2025/09/04', '9:16', 'Technical interview prep', 'The student demonstrated a strong understanding of the material we covered in our session.', 'scheduled', '2025/02/20');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (39, 8, '2025/10/04', '11:17', 'General career exploration', 'The student demonstrated a good understanding of the material we covered in our session.', 'completed', '2024/11/17');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (7, 28, '2025/11/19', '17:23', 'Grad school vs industry discussion', 'It was a positive session with the student; they showed a good understanding of the topic.', 'cancelled', '2025/07/01');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (26, 27, '2025/09/13', '9:02', 'Technical interview prep', 'The student''s enthusiasm for the topic was evident throughout our discussion.', 'scheduled', '2025/07/19');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (19, 22, '2025/04/29', '12:02', 'First week on the job advice', 'It was a positive session with the student; they showed a good understanding of the topic.', 'scheduled', '2025/03/27');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (26, 18, '2024/09/14', '9:29', 'Grad school vs industry discussion', 'The student demonstrated a strong understanding of the material we covered in our session.', 'scheduled', '2025/06/21');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (27, 28, '2025/09/20', '12:12', 'Networking strategy and LinkedIn review', 'The student''s analysis of the session topic was thorough and well-reasoned.', 'completed', '2025/09/23');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (31, 23, '2025/09/01', '13:04', 'Job offer or negotiation questions', 'We had a productive conversation about the session topic and the student seemed to grasp the concepts well.', 'completed', '2025/02/06');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (9, 7, '2025/10/31', '19:02', 'Talking through imposter feelings and confidence', 'and the student''s input was valuable.', 'scheduled', '2025/08/02');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (31, 31, '2025/04/29', '9:56', 'Mock interview practice', 'We had a productive conversation about the session topic and the student seemed to grasp the concepts well.', 'scheduled', '2025/04/21');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (13, 10, '2025/10/24', '9:03', 'Job offer or negotiation questions', 'It was a positive session with the student; they showed a good understanding of the topic.', 'completed', '2024/10/22');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (2, 27, '2025/06/04', '10:40', 'First week on the job advice', 'The student''s feedback on the session topic was constructive and well-received.', 'completed', '2024/08/07');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (32, 14, '2025/01/27', '10:55', 'Portfolio or project feedback', 'The student''s questions during our discussion were perceptive and showed a deep interest in the topic.', 'scheduled', '2024/09/11');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (22, 14, '2025/10/02', '13:53', 'Internship search planning', 'The student''s questions during our discussion were perceptive and showed a deep interest in the topic.', 'completed', '2025/06/15');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (5, 3, '2025/04/10', '13:13', 'Talking through imposter feelings and confidence', 'It was a pleasure discussing the session topic with the student; they had some interesting insights.', 'scheduled', '2025/06/01');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (10, 12, '2025/01/01', '11:17', 'Internship search planning', 'The student''s engagement with the session topic was impressive.', 'scheduled', '2025/06/05');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (11, 4, '2025/05/08', '14:45', 'Internship search planning', 'It was a positive session with the student; they showed a good understanding of the topic.', 'scheduled', '2025/02/12');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (7, 36, '2025/03/30', '12:23', 'Exploring non-traditional career paths', 'The student shared some insightful perspectives during our session.', 'cancelled', '2025/03/05');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (13, 4, '2025/07/23', '10:38', 'Resume review and career story', 'It was a positive session with the student; they showed a good understanding of the topic.', 'completed', '2025/06/29');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (31, 32, '2024/10/04', '20:46', 'Grad school vs industry discussion', 'The student''s feedback on the session topic was constructive and well-received.', 'cancelled', '2025/08/01');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (11, 20, '2024/09/29', '16:48', 'Talking through imposter feelings and confidence', 'The student seemed engaged and interested in the topic we discussed today.', 'completed', '2025/05/06');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (25, 35, '2025/03/02', '16:30', 'Networking strategy and LinkedIn review', 'The student''s feedback on the session topic was thoughtful and well-articulated.', 'completed', '2024/09/30');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (24, 22, '2025/08/14', '16:13', 'Talking through imposter feelings and confidence', 'We had a productive conversation about the session topic and the student seemed to grasp the concepts well.', 'scheduled', '2025/10/09');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (40, 22, '2025/07/19', '16:54', 'General career exploration', 'The student''s engagement with the session topic was impressive.', 'completed', '2025/06/12');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (7, 34, '2024/10/29', '11:10', 'Mock interview practice', 'The student''s engagement with the session topic was commendable.', 'cancelled', '2024/12/14');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (40, 35, '2025/03/16', '15:43', 'Time management and balance', 'The student''s feedback on the session topic was constructive and well-received.', 'completed', '2025/06/15');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (32, 3, '2025/06/13', '18:07', 'General career exploration', 'The student showed a strong grasp of the material and asked intelligent questions.', 'completed', '2024/09/20');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (33, 9, '2025/03/20', '10:24', 'General career exploration', 'The student demonstrated a strong understanding of the material we covered in our session.', 'scheduled', '2025/08/23');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (9, 18, '2024/11/27', '19:42', 'Networking strategy and LinkedIn review', 'The student showed a strong grasp of the material and asked intelligent questions.', 'completed', '2025/10/23');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (23, 18, '2025/01/13', '14:16', 'Portfolio or project feedback', 'The student showed a strong grasp of the material and asked intelligent questions.', 'completed', '2025/02/12');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (20, 4, '2025/08/07', '16:02', 'Mock interview practice', 'The student showed a strong grasp of the material and asked intelligent questions.', 'cancelled', '2025/08/28');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (11, 37, '2024/09/23', '10:07', 'Grad school vs industry discussion', 'The student shared some insightful perspectives during our session.', 'scheduled', '2025/10/01');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (12, 28, '2025/05/22', '9:27', 'Job offer or negotiation questions', 'It was a pleasure discussing the session topic with the student; they had some interesting insights.', 'cancelled', '2025/02/24');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (9, 15, '2024/12/12', '20:11', 'Internship search planning', 'We had a productive conversation about the session topic and the student seemed to grasp the concepts well.', 'completed', '2025/06/25');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (4, 8, '2025/11/25', '12:32', 'Resume review and career story', 'The student demonstrated a good understanding of the material we covered in our session.', 'scheduled', '2025/07/31');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (32, 32, '2025/01/02', '16:29', 'Time management and balance', 'The student seemed engaged and interested in the topic we discussed today.', 'completed', '2025/05/25');
insert into session (student_id, alumni_id, session_date, session_time, topic, notes, status, created_at) values (29, 39, '2025/11/25', '20:55', 'Job offer or negotiation questions', 'The student''s analysis of the session topic was thorough and well-reasoned.', 'cancelled', '2025/09/14');
