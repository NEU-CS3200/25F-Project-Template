# FitFlow — Team Project


A Streamlit client portal plus Flask REST API for tracking training programs, logging workouts, and showcasing progress with a MySQL backend. Containers are orchestrated with Docker Compose so the app, API, and database start together and seed automatically from the bundled SQL scripts.


## Team
- Ranya Jain 
- Laila Alston 
- Malk Abou Hadiba 
- Alex Quintyne 


## Tech & Services
- Frontend: Streamlit (Python)
- Backend: Flask REST API
- Database: MySQL seeded from `database-files/*.sql` (runs in alphabetical order on first startup)
- Containerization: Docker & Docker Compose
- Extras: optional notebooks/scripts in `ml-src` for model experimentation


## Repository Layout
- `app/` – Streamlit UI (`app/src/pages` holds the pages)
- `api/` – Flask API (`api/backend` for routes/services)
- `database-files/` – SQL used to initialize MySQL (auto-run on first container create)
- `datasets/` – datasets for experiments
- `docker-compose.yaml` – spins up app, API, and DB together


## Prerequisites
- Docker Desktop 
- Optional for local-only dev: Python 3.11 + `pip` if you want to run components outside Docker


## Quick Start (Docker)
1) Clone the repo (ensure it is public per course requirements). 
2) Create `api/.env` with your secrets (leave blanks here and fill locally):
  ```env
  SECRET_KEY=
  DB_USER=
  DB_PASSWORD=
  DB_HOST=db
  DB_PORT=3306
  DB_NAME=fitflow
  MYSQL_ROOT_PASSWORD=
  ```
3) Build and start everything:
  ```bash
  docker compose up -d --build
  ```
  - First run: MySQL executes every `.sql` in `database-files/` alphabetically to seed schema/data.
  - App: http://localhost:8501 
  - API: http://localhost:4000 
  - DB (inside Compose network): host `db`, port `3306`.
4) Check status/logs (optional):
  ```bash
  docker compose ps
  docker compose logs -f db   # watch SQL init
  docker compose logs -f api  # API startup/route logs
  ```
5) Stop/clean:
  ```bash
  docker compose down              # stop containers
  docker compose down -v           # stop and remove volumes (wipes DB data)
  ```


### Updating SQL seeds
If you modify files in `database-files/`, recreate the DB container to re-run the scripts:
```bash
docker compose down db -v
docker compose up db -d
```


## Local Development (without Docker)
- Frontend:
 ```bash
 cd app
 pip install -r src/requirements.txt
 streamlit run src/Home.py
 ```
- Backend:
 ```bash
 cd api
 pip install -r requirements.txt
 flask --app backend_app.py run
 ```
Make sure a MySQL instance is reachable and matches the `api/.env` values when running outside Compose.




Enjoy the demo-friendly Fitflow version now!
