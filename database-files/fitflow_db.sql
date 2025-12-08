DROP DATABASE IF EXISTS fitflow;
CREATE DATABASE IF NOT EXISTS fitflow;
USE fitflow;


DROP TABLE IF EXISTS System_Admin;
CREATE TABLE System_Admin
(
  system_admin_id INT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);


DROP TABLE IF EXISTS User;
CREATE TABLE User(
  user_id       INT PRIMARY KEY AUTO_INCREMENT,
  email         VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255)        NOT NULL,
  role          ENUM ('admin','trainer','client','analyst') NOT NULL,
  permissions   VARCHAR(255),
  created_by    INT NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_user_created_by
      FOREIGN KEY (created_by)
      REFERENCES System_Admin(system_admin_id)
      ON DELETE SET NULL
      ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Health_Analyst;
CREATE TABLE Health_Analyst(
  analyst_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id    INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name  VARCHAR(50) NOT NULL,
  CONSTRAINT fk_analyst_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,


  UNIQUE (user_id)
);


DROP TABLE IF EXISTS Trainer;
CREATE TABLE Trainer(
  trainer_id    INT PRIMARY KEY AUTO_INCREMENT,
  user_id       INT NOT NULL,
  first_name    VARCHAR(50) NOT NULL,
  last_name     VARCHAR(50) NOT NULL,
  specialization VARCHAR(100),
  certification VARCHAR(100),


  CONSTRAINT fk_trainer_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE (user_id)
);


DROP TABLE IF EXISTS Client;
CREATE TABLE Client(
  client_id     INT PRIMARY KEY AUTO_INCREMENT,
  user_id       INT NOT NULL,
  first_name    VARCHAR(50) NOT NULL,
  last_name     VARCHAR(50) NOT NULL,
  date_of_birth DATE,
  age           INT, -- derived attribute from date_of_birth
  fitness_level VARCHAR(50),
  goals         VARCHAR(255),
  join_date     DATE,
  CONSTRAINT fk_client_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  UNIQUE (user_id)
);


