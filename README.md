# Appli-Tracker

Appli-Tracker is a centralized dashboard designed to organize the job and co-op application process for university students, career coaches, hiring coordinators, and system administrators. Instead of juggling NUWorks, LinkedIn, Handshake, spreadsheets, and trackers, users get one platform where all applications, postings, analytics, performance metrics, and communication tools come together.

## Team Members

This project was developed by:

| Name                | Northeastern Email          |
| ------------------- | --------------------------- |
| **Alan Tai**        | tai.a@northeastern.edu      |
| **Brian Wong**      | wong.bria@northeastern.edu  |
| **Joshua Chan**     | chan.jos@northeastern.edu   |
| **Zoran Shamsi**    | shamsi.z@northeastern.edu   |
| **George Kressler** | kressler.g@northeastern.edu |

## Features & Personas

### James is a Student

- They can:
  - Add and manage job applications
  - Attach resumes and documents
  - Track platforms like LinkedIn, NUWorks, and Handshake.
  - View sorted application lists and status'

### Marcus is a Career Coach

- They can:
  - See a dashboard of all student activity
  - Track interviews, offers, and outcomes
  - Filter students by application stage
  - Send messages & receive notifications

### Sophia is a Hiring Coordinator

- They can:
  - Manage job postings across platforms
  - Track applicant counts and listing performance
  - Receive alerts on expired/expiring postings
  - Analyze platform effectiveness

### Jack is a System Administrator

- They can:
  - Monitor performance metrics and CPU usage
  - Review alerts and audit logs
  - Manage backups and restore points
  - Adjust retention policies and system configs

---

## 🛠 Tech Stack

- **Python**
- **Streamlit** (Frontend UI)
- **Flask** (REST API)
- **MySQL** (Database)
- **Docker & Docker Compose**

---

## ⚙️ Getting Started

The project runs entirely inside Docker.

### 1. Clone the repository

    git clone https://github.com/alantai26/Phase-3.git
    cd Phase-3

### 2. Create a `.env` file

    SECRET_KEY=yourSecretKeyHere

    DB_USER=root
    DB_PASSWORD=yourDBPasswordHere
    DB_HOST=db
    DB_PORT=3306
    DB_NAME=appliTracker

    MYSQL_ROOT_PASSWORD=yourDBPasswordHere

### 3. Start the project with Docker

    docker compose up -d

### 4. Access the application

- Streamlit UI:  
  **http://localhost:8501**

- API root (optional):  
  **http://localhost:4000**

### 5. Stopping the application

Stop all running containers:

    docker compose down

To reset database data as well:

    docker compose down -v

## REST API Overview

The backend contains Blueprints for:

- `/applications`
- `/resume`
- `/hiring`
- `/system-admin`

Each supports:

- GET
- POST
- PUT
- DELETE

based on user stories.

## Personas

- **James** - Student
- **Marcus** - Career Coach
- **Sophia** - Hiring Coordinator
- **Jack** - System Administrator
