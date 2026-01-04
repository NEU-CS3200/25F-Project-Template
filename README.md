Fall 2025 CS 3200 DataDunkers Project

This repo is for our team DataDunkers - Caitlin Heery, Aarav Sikriwal, Sebastian Romero, Krish Gupta. We created a data-driven web app CourtVision. Our mission is to create a thorough basketball scouting and analytics platform that connects players, scouts, and analysts through real-time statistics tracking, video analysis, and data-driven insights.
Presentation Link - 
Prerequisites:

A GitHub account
A terminal-based or GUI git client
VSCode with the Python Plugin
A distribution of Python running on laptop (Choco (for Windows), brew (for Macs), miniconda, Anaconda, etc).
Docker Desktop installed and running

Current Project Components
Currently, there are three major components which will each run in their own respective Docker Containers:

Streamlit App in the ./app directory
Flask REST API in the ./api directory
SQL files for your data model and database in the ./database-files directory

Setting Up Personal Repo

In GitHub, click the fork button in the upper right corner of the repo screen.
When prompted, give the new repo a unique name, also including your last name and the word 'personal'.
Once the fork has been created, clone YOUR forked version of the repo to your computer.
Set up the .env file in the api folder based on the .env.template file (if applicable).
Start the docker containers.

Controlling the Containers

docker compose up -d to start all the containers in the background
docker compose down to shutdown and delete the containers
docker compose up db -d only start the database container (replace db with api or app as needed)
docker compose stop to "turn off" the containers but not delete them.

Accessing the Application
Once containers are running:

Web App: http://localhost:8501
API: http://localhost:4000
MySQL: localhost:3306

Handling User Role Access and Control in the "CourtVision" Project
In the CourtVision project, we developed a dynamic system that manages role-based access for different user types, such as players, scouts, data analysts, and system administrators. Each user role interacts with unique features tailored to their responsibilities while sharing some overlapping functionality. This concept ensures a secure, intuitive, and personalized user experience.
Our implementation demonstrates how to integrate this seamlessly within a Streamlit-powered app while managing user interactions and navigation efficiently. Understanding CourtVision may take a bit of exploration into the code and some time. Some highlights are below.
Custom Sidebar Navigation: The default sidebar is replaced with role-specific navigation managed via app/src/modules/nav.py. Links are generated based on user roles.
Role Assignment: Users select their role on the homepage of the app (app/src/Home.py), setting their session variables for role, authentication, and personalization. The app redirects users to their role-specific dashboards where they can further interact with their personalized interface.
Role-Specific Pages: Pages are categorized by role (e.g., Players, Scouts, Analysts, Admins). Each page displays relevant navigation links via the SideBarLinks function.
Tailored Features:

Players: View profile, upload highlight videos, track game statistics, review scout reports.
Scouts: Write player reports, annotate game footage, track future games, view player videos.
Data Analysts: Create dashboards, export data, analyze performance trends, generate insights.
System Administrators: Verify scout accounts, update user profiles, remove fraudulent data, manage system integrity.

Key API Routes:
Players (/players)

GET /{id}/profile - Get player profile with bio, stats, and team info
GET /{id}/game-stats - Get all game statistics across the season
POST /{id}/game-stats - Add new game statistics
POST /{id}/videos - Upload highlight video
GET /{id}/scout-reports - Get scout feedback and reports

Scouts (/scouts)

GET /players/{id}/videos - Get all player highlight videos
GET /players/{id}/future-games - Get upcoming scheduled games
POST /{scout_id}/players/{player_id}/report/footage - Add footage to player report
POST /footage/{id}/annotations - Add timestamped annotations to video

Analysts (/analysts)

GET /dashboards - List all analytics dashboards
GET /export-requests - List data export requests
GET /exports/{id} - Get export details with a download URL
DELETE /dashboards/{id}/remove - Remove a dashboard

Admins (/admins)

PUT /players/{id}/update - Update profile information for player
PUT /scouts/{id}/update - Update scout profile
PUT /scouts/{id}/verify - Verify and activate scout account
DELETE /players/{id}/remove - Remove player for fraud
DELETE /stats/fraudulent/{id}/remove - Remove fraudulent statistics

Database Schema Highlights

Players - Player profiles with bio, stats, and team affiliations
Teams - Team information and league details
Games - Game schedules with opponents, venues, and tournaments
GameStats - Detailed per-game player statistics
SeasonStats - Aggregated season performance metrics
Scouts - Scout profiles and credentials
PlayerReports - Scout evaluations with strengths, weaknesses, and grades
Footage - Video highlights and game footage URLs
Annotations - Timestamped video annotations
Schools - College and university information
Offers - Scholarship offers to players
Dashboard - Analytics dashboards and visualizations

Testing the API
bash# Test player profile
curl http://localhost:4000/players/4/profile

# Add game stats
curl -X POST http://localhost:4000/players/4/game-stats \
  -H "Content-Type: application/json" \
  -d '{"gameID": 1, "points": 24, "rebounds": 8, "assists": 6}'

# Upload video
curl -X POST http://localhost:4000/players/4/videos \
  -H "Content-Type: application/json" \
  -d '{"gameID": 1, "URL": "https://youtube.com/watch?v=test"}'
Important Tips

Hot Reloading - Code changes auto-reload. Click "Always Rerun" in Streamlit.
MySQL Container - SQL files in database-files/ run in alphabetical order on first creation.
Database Updates - Must recreate container with docker compose down -v to apply schema changes.
Check Logs - Use docker logs <container-name> to debug issues.

Troubleshooting
Database connection error:
bashdocker exec -it mysql_db mysql -u root -p'courtvision_root_2024'
GRANT ALL PRIVILEGES ON courtvision.* TO 'courtvision_user'@'%';
FLUSH PRIVILEGES;
API not starting: Check docker logs web-api for syntax errors.
Reset everything: docker compose down -v && docker compose up -d
Tech Stack
Flask • Streamlit • MySQL • Docker • PyMySQL