DROP TABLE IF EXISTS System_Log;
CREATE TABLE System_Log(
  log_id      INT PRIMARY KEY AUTO_INCREMENT,
  user_id     INT NOT NULL,
  action_type VARCHAR(100) NOT NULL,
  description TEXT,
  timestamp   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,


  CONSTRAINT fk_systemlog_user
     FOREIGN KEY (user_id) REFERENCES User(user_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Backup_Log;
CREATE TABLE Backup_Log(
  backup_id        INT PRIMARY KEY AUTO_INCREMENT,
  performed_by     INT NOT NULL,   -- system_admin_id
  backup_start     DATETIME NOT NULL,
  backup_end       DATETIME NOT NULL,
  backup_time_mins INT,
  status           ENUM('success','failed','partial') NOT NULL,
  CONSTRAINT fk_backuplog_admin
     FOREIGN KEY (performed_by) REFERENCES System_Admin(system_admin_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Health_Metrics;
CREATE TABLE Health_Metrics(
  metric_id           INT PRIMARY KEY AUTO_INCREMENT,
  client_id           INT NOT NULL,
  analyst_id          INT,
  record_date         DATE NOT NULL,
  weight_kg           DECIMAL(5,2),
  height_inches       DECIMAL(4,1),
  bmi                 DECIMAL(4,1),
  body_fat_percentage DECIMAL(4,1),
  heart_rate          INT,
  notes               VARCHAR(500),
  CONSTRAINT fk_metrics_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_metrics_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Trainer_Client;
CREATE TABLE Trainer_Client(
  trainer_id INT NOT NULL,
  client_id  INT NOT NULL,
  start_date DATE NOT NULL,
  PRIMARY KEY (trainer_id, client_id, start_date),
  CONSTRAINT fk_tc_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_tc_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Exercise;
CREATE TABLE Exercise(
  exercise_id INT PRIMARY KEY AUTO_INCREMENT,
  name        VARCHAR(100) NOT NULL,
  description TEXT,
  category    VARCHAR(50) NOT NULL
);


DROP TABLE IF EXISTS Workout_Session_Template;
CREATE TABLE Workout_Session_Template(
  workout_id        INT PRIMARY KEY AUTO_INCREMENT,
  trainer_id        INT NOT NULL,
  analyst_id        INT,
  name              VARCHAR(100) NOT NULL,
  description       TEXT,
  duration_minutes  INT,
  difficulty        ENUM('easy','moderate','hard') NOT NULL,
  date_created      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_wst_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_wst_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Workout_Specific_Exercise;
CREATE TABLE Workout_Specific_Exercise(
  workout_exercise_id INT PRIMARY KEY AUTO_INCREMENT,
  workout_id          INT,
  exercise_id         INT NOT NULL,
  sets                INT NOT NULL,
  reps                INT NOT NULL,
  rest_period         INT,
  CONSTRAINT fk_wse_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_wse_exercise
     FOREIGN KEY (exercise_id) REFERENCES Exercise(exercise_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Client_Specific_Workout_Program;
CREATE TABLE Client_Specific_Workout_Program(
  program_id  INT PRIMARY KEY AUTO_INCREMENT,
  workout_id  INT NOT NULL,
  created_by  INT NOT NULL,   -- trainer_id
  client_id   INT NOT NULL,
  name        VARCHAR(100) NOT NULL,
  description TEXT,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_cswp_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cswp_trainer
     FOREIGN KEY (created_by) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cswp_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Client_Workout_Log;
CREATE TABLE Client_Workout_Log (
  log_id            INT PRIMARY KEY AUTO_INCREMENT,
  client_id         INT NOT NULL,
  workout_id        INT NOT NULL,  -- from Workout_Session_Template
  analyst_id        INT,
  workout_date      DATE NOT NULL,
  completion_status ENUM('not_started','partial','completed') NOT NULL DEFAULT 'not_started',
  duration_minutes  INT,
  notes             TEXT,
  PR                TEXT,     -- multivalued attribute
  CONSTRAINT fk_cwl_client
     FOREIGN KEY (client_id) REFERENCES Client(client_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cwl_workout
     FOREIGN KEY (workout_id) REFERENCES Workout_Session_Template(workout_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_cwl_analyst
     FOREIGN KEY (analyst_id) REFERENCES Health_Analyst(analyst_id)
     ON DELETE SET NULL ON UPDATE CASCADE
);


DROP TABLE IF EXISTS Trainer_Feedback;
CREATE TABLE Trainer_Feedback(
  feedback_id INT PRIMARY KEY AUTO_INCREMENT,
  trainer_id  INT NOT NULL,
  log_id      INT NOT NULL,
  comment     TEXT NOT NULL,
  created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_tf_trainer
     FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
     ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_tf_log
     FOREIGN KEY (log_id) REFERENCES Client_Workout_Log(log_id)
     ON DELETE CASCADE ON UPDATE CASCADE
);

-- =========================================================
-- MOCK DATA FOR FITFLOW
-- Run this AFTER creating the schema and USE fitflow;
-- =========================================================

-- System_Admin
INSERT INTO System_Admin (system_admin_id, first_name, last_name, email) VALUES
  (1, 'Sam', 'Admin', 'sysadmin@fitflow.com');

-- User
INSERT INTO User (user_id, email, password_hash, role, permissions, created_by, created_at) VALUES
  (1, 'admin1@fitflow.com', 'hashed_admin1', 'admin', NULL, 1, '2025-10-01 10:00:00'),
  (2, 'trainer1@fitflow.com', 'hashed_trainer1', 'trainer', NULL, 1, '2025-10-01 10:00:00'),
  (3, 'trainer2@fitflow.com', 'hashed_trainer2', 'trainer', NULL, 1, '2025-10-02 10:00:00'),
  (4, 'trainer3@fitflow.com', 'hashed_trainer3', 'trainer', NULL, 1, '2025-10-03 10:00:00'),
  (5, 'trainer4@fitflow.com', 'hashed_trainer4', 'trainer', NULL, 1, '2025-10-04 10:00:00'),
  (6, 'trainer5@fitflow.com', 'hashed_trainer5', 'trainer', NULL, 1, '2025-10-05 10:00:00'),
  (7, 'trainer6@fitflow.com', 'hashed_trainer6', 'trainer', NULL, 1, '2025-10-06 10:00:00'),
  (8, 'trainer7@fitflow.com', 'hashed_trainer7', 'trainer', NULL, 1, '2025-10-07 10:00:00'),
  (9, 'trainer8@fitflow.com', 'hashed_trainer8', 'trainer', NULL, 1, '2025-10-08 10:00:00'),
  (10, 'client1@fitflow.com', 'hashed_client1', 'client', NULL, 1, '2025-10-01 10:00:00'),
  (11, 'client2@fitflow.com', 'hashed_client2', 'client', NULL, 1, '2025-10-02 10:00:00'),
  (12, 'client3@fitflow.com', 'hashed_client3', 'client', NULL, 1, '2025-10-03 10:00:00'),
  (13, 'client4@fitflow.com', 'hashed_client4', 'client', NULL, 1, '2025-10-04 10:00:00'),
  (14, 'client5@fitflow.com', 'hashed_client5', 'client', NULL, 1, '2025-10-05 10:00:00'),
  (15, 'client6@fitflow.com', 'hashed_client6', 'client', NULL, 1, '2025-10-06 10:00:00'),
  (16, 'client7@fitflow.com', 'hashed_client7', 'client', NULL, 1, '2025-10-07 10:00:00'),
  (17, 'client8@fitflow.com', 'hashed_client8', 'client', NULL, 1, '2025-10-08 10:00:00'),
  (18, 'client9@fitflow.com', 'hashed_client9', 'client', NULL, 1, '2025-10-09 10:00:00'),
  (19, 'client10@fitflow.com', 'hashed_client10', 'client', NULL, 1, '2025-10-10 10:00:00'),
  (20, 'client11@fitflow.com', 'hashed_client11', 'client', NULL, 1, '2025-10-11 10:00:00'),
  (21, 'client12@fitflow.com', 'hashed_client12', 'client', NULL, 1, '2025-10-12 10:00:00'),
  (22, 'client13@fitflow.com', 'hashed_client13', 'client', NULL, 1, '2025-10-13 10:00:00'),
  (23, 'client14@fitflow.com', 'hashed_client14', 'client', NULL, 1, '2025-10-14 10:00:00'),
  (24, 'client15@fitflow.com', 'hashed_client15', 'client', NULL, 1, '2025-10-15 10:00:00'),
  (25, 'analyst1@fitflow.com', 'hashed_analyst1', 'analyst', NULL, 1, '2025-10-01 10:00:00');

-- Health_Analyst
INSERT INTO Health_Analyst (analyst_id, user_id, first_name, last_name) VALUES
  (1, 25, 'Alex', 'Analyst');

-- Trainer
INSERT INTO Trainer (trainer_id, user_id, first_name, last_name, specialization, certification) VALUES
  (1, 2, 'Trainer1', 'Fit', 'Strength', 'NASM-CPT'),
  (2, 3, 'Trainer2', 'Fit', 'Hypertrophy', 'ACE-CPT'),
  (3, 4, 'Trainer3', 'Fit', 'Endurance', 'CSCS'),
  (4, 5, 'Trainer4', 'Fit', 'Cardio', 'ISSA-CPT'),
  (5, 6, 'Trainer5', 'Fit', 'Mobility', 'NASM-CPT'),
  (6, 7, 'Trainer6', 'Fit', 'Strength', 'ACE-CPT'),
  (7, 8, 'Trainer7', 'Fit', 'Hypertrophy', 'CSCS'),
  (8, 9, 'Trainer8', 'Fit', 'Endurance', 'ISSA-CPT');

-- Client
INSERT INTO Client (client_id, user_id, first_name, last_name, date_of_birth, age, fitness_level, goals, join_date) VALUES
  (1, 10, 'Client1', 'User', '1986-02-15', 39, 'Intermediate', 'Lose weight', '2025-02-01'),
  (2, 11, 'Client2', 'User', '1987-03-15', 38, 'Intermediate', 'Build muscle', '2025-03-01'),
  (3, 12, 'Client3', 'User', '1988-04-15', 37, 'Advanced', 'Rehab', '2025-04-01'),
  (4, 13, 'Client4', 'User', '1989-05-15', 36, 'Beginner', 'Improve endurance', '2025-05-01'),
  (5, 14, 'Client5', 'User', '1990-06-15', 35, 'Beginner', 'Lose weight', '2025-06-01'),
  (6, 15, 'Client6', 'User', '1991-07-15', 34, 'Advanced', 'Improve endurance', '2025-07-01'),
  (7, 16, 'Client7', 'User', '1992-08-15', 33, 'Intermediate', 'Rehab', '2025-08-01'),
  (8, 17, 'Client8', 'User', '1993-09-15', 32, 'Beginner', 'Improve endurance', '2025-09-01'),
  (9, 18, 'CLient9', 'User', '1994-01-15', 31, 'Intermediate', 'Improve endurance', '2025-01-01'),
  (10, 19, 'Client10', 'User', '1995-02-15', 30, 'Advanced', 'Build muscle', '2025-02-01'),
  (11, 20, 'Client11', 'User', '1996-03-15', 29, 'Advanced', 'General fitness', '2025-03-01'),
  (12, 21, 'Client12', 'User', '1997-04-15', 28, 'Intermediate', 'Rehab', '2025-04-01'),
  (13, 22, 'Client13', 'User', '1998-05-15', 27, 'Intermediate', 'Lose weight', '2025-05-01'),
  (14, 23, 'Client14', 'User', '1999-06-15', 26, 'Advanced', 'Lose weight', '2025-06-01'),
  (15, 24, 'Client15', 'User', '1985-07-15', 40, 'Beginner', 'General fitness', '2025-07-01');

-- System_Log
INSERT INTO System_Log (log_id, user_id, action_type, description, timestamp) VALUES
  (1, 13, 'DELETE_LOG', 'DELETE_LOG action by user 13', '2025-10-01 09:00:00'),
  (2, 24, 'LOGOUT', 'LOGOUT action by user 24', '2025-10-01 09:15:00'),
  (3, 8, 'DELETE_LOG', 'DELETE_LOG action by user 8', '2025-10-01 09:30:00'),
  (4, 9, 'LOGIN', 'LOGIN action by user 9', '2025-10-01 09:45:00'),
  (5, 22, 'DELETE_LOG', 'DELETE_LOG action by user 22', '2025-10-01 10:00:00'),
  (6, 16, 'CREATE_WORKOUT', 'CREATE_WORKOUT action by user 16', '2025-10-01 10:15:00'),
  (7, 24, 'CREATE_WORKOUT', 'CREATE_WORKOUT action by user 24', '2025-10-01 10:30:00'),
  (8, 4, 'LOGOUT', 'LOGOUT action by user 4', '2025-10-01 10:45:00'),
  (9, 5, 'UPDATE_PROFILE', 'UPDATE_PROFILE action by user 5', '2025-10-01 11:00:00'),
  (10, 14, 'CREATE_WORKOUT', 'CREATE_WORKOUT action by user 14', '2025-10-01 11:15:00'),
  (11, 12, 'UPDATE_PROFILE', 'UPDATE_PROFILE action by user 12', '2025-10-01 11:30:00'),
  (12, 16, 'LOGIN', 'LOGIN action by user 16', '2025-10-01 11:45:00'),
  (13, 9, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 9', '2025-10-01 12:00:00'),
  (14, 20, 'LOGIN', 'LOGIN action by user 20', '2025-10-01 12:15:00'),
  (15, 4, 'DELETE_LOG', 'DELETE_LOG action by user 4', '2025-10-01 12:30:00'),
  (16, 21, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 21', '2025-10-01 12:45:00'),
  (17, 13, 'UPDATE_PROFILE', 'UPDATE_PROFILE action by user 13', '2025-10-01 13:00:00'),
  (18, 18, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 18', '2025-10-01 13:15:00'),
  (19, 3, 'LOGIN', 'LOGIN action by user 3', '2025-10-01 13:30:00'),
  (20, 1, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 1', '2025-10-01 13:45:00'),
  (21, 13, 'UPDATE_PROFILE', 'UPDATE_PROFILE action by user 13', '2025-10-01 14:00:00'),
  (22, 1, 'CREATE_WORKOUT', 'CREATE_WORKOUT action by user 1', '2025-10-01 14:15:00'),
  (23, 7, 'LOGOUT', 'LOGOUT action by user 7', '2025-10-01 14:30:00'),
  (24, 14, 'CREATE_WORKOUT', 'CREATE_WORKOUT action by user 14', '2025-10-01 14:45:00'),
  (25, 11, 'DELETE_LOG', 'DELETE_LOG action by user 11', '2025-10-01 15:00:00'),
  (26, 20, 'DELETE_LOG', 'DELETE_LOG action by user 20', '2025-10-01 15:15:00'),
  (27, 14, 'UPDATE_PROFILE', 'UPDATE_PROFILE action by user 14', '2025-10-01 15:30:00'),
  (28, 4, 'LOGIN', 'LOGIN action by user 4', '2025-10-01 15:45:00'),
  (29, 10, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 10', '2025-10-01 16:00:00'),
  (30, 13, 'DELETE_LOG', 'DELETE_LOG action by user 13', '2025-10-01 16:15:00'),
  (31, 3, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 3', '2025-10-01 16:30:00'),
  (32, 18, 'DELETE_LOG', 'DELETE_LOG action by user 18', '2025-10-01 16:45:00'),
  (33, 21, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 21', '2025-10-01 17:00:00'),
  (34, 8, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 8', '2025-10-01 17:15:00'),
  (35, 23, 'VIEW_DASHBOARD', 'VIEW_DASHBOARD action by user 23', '2025-10-01 17:30:00'),
  (36, 20, 'DELETE_LOG', 'DELETE_LOG action by user 20', '2025-10-01 17:45:00'),
  (37, 20, 'LOGOUT', 'LOGOUT action by user 20', '2025-10-01 18:00:00'),
  (38, 10, 'LOGIN', 'LOGIN action by user 10', '2025-10-01 18:15:00'),
  (39, 1, 'LOGOUT', 'LOGOUT action by user 1', '2025-10-01 18:30:00'),
  (40, 5, 'DELETE_LOG', 'DELETE_LOG action by user 5', '2025-10-01 18:45:00');

-- Backup_Log
INSERT INTO Backup_Log (backup_id, performed_by, backup_start, backup_end, backup_time_mins, status) VALUES
  (1, 1, '2025-10-01 02:00:00', '2025-10-01 02:22:00', 22, 'success'),
  (2, 1, '2025-10-02 02:00:00', '2025-10-02 02:20:00', 20, 'success'),
  (3, 1, '2025-10-03 02:00:00', '2025-10-03 02:12:00', 12, 'success'),
  (4, 1, '2025-10-04 02:00:00', '2025-10-04 02:19:00', 19, 'success'),
  (5, 1, '2025-10-05 02:00:00', '2025-10-05 02:16:00', 16, 'success'),
  (6, 1, '2025-10-06 02:00:00', '2025-10-06 02:14:00', 14, 'success'),
  (7, 1, '2025-10-07 02:00:00', '2025-10-07 02:18:00', 18, 'success'),
  (8, 1, '2025-10-08 02:00:00', '2025-10-08 02:24:00', 24, 'success'),
  (9, 1, '2025-10-09 02:00:00', '2025-10-09 02:15:00', 15, 'partial'),
  (10, 1, '2025-10-10 02:00:00', '2025-10-10 02:25:00', 25, 'success');

-- Exercise
INSERT INTO Exercise (exercise_id, name, description, category) VALUES
  (1, 'Squat', 'Barbell back squat for lower body strength', 'Strength'),
  (2, 'Bench Press', 'Flat barbell bench press', 'Strength'),
  (3, 'Deadlift', 'Conventional barbell deadlift', 'Strength'),
  (4, 'Overhead Press', 'Standing barbell overhead press', 'Strength'),
  (5, 'Pull-Up', 'Bodyweight pull-up', 'Strength'),
  (6, 'Push-Up', 'Bodyweight push-up', 'Strength'),
  (7, 'Plank', 'Core isometric hold', 'Core'),
  (8, 'Mountain Climbers', 'Dynamic core and cardio move', 'Cardio'),
  (9, 'Jumping Jacks', 'Full body warm-up', 'Cardio'),
  (10, 'Burpees', 'Full body conditioning', 'Cardio'),
  (11, 'Lunges', 'Alternating walking lunges', 'Strength'),
  (12, 'Leg Press', 'Machine leg press', 'Strength'),
  (13, 'Lat Pulldown', 'Cable lat pulldown', 'Strength'),
  (14, 'Seated Row', 'Cable seated row', 'Strength'),
  (15, 'Bicep Curl', 'Dumbbell bicep curl', 'Strength'),
  (16, 'Tricep Dip', 'Bodyweight tricep dip', 'Strength'),
  (17, 'Hip Thrust', 'Barbell hip thrust', 'Strength'),
  (18, 'Russian Twist', 'Rotational core exercise', 'Core'),
  (19, 'Treadmill Run', 'Steady-state cardio on treadmill', 'Cardio'),
  (20, 'Cycling', 'Stationary bike cardio', 'Cardio');

-- Workout_Session_Template
INSERT INTO Workout_Session_Template (workout_id, trainer_id, analyst_id, name, description, duration_minutes, difficulty, date_created) VALUES
  (1, 1, 1, 'Full Body Strength A', 'Full Body Strength A template designed for general clients.', 40, 'moderate', '2025-09-01 08:00:00'),
  (2, 2, NULL, 'Full Body Strength B', 'Full Body Strength B template designed for general clients.', 30, 'hard', '2025-09-02 08:00:00'),
  (3, 3, NULL, 'Hypertrophy Upper', 'Hypertrophy Upper template designed for general clients.', 60, 'hard', '2025-09-03 08:00:00'),
  (4, 4, 1, 'Hypertrophy Lower', 'Hypertrophy Lower template designed for general clients.', 45, 'easy', '2025-09-04 08:00:00'),
  (5, 5, NULL, 'Cardio Endurance', 'Cardio Endurance template designed for general clients.', 50, 'moderate', '2025-09-05 08:00:00'),
  (6, 6, NULL, 'HIIT Conditioning', 'HIIT Conditioning template designed for general clients.', 30, 'hard', '2025-09-06 08:00:00'),
  (7, 7, 1, 'Core & Stability', 'Core & Stability template designed for general clients.', 45, 'moderate', '2025-09-07 08:00:00'),
  (8, 8, NULL, 'Mobility Flow', 'Mobility Flow template designed for general clients.', 40, 'easy', '2025-09-08 08:00:00'),
  (9, 1, NULL, 'Glute Focus', 'Glute Focus template designed for general clients.', 60, 'hard', '2025-09-09 08:00:00'),
  (10, 2, 1, 'Athletic Power', 'Athletic Power template designed for general clients.', 50, 'moderate', '2025-09-10 08:00:00');

-- Workout_Specific_Exercise
INSERT INTO Workout_Specific_Exercise (workout_exercise_id, workout_id, exercise_id, sets, reps, rest_period) VALUES
  (1, 1, 13, 4, 12, 60),
  (2, 1, 14, 3, 10, 45),
  (3, 1, 20, 3, 15, 90),
  (4, 1, 6, 3, 8, 60),
  (5, 1, 16, 3, 12, 45),
  (6, 2, 12, 4, 12, 90),
  (7, 2, 18, 3, 15, 60),
  (8, 2, 2, 5, 10, 45),
  (9, 2, 14, 3, 12, 60),
  (10, 2, 9, 3, 10, 60),
  (11, 3, 20, 3, 10, 45),
  (12, 3, 11, 4, 8, 90),
  (13, 3, 9, 3, 12, 45),
  (14, 3, 10, 3, 10, 60),
  (15, 3, 7, 3, 15, 60),
  (16, 4, 14, 3, 10, 45),
  (17, 4, 3, 4, 12, 60),
  (18, 4, 2, 4, 12, 90),
  (19, 4, 4, 5, 10, 60),
  (20, 4, 18, 3, 8, 45),
  (21, 5, 13, 4, 8, 60),
  (22, 5, 8, 3, 15, 45),
  (23, 5, 7, 3, 12, 90),
  (24, 5, 17, 3, 10, 60),
  (25, 5, 4, 4, 8, 60),
  (26, 6, 14, 4, 10, 60),
  (27, 6, 11, 3, 12, 90),
  (28, 6, 9, 3, 10, 45),
  (29, 6, 5, 3, 8, 60),
  (30, 6, 2, 4, 15, 60),
  (31, 7, 1, 3, 12, 45),
  (32, 7, 8, 4, 12, 60),
  (33, 7, 12, 3, 12, 90),
  (34, 7, 6, 3, 10, 60),
  (35, 7, 20, 5, 8, 60),
  (36, 8, 13, 3, 8, 45),
  (37, 8, 16, 3, 10, 60),
  (38, 8, 14, 4, 12, 90),
  (39, 8, 18, 3, 15, 60),
  (40, 8, 7, 3, 10, 45),
  (41, 9, 20, 3, 10, 60),
  (42, 9, 9, 3, 12, 45),
  (43, 9, 11, 4, 15, 90),
  (44, 9, 10, 3, 12, 60),
  (45, 9, 5, 3, 8, 60),
  (46, 10, 12, 4, 12, 45),
  (47, 10, 19, 3, 12, 60),
  (48, 10, 15, 3, 10, 90),
  (49, 10, 1, 3, 8, 60),
  (50, 10, 6, 3, 15, 60);

-- Trainer_Client (bridge, 130 rows)
INSERT INTO Trainer_Client (trainer_id, client_id, start_date) VALUES
  (1, 1, '2025-09-02'),
  (1, 2, '2025-09-03'),
  (1, 3, '2025-09-04'),
  (1, 4, '2025-09-05'),
  (1, 5, '2025-09-06'),
  (1, 6, '2025-09-07'),
  (1, 7, '2025-09-08'),
  (1, 8, '2025-09-09'),
  (1, 9, '2025-09-10'),
  (1, 10, '2025-09-11'),
  (1, 11, '2025-09-12'),
  (1, 12, '2025-09-13'),
  (1, 13, '2025-09-14'),
  (1, 14, '2025-09-15'),
  (1, 15, '2025-09-16'),
  (2, 1, '2025-09-17'),
  (2, 2, '2025-09-18'),
  (2, 3, '2025-09-19'),
  (2, 4, '2025-09-20'),
  (2, 5, '2025-09-21'),
  (2, 6, '2025-09-22'),
  (2, 7, '2025-09-23'),
  (2, 8, '2025-09-24'),
  (2, 9, '2025-09-25'),
  (2, 10, '2025-09-26'),
  (2, 11, '2025-09-27'),
  (2, 12, '2025-09-28'),
  (2, 13, '2025-09-29'),
  (2, 14, '2025-09-30'),
  (2, 15, '2025-10-01'),
  (3, 1, '2025-10-02'),
  (3, 2, '2025-10-03'),
  (3, 3, '2025-10-04'),
  (3, 4, '2025-10-05'),
  (3, 5, '2025-10-06'),
  (3, 6, '2025-10-07'),
  (3, 7, '2025-10-08'),
  (3, 8, '2025-10-09'),
  (3, 9, '2025-10-10'),
  (3, 10, '2025-10-11'),
  (3, 11, '2025-10-12'),
  (3, 12, '2025-10-13'),
  (3, 13, '2025-10-14'),
  (3, 14, '2025-10-15'),
  (3, 15, '2025-10-16'),
  (4, 1, '2025-10-17'),
  (4, 2, '2025-10-18'),
  (4, 3, '2025-10-19'),
  (4, 4, '2025-10-20'),
  (4, 5, '2025-10-21'),
  (4, 6, '2025-10-22'),
  (4, 7, '2025-10-23'),
  (4, 8, '2025-10-24'),
  (4, 9, '2025-10-25'),
  (4, 10, '2025-10-26'),
  (4, 11, '2025-10-27'),
  (4, 12, '2025-10-28'),
  (4, 13, '2025-10-29'),
  (4, 14, '2025-10-30'),
  (4, 15, '2025-10-31'),
  (5, 1, '2025-09-01'),
  (5, 2, '2025-09-02'),
  (5, 3, '2025-09-03'),
  (5, 4, '2025-09-04'),
  (5, 5, '2025-09-05'),
  (5, 6, '2025-09-06'),
  (5, 7, '2025-09-07'),
  (5, 8, '2025-09-08'),
  (5, 9, '2025-09-09'),
  (5, 10, '2025-09-10'),
  (5, 11, '2025-09-11'),
  (5, 12, '2025-09-12'),
  (5, 13, '2025-09-13'),
  (5, 14, '2025-09-14'),
  (5, 15, '2025-09-15'),
  (6, 1, '2025-09-16'),
  (6, 2, '2025-09-17'),
  (6, 3, '2025-09-18'),
  (6, 4, '2025-09-19'),
  (6, 5, '2025-09-20'),
  (6, 6, '2025-09-21'),
  (6, 7, '2025-09-22'),
  (6, 8, '2025-09-23'),
  (6, 9, '2025-09-24'),
  (6, 10, '2025-09-25'),
  (6, 11, '2025-09-26'),
  (6, 12, '2025-09-27'),
  (6, 13, '2025-09-28'),
  (6, 14, '2025-09-29'),
  (6, 15, '2025-09-30'),
  (7, 1, '2025-10-01'),
  (7, 2, '2025-10-02'),
  (7, 3, '2025-10-03'),
  (7, 4, '2025-10-04'),
  (7, 5, '2025-10-05'),
  (7, 6, '2025-10-06'),
  (7, 7, '2025-10-07'),
  (7, 8, '2025-10-08'),
  (7, 9, '2025-10-09'),
  (7, 10, '2025-10-10'),
  (7, 11, '2025-10-11'),
  (7, 12, '2025-10-12'),
  (7, 13, '2025-10-13'),
  (7, 14, '2025-10-14'),
  (7, 15, '2025-10-15'),
  (8, 1, '2025-10-16'),
  (8, 2, '2025-10-17'),
  (8, 3, '2025-10-18'),
  (8, 4, '2025-10-19'),
  (8, 5, '2025-10-20'),
  (8, 6, '2025-10-21'),
  (8, 7, '2025-10-22'),
  (8, 8, '2025-10-23'),
  (8, 9, '2025-10-24'),
  (8, 10, '2025-10-25'),
  (8, 11, '2025-10-26'),
  (8, 12, '2025-10-27'),
  (8, 13, '2025-10-28'),
  (8, 14, '2025-10-29'),
  (8, 15, '2025-10-30'),
  -- extra rows (reassignment)
  (1, 1, '2025-12-10'),
  (2, 2, '2025-12-11'),
  (3, 3, '2025-12-12'),
  (4, 4, '2025-12-13'),
  (5, 5, '2025-12-14'),
  (6, 6, '2025-12-15'),
  (7, 7, '2025-12-16'),
  (8, 8, '2025-12-17'),
  (1, 9, '2025-12-18'),
  (2, 10, '2025-12-19');

-- Health_Metrics (60 rows: 4 records per client)
INSERT INTO Health_Metrics (metric_id, client_id, analyst_id, record_date, weight_kg, height_inches, bmi, body_fat_percentage, heart_rate, notes) VALUES
  (1, 1, 1, '2025-09-01', 60.76, 60.3, 17.2, 26.6, 88, 'Check-in 1 for client 1'),
  (2, 1, NULL, '2025-09-08', 59.71, 60.3, 16.9, 24.0, 78, 'Check-in 2 for client 1'),
  (3, 1, 1, '2025-09-15', 60.45, 60.3, 17.2, 19.1, 71, 'Check-in 3 for client 1'),
  (4, 1, NULL, '2025-09-22', 62.72, 60.3, 17.9, 24.2, 76, 'Check-in 4 for client 1'),
  (5, 2, 1, '2025-09-01', 61.62, 60.6, 17.4, 24.2, 80, 'Check-in 1 for client 2'),
  (6, 2, NULL, '2025-09-08', 63.68, 60.6, 18.0, 16.9, 80, 'Check-in 2 for client 2'),
  (7, 2, 1, '2025-09-15', 64.73, 60.6, 18.3, 25.9, 76, 'Check-in 3 for client 2'),
  (8, 2, NULL, '2025-09-22', 61.28, 60.6, 17.3, 23.8, 81, 'Check-in 4 for client 2'),
  (9, 3, 1, '2025-09-01', 61.71, 60.9, 17.4, 23.2, 88, 'Check-in 1 for client 3'),
  (10, 3, NULL, '2025-09-08', 64.33, 60.9, 18.1, 23.9, 78, 'Check-in 2 for client 3'),
  (11, 3, 1, '2025-09-15', 62.07, 60.9, 17.5, 18.1, 70, 'Check-in 3 for client 3'),
  (12, 3, NULL, '2025-09-22', 61.66, 60.9, 17.4, 28.0, 65, 'Check-in 4 for client 3'),
  (13, 4, 1, '2025-09-01', 62.91, 61.2, 17.6, 22.4, 87, 'Check-in 1 for client 4'),
  (14, 4, NULL, '2025-09-08', 67.40, 61.2, 18.8, 20.5, 77, 'Check-in 2 for client 4'),
  (15, 4, 1, '2025-09-15', 64.30, 61.2, 18.0, 29.8, 60, 'Check-in 3 for client 4'),
  (16, 4, NULL, '2025-09-22', 65.42, 61.2, 18.3, 23.3, 80, 'Check-in 4 for client 4'),
  (17, 5, 1, '2025-09-01', 64.74, 61.5, 18.0, 20.5, 65, 'Check-in 1 for client 5'),
  (18, 5, NULL, '2025-09-08', 66.10, 61.5, 18.4, 27.5, 71, 'Check-in 2 for client 5'),
  (19, 5, 1, '2025-09-15', 65.92, 61.5, 18.3, 22.5, 80, 'Check-in 3 for client 5'),
  (20, 5, NULL, '2025-09-22', 64.32, 61.5, 17.9, 22.5, 79, 'Check-in 4 for client 5'),
  (21, 6, 1, '2025-09-01', 62.25, 61.8, 17.4, 20.0, 76, 'Check-in 1 for client 6'),
  (22, 6, NULL, '2025-09-08', 63.30, 61.8, 17.7, 24.7, 78, 'Check-in 2 for client 6'),
  (23, 6, 1, '2025-09-15', 66.60, 61.8, 18.6, 19.5, 60, 'Check-in 3 for client 6'),
  (24, 6, NULL, '2025-09-22', 63.41, 61.8, 17.8, 23.9, 73, 'Check-in 4 for client 6'),
  (25, 7, 1, '2025-09-01', 66.24, 62.1, 18.2, 16.9, 62, 'Check-in 1 for client 7'),
  (26, 7, NULL, '2025-09-08', 63.65, 62.1, 17.5, 25.2, 65, 'Check-in 2 for client 7'),
  (27, 7, 1, '2025-09-15', 65.46, 62.1, 18.0, 20.7, 73, 'Check-in 3 for client 7'),
  (28, 7, NULL, '2025-09-22', 66.85, 62.1, 18.4, 27.7, 87, 'Check-in 4 for client 7'),
  (29, 8, 1, '2025-09-01', 67.44, 62.4, 18.5, 24.6, 76, 'Check-in 1 for client 8'),
  (30, 8, NULL, '2025-09-08', 70.72, 62.4, 19.4, 22.8, 74, 'Check-in 2 for client 8'),
  (31, 8, 1, '2025-09-15', 68.13, 62.4, 18.7, 16.9, 81, 'Check-in 3 for client 8'),
  (32, 8, NULL, '2025-09-22', 70.16, 62.4, 19.2, 23.2, 62, 'Check-in 4 for client 8'),
  (33, 9, 1, '2025-09-01', 70.83, 62.7, 19.1, 21.8, 72, 'Check-in 1 for client 9'),
  (34, 9, NULL, '2025-09-08', 70.56, 62.7, 19.0, 16.8, 81, 'Check-in 2 for client 9'),
  (35, 9, 1, '2025-09-15', 73.73, 62.7, 19.9, 23.4, 65, 'Check-in 3 for client 9'),
  (36, 9, NULL, '2025-09-22', 71.02, 62.7, 19.1, 16.7, 60, 'Check-in 4 for client 9'),
  (37, 10, 1, '2025-09-01', 71.83, 63.0, 19.2, 22.4, 86, 'Check-in 1 for client 10'),
  (38, 10, NULL, '2025-09-08', 73.63, 63.0, 19.7, 24.3, 63, 'Check-in 2 for client 10'),
  (39, 10, 1, '2025-09-15', 73.07, 63.0, 19.6, 27.2, 74, 'Check-in 3 for client 10'),
  (40, 10, NULL, '2025-09-22', 73.26, 63.0, 19.6, 18.7, 82, 'Check-in 4 for client 10'),
  (41, 11, 1, '2025-09-01', 73.93, 63.3, 19.7, 19.2, 74, 'Check-in 1 for client 11'),
  (42, 11, NULL, '2025-09-08', 74.81, 63.3, 19.9, 16.8, 63, 'Check-in 2 for client 11'),
  (43, 11, 1, '2025-09-15', 74.92, 63.3, 19.9, 22.8, 70, 'Check-in 3 for client 11'),
  (44, 11, NULL, '2025-09-22', 73.72, 63.3, 19.5, 16.4, 83, 'Check-in 4 for client 11'),
  (45, 12, 1, '2025-09-01', 76.43, 63.6, 20.2, 29.4, 64, 'Check-in 1 for client 12'),
  (46, 12, NULL, '2025-09-08', 73.03, 63.6, 19.3, 24.4, 70, 'Check-in 2 for client 12'),
  (47, 12, 1, '2025-09-15', 77.45, 63.6, 20.4, 18.3, 79, 'Check-in 3 for client 12'),
  (48, 12, NULL, '2025-09-22', 76.46, 63.6, 20.1, 27.1, 86, 'Check-in 4 for client 12'),
  (49, 13, 1, '2025-09-01', 77.82, 63.9, 20.4, 27.5, 64, 'Check-in 1 for client 13'),
  (50, 13, NULL, '2025-09-08', 76.62, 63.9, 20.1, 23.6, 71, 'Check-in 2 for client 13'),
  (51, 13, 1, '2025-09-15', 78.26, 63.9, 20.5, 27.6, 69, 'Check-in 3 for client 13'),
  (52, 13, NULL, '2025-09-22', 78.65, 63.9, 20.6, 29.0, 72, 'Check-in 4 for client 13'),
  (53, 14, 1, '2025-09-01', 76.95, 64.2, 20.0, 23.9, 89, 'Check-in 1 for client 14'),
  (54, 14, NULL, '2025-09-08', 80.33, 64.2, 20.9, 22.0, 61, 'Check-in 2 for client 14'),
  (55, 14, 1, '2025-09-15', 79.38, 64.2, 20.6, 17.8, 73, 'Check-in 3 for client 14'),
  (56, 14, NULL, '2025-09-22', 79.83, 64.2, 20.8, 26.5, 82, 'Check-in 4 for client 14'),
  (57, 15, 1, '2025-09-01', 80.24, 64.5, 20.9, 17.7, 86, 'Check-in 1 for client 15'),
  (58, 15, NULL, '2025-09-08', 79.61, 64.5, 20.7, 20.1, 80, 'Check-in 2 for client 15'),
  (59, 15, 1, '2025-09-15', 82.82, 64.5, 21.5, 24.7, 72, 'Check-in 3 for client 15'),
  (60, 15, NULL, '2025-09-22', 82.79, 64.5, 21.5, 17.7, 83, 'Check-in 4 for client 15');

-- Client_Specific_Workout_Program
INSERT INTO Client_Specific_Workout_Program (program_id, workout_id, created_by, client_id, name, description, created_at) VALUES
  (1, 1, 1, 1, 'Program 1 for Client 1', 'Custom program based on Full Body Strength A', '2025-09-15 09:00:00'),
  (2, 2, 2, 2, 'Program 2 for Client 2', 'Custom program based on Full Body Strength B', '2025-09-16 09:00:00'),
  (3, 3, 3, 3, 'Program 3 for Client 3', 'Custom program based on Hypertrophy Upper', '2025-09-17 09:00:00'),
  (4, 4, 4, 4, 'Program 4 for Client 4', 'Custom program based on Hypertrophy Lower', '2025-09-18 09:00:00'),
  (5, 5, 5, 5, 'Program 5 for Client 5', 'Custom program based on Cardio Endurance', '2025-09-19 09:00:00'),
  (6, 6, 6, 6, 'Program 6 for Client 6', 'Custom program based on HIIT Conditioning', '2025-09-20 09:00:00'),
  (7, 7, 7, 7, 'Program 7 for Client 7', 'Custom program based on Core & Stability', '2025-09-21 09:00:00'),
  (8, 8, 8, 8, 'Program 8 for Client 8', 'Custom program based on Mobility Flow', '2025-09-22 09:00:00'),
  (9, 9, 1, 9, 'Program 9 for Client 9', 'Custom program based on Glute Focus', '2025-09-23 09:00:00'),
  (10, 10, 2, 10, 'Program 10 for Client 10', 'Custom program based on Athletic Power', '2025-09-24 09:00:00'),
  (11, 1, 1, 11, 'Program 11 for Client 11', 'Custom program based on Full Body Strength A', '2025-09-25 09:00:00'),
  (12, 2, 2, 12, 'Program 12 for Client 12', 'Custom program based on Full Body Strength B', '2025-09-26 09:00:00'),
  (13, 3, 3, 13, 'Program 13 for Client 13', 'Custom program based on Hypertrophy Upper', '2025-09-27 09:00:00'),
  (14, 4, 4, 14, 'Program 14 for Client 14', 'Custom program based on Hypertrophy Lower', '2025-09-28 09:00:00'),
  (15, 5, 5, 15, 'Program 15 for Client 15', 'Custom program based on Cardio Endurance', '2025-09-29 09:00:00'),
  (16, 6, 6, 1, 'Program 16 for Client 1', 'Custom program based on HIIT Conditioning', '2025-09-30 09:00:00'),
  (17, 7, 7, 2, 'Program 17 for Client 2', 'Custom program based on Core & Stability', '2025-10-01 09:00:00'),
  (18, 8, 8, 3, 'Program 18 for Client 3', 'Custom program based on Mobility Flow', '2025-10-02 09:00:00'),
  (19, 9, 1, 4, 'Program 19 for Client 4', 'Custom program based on Glute Focus', '2025-10-03 09:00:00'),
  (20, 10, 2, 5, 'Program 20 for Client 5', 'Custom program based on Athletic Power', '2025-10-04 09:00:00');

DELETE FROM Client_Workout_Log;

INSERT INTO Client_Workout_Log
(log_id, client_id, workout_id, analyst_id, workout_date, completion_status, duration_minutes, notes, PR) VALUES
  (1, 1, 1, 1, '2025-10-01', 'completed', 60, 'Workout 1 for client 1, session 1', 'New PR on exercise 10'),
  (2, 2, 2, NULL, '2025-10-02', 'completed', 40, 'Workout 2 for client 2, session 2', 'New PR on exercise 3'),
  (3, 3, 3, NULL, '2025-10-03', 'partial', 35, 'Workout 3 for client 3, session 3', NULL),
  (4, 4, 4, NULL, '2025-10-04', 'completed', 35, 'Workout 4 for client 4, session 4', 'New PR on exercise 5'),
  (5, 5, 5, 1, '2025-10-05', 'partial', 30, 'Workout 5 for client 5, session 5', NULL),
  (6, 6, 6, NULL, '2025-10-06', 'completed', 40, 'Workout 6 for client 6, session 6', 'New PR on exercise 18'),
  (7, 7, 7, NULL, '2025-10-07', 'completed', 60, 'Workout 7 for client 7, session 7', NULL),
  (8, 8, 8, NULL, '2025-10-08', 'partial', 45, 'Workout 8 for client 8, session 8', NULL),
  (9, 9, 9, 1, '2025-10-09', 'partial', 50, 'Workout 9 for client 9, session 9', NULL),
  (10, 10, 10, NULL, '2025-10-10', 'completed', 40, 'Workout 10 for client 10, session 10', 'New PR on exercise 13'),
  (11, 11, 1, NULL, '2025-10-11', 'partial', 45, 'Workout 1 for client 11, session 11', NULL),
  (12, 12, 2, NULL, '2025-10-12', 'completed', 35, 'Workout 2 for client 12, session 12', 'New PR on exercise 12'),
  (13, 13, 3, 1, '2025-10-13', 'completed', 60, 'Workout 3 for client 13, session 13', 'New PR on exercise 20'),
  (14, 14, 4, NULL, '2025-10-14', 'partial', 50, 'Workout 4 for client 14, session 14', NULL),
  (15, 15, 5, NULL, '2025-10-15', 'partial', 60, 'Workout 5 for client 15, session 15', NULL),
  (16, 1, 6, NULL, '2025-10-16', 'completed', 45, 'Workout 6 for client 1, session 16', NULL),
  (17, 2, 7, 1, '2025-10-17', 'completed', 50, 'Workout 7 for client 2, session 17', 'New PR on exercise 18'),
  (18, 3, 8, NULL, '2025-10-18', 'partial', 35, 'Workout 8 for client 3, session 18', NULL),
  (19, 4, 9, NULL, '2025-10-19', 'completed', 45, 'Workout 9 for client 4, session 19', 'New PR on exercise 2'),
  (20, 5, 10, NULL, '2025-10-20', 'partial', 50, 'Workout 10 for client 5, session 20', NULL),
  (21, 6, 1, 1, '2025-10-21', 'partial', 60, 'Workout 1 for client 6, session 21', NULL),
  (22, 7, 2, NULL, '2025-10-22', 'partial', 40, 'Workout 2 for client 7, session 22', NULL),
  (23, 8, 3, NULL, '2025-10-23', 'partial', 30, 'Workout 3 for client 8, session 23', NULL),
  (24, 9, 4, NULL, '2025-10-24', 'completed', 50, 'Workout 4 for client 9, session 24', 'New PR on exercise 14'),
  (25, 10, 5, 1, '2025-10-25', 'completed', 30, 'Workout 5 for client 10, session 25', 'New PR on exercise 1'),
  (26, 11, 6, NULL, '2025-10-26', 'completed', 40, 'Workout 6 for client 11, session 26', NULL),
  (27, 12, 7, NULL, '2025-10-27', 'completed', 50, 'Workout 7 for client 12, session 27', NULL),
  (28, 13, 8, NULL, '2025-10-28', 'completed', 35, 'Workout 8 for client 13, session 28', 'New PR on exercise 14'),
  (29, 14, 9, 1, '2025-10-29', 'completed', 50, 'Workout 9 for client 14, session 29', 'New PR on exercise 5'),
  (30, 15, 10, NULL, '2025-10-30', 'completed', 30, 'Workout 10 for client 15, session 30', 'New PR on exercise 1'),

  (31, 1, 1, NULL, '2025-10-01', 'partial', 40, 'Workout 1 for client 1, session 31', NULL),

  -- FIXED ROW (no "pending")
  (32, 2, 2, NULL, '2025-10-02', 'not_started', 35, 'Workout 2 for client 2, session 32', NULL),

  (33, 3, 3, 1, '2025-10-03', 'completed', 45, 'Workout 3 for client 3, session 33', 'New PR on exercise 19'),
  (34, 4, 4, NULL, '2025-10-04', 'partial', 50, 'Workout 4 for client 4, session 34', NULL),
  (35, 5, 5, NULL, '2025-10-05', 'completed', 30, 'Workout 5 for client 5, session 35', NULL),
  (36, 6, 6, 1, '2025-10-06', 'completed', 60, 'Workout 6 for client 6, session 36', 'New PR on exercise 3'),
  (37, 7, 7, NULL, '2025-10-07', 'partial', 45, 'Workout 7 for client 7, session 37', NULL),
  (38, 8, 8, NULL, '2025-10-08', 'partial', 35, 'Workout 8 for client 8, session 38', NULL),
  (39, 9, 9, NULL, '2025-10-09', 'completed', 60, 'Workout 9 for client 9, session 39', 'New PR on exercise 2'),
  (40, 10, 10, 1, '2025-10-10', 'partial', 40, 'Workout 10 for client 10, session 40', NULL),
  (41, 11, 1, NULL, '2025-10-11', 'completed', 45, 'Workout 1 for client 11, session 41', NULL),
  (42, 12, 2, NULL, '2025-10-12', 'completed', 60, 'Workout 2 for client 12, session 42', NULL),
  (43, 13, 3, NULL, '2025-10-13', 'partial', 35, 'Workout 3 for client 13, session 43', NULL),
  (44, 14, 4, 1, '2025-10-14', 'completed', 50, 'Workout 4 for client 14, session 44', 'New PR on exercise 16'),
  (45, 15, 5, NULL, '2025-10-15', 'completed', 30, 'Workout 5 for client 15, session 45', 'New PR on exercise 10'),
  (46, 1, 6, NULL, '2025-10-16', 'partial', 40, 'Workout 6 for client 1, session 46', NULL),
  (47, 2, 7, NULL, '2025-10-17', 'partial', 35, 'Workout 7 for client 2, session 47', NULL),
  (48, 3, 8, 1, '2025-10-18', 'completed', 60, 'Workout 8 for client 3, session 48', 'New PR on exercise 5'),
  (49, 4, 9, NULL, '2025-10-19', 'partial', 45, 'Workout 9 for client 4, session 49', NULL),
  (50, 5, 10, NULL, '2025-10-20', 'completed', 40, 'Workout 10 for client 5, session 50', 'New PR on exercise 8'),
  (51, 6, 1, 1, '2025-10-21', 'completed', 35, 'Workout 1 for client 6, session 51', 'New PR on exercise 19'),
  (52, 7, 2, NULL, '2025-10-22', 'completed', 60, 'Workout 2 for client 7, session 52', NULL),
  (53, 8, 3, NULL, '2025-10-23', 'completed', 40, 'Workout 3 for client 8, session 53', NULL),
  (54, 9, 4, NULL, '2025-10-24', 'partial', 45, 'Workout 4 for client 9, session 54', NULL),
  (55, 10, 5, 1, '2025-10-25', 'completed', 60, 'Workout 5 for client 10, session 55', 'New PR on exercise 11'),
  (56, 11, 6, NULL, '2025-10-26', 'partial', 35, 'Workout 6 for client 11, session 56', NULL),
  (57, 12, 7, NULL, '2025-10-27', 'completed', 45, 'Workout 7 for client 12, session 57', 'New PR on exercise 10'),
  (58, 13, 8, NULL, '2025-10-28', 'completed', 30, 'Workout 8 for client 13, session 58', NULL),
  (59, 14, 9, NULL, '2025-10-29', 'completed', 40, 'Workout 9 for client 14, session 59', 'New PR on exercise 20'),
  (60, 15, 10, NULL, '2025-10-30', 'completed', 60, 'Workout 10 for client 15, session 60', NULL),

  (61, 1, 1, 1, '2025-10-01', 'partial', 45, 'Workout 1 for client 1, session 61', NULL),
  (62, 2, 2, NULL, '2025-10-02', 'completed', 35, 'Workout 2 for client 2, session 62', NULL),
  (63, 3, 3, NULL, '2025-10-03', 'partial', 50, 'Workout 3 for client 3, session 63', NULL),
  (64, 4, 4, NULL, '2025-10-04', 'partial', 45, 'Workout 4 for client 4, session 64', NULL),
  (65, 5, 5, NULL, '2025-10-05', 'completed', 30, 'Workout 5 for client 5, session 65', NULL),
  (66, 6, 6, 1, '2025-10-06', 'partial', 30, 'Workout 6 for client 6, session 66', NULL),
  (67, 7, 7, NULL, '2025-10-07', 'completed', 45, 'Workout 7 for client 7, session 67', NULL),
  (68, 8, 8, NULL, '2025-10-08', 'not_started', 40, 'Workout 8 for client 8, session 68', NULL),
  (69, 9, 9, NULL, '2025-10-09', 'partial', 60, 'Workout 9 for client 9, session 69', NULL),
  (70, 10, 10, NULL, '2025-10-10', 'partial', 50, 'Workout 10 for client 10, session 70', NULL),
  (71, 11, 1, 1, '2025-10-11', 'partial', 60, 'Workout 1 for client 11, session 71', NULL),
  (72, 12, 2, NULL, '2025-10-12', 'completed', 30, 'Workout 2 for client 12, session 72', NULL),
  (73, 13, 3, NULL, '2025-10-13', 'completed', 35, 'Workout 3 for client 13, session 73', NULL),
  (74, 14, 4, NULL, '2025-10-14', 'completed', 45, 'Workout 4 for client 14, session 74', NULL),
  (75, 15, 5, 1, '2025-10-15', 'completed', 40, 'Workout 5 for client 15, session 75', NULL),
  (76, 1, 6, NULL, '2025-10-16', 'partial', 35, 'Workout 6 for client 1, session 76', NULL),
  (77, 2, 7, NULL, '2025-10-17', 'partial', 60, 'Workout 7 for client 2, session 77', NULL),
  (78, 3, 8, NULL, '2025-10-18', 'completed', 40, 'Workout 8 for client 3, session 78', NULL),
  (79, 4, 9, NULL, '2025-10-19', 'partial', 30, 'Workout 9 for client 4, session 79', NULL),
  (80, 5, 10, 1, '2025-10-20', 'completed', 60, 'Workout 10 for client 5, session 80', NULL);

DELETE FROM Trainer_Feedback;

INSERT INTO Trainer_Feedback (feedback_id, trainer_id, log_id, comment, created_at) VALUES
  (1, 1, 1, 'Great work today — maintain form on squats.', '2025-10-05 18:00:00'),
  (2, 2, 2, 'Push a little harder next time.', '2025-10-05 18:30:00'),
  (3, 3, 3, 'Good effort — try to hit full depth.', '2025-10-05 19:00:00'),
  (4, 4, 4, 'Nice session! Keep core tight.', '2025-10-05 19:30:00'),
  (5, 5, 5, 'Form is improving — stay consistent.', '2025-10-05 20:00:00'),
  (6, 6, 6, 'Increase reps by 1–2 next time.', '2025-10-05 20:30:00'),
  (7, 7, 7, 'Excellent pacing today.', '2025-10-05 21:00:00'),
  (8, 8, 8, 'Focus on breathing during sets.', '2025-10-05 21:30:00'),
  (9, 1, 9, 'Try adding a small weight increase.', '2025-10-05 22:00:00'),
  (10, 2, 10, 'Good control on movements.', '2025-10-05 22:30:00'),

  (11, 3, 11, 'Keep knees aligned with toes.', '2025-10-06 10:00:00'),
  (12, 4, 12, 'Nice job, stay consistent.', '2025-10-06 10:30:00'),
  (13, 5, 13, 'Great energy today.', '2025-10-06 11:00:00'),
  (14, 6, 14, 'Try slower tempo next session.', '2025-10-06 11:30:00'),
  (15, 7, 15, 'Watch shoulder position on presses.', '2025-10-06 12:00:00'),
  (16, 8, 16, 'Big improvement in endurance!', '2025-10-06 12:30:00'),
  (17, 1, 17, 'Try to hit all reps next time.', '2025-10-06 13:00:00'),
  (18, 2, 18, 'Keep elbows in on push movements.', '2025-10-06 13:30:00'),
  (19, 3, 19, 'Excellent posture today.', '2025-10-06 14:00:00'),
  (20, 4, 20, 'Focus on consistency.', '2025-10-06 14:30:00'),

  (21, 5, 21, 'Leg drive is improving.', '2025-10-06 15:00:00'),
  (22, 6, 22, 'Keep spine neutral.', '2025-10-06 15:30:00'),
  (23, 7, 23, 'Good session — stay focused.', '2025-10-06 16:00:00'),
  (24, 8, 24, 'Try increasing speed slightly.', '2025-10-06 16:30:00'),
  (25, 1, 25, 'Excellent technique today.', '2025-10-06 17:00:00'),
  (26, 2, 26, 'Good effort — maintain cadence.', '2025-10-06 17:30:00'),
  (27, 3, 27, 'Increase weight if comfortable.', '2025-10-06 18:00:00'),
  (28, 4, 28, 'Solid endurance performance.', '2025-10-06 18:30:00'),
  (29, 5, 29, 'Try a slower negative phase.', '2025-10-06 19:00:00'),
  (30, 6, 30, 'Great power output!', '2025-10-06 19:30:00'),

  (31, 7, 31, 'Nice improvement on cardio.', '2025-10-07 09:00:00'),
  (32, 8, 32, 'Try driving knees higher.', '2025-10-07 09:30:00'),
  (33, 1, 33, 'Good upper body stability.', '2025-10-07 10:00:00'),
  (34, 2, 34, 'Keep pushing — great momentum.', '2025-10-07 10:30:00'),
  (35, 3, 35, 'Smooth transitions between sets.', '2025-10-07 11:00:00'),
  (36, 4, 36, 'Try breathing rhythmically.', '2025-10-07 11:30:00'),
  (37, 5, 37, 'Good conditioning today.', '2025-10-07 12:00:00'),
  (38, 6, 38, 'Stay tight during core work.', '2025-10-07 12:30:00'),
  (39, 7, 39, 'Push a bit harder on the last set.', '2025-10-07 13:00:00'),
  (40, 8, 40, 'Your tempo is improving.', '2025-10-07 13:30:00'),

  (41, 1, 41, 'Very strong session today.', '2025-10-07 14:00:00'),
  (42, 2, 42, 'Try keeping hips square.', '2025-10-07 14:30:00'),
  (43, 3, 43, 'Consistency is paying off.', '2025-10-07 15:00:00'),
  (44, 4, 44, 'Excellent execution!', '2025-10-07 15:30:00'),
  (45, 5, 45, 'Keep shoulders relaxed.', '2025-10-07 16:00:00'),
  (46, 6, 46, 'Good session — strong progress.', '2025-10-07 16:30:00'),
  (47, 7, 47, 'Try slower reps for control.', '2025-10-07 17:00:00'),
  (48, 8, 48, 'Great job keeping pace steady.', '2025-10-07 17:30:00'),
  (49, 1, 49, 'Big improvement in technique.', '2025-10-07 18:00:00'),
  (50, 2, 50, 'Nice balance and control today.', '2025-10-07 18:30:00');
