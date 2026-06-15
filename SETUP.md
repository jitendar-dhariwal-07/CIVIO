# Setup Guide - CIVIO

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Database Setup](#database-setup)
4. [Backend Setup](#backend-setup)
5. [Frontend Setup](#frontend-setup)
6. [Running the Application](#running-the-application)
7. [Docker Setup](#docker-setup)
8. [Production Deployment](#production-deployment)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.10+** - Download from [python.org](https://www.python.org/downloads/)
- **Node.js 18+** - Download from [nodejs.org](https://nodejs.org/)
- **PostgreSQL 14+** - Download from [postgresql.org](https://www.postgresql.org/download/)
- **Git** - Download from [git-scm.com](https://git-scm.com/)

### Optional (Recommended)
- **Docker** - Download from [docker.com](https://www.docker.com/products/docker-desktop)
- **Redis** - For caching (optional, can use without)
- **VS Code** - Recommended editor

### Check Installations
```bash
# Check Python
python --version
# Output: Python 3.10.x or higher

# Check Node.js
node --version
npm --version
# Output: v18.x or higher

# Check PostgreSQL
psql --version
# Output: psql (PostgreSQL) 14.x or higher

# Check Git
git --version
# Output: git version 2.x.x or higher
```

---

## Local Development Setup

### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/yourusername/civio.git
cd civio

# Optional: Create a project folder for organization
# mkdir projects
# cd projects
# git clone ...
```

### Step 2: Create Directory Structure
The project should have this structure:
```
civio/
├── backend/
├── frontend/
├── database/
├── docker-compose.yml
├── README.md
└── PROJECT_DESIGN.md
```

If folders are missing, create them:
```bash
mkdir -p backend/db backend/models backend/services backend/routes
mkdir -p frontend/src/app frontend/src/components frontend/src/lib
mkdir -p database
```

---

## Database Setup

### Option 1: PostgreSQL Direct Installation (Windows/macOS/Linux)

#### 1.1 Install PostgreSQL
- Download and install from [postgresql.org](https://www.postgresql.org/download/)
- Remember the superuser password (default user: `postgres`)

#### 1.2 Create Database
```bash
# Open PostgreSQL terminal (psql)
# Windows: Open "SQL Shell (psql)" from Start menu
# macOS/Linux: Open terminal and run:
psql -U postgres

# In psql prompt, create database:
CREATE DATABASE civio_db;
CREATE USER civio_user WITH PASSWORD 'civio_password';
ALTER ROLE civio_user SET client_encoding TO 'utf8';
ALTER ROLE civio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE civio_user SET default_transaction_deferrable TO on;
ALTER ROLE civio_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE civio_db TO civio_user;
\q
```

#### 1.3 Verify Connection
```bash
psql -U civio_user -d civio_db -h localhost
# Should connect successfully
# Type: \q to exit
```

### Option 2: Docker PostgreSQL (Easiest)

```bash
# Pull PostgreSQL image
docker pull postgres:14

# Run PostgreSQL container
docker run --name civio_postgres \
  -e POSTGRES_DB=civio_db \
  -e POSTGRES_USER=civio_user \
  -e POSTGRES_PASSWORD=civio_password \
  -p 5432:5432 \
  -v civio_postgres_data:/var/lib/postgresql/data \
  -d postgres:14

# Verify running
docker ps | grep civio_postgres

# Stop container (later when done)
docker stop civio_postgres

# Start again
docker start civio_postgres
```

### Option 3: Cloud PostgreSQL (For Production)

**Neon.tech** (Free tier):
1. Go to [https://neon.tech](https://neon.tech)
2. Sign up with GitHub
3. Create a project
4. Copy connection string: `postgresql://user:password@host/dbname`

---

## Backend Setup

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) prefix in terminal)
```

#### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show (venv) prefix in terminal)
```

### Step 3: Install Dependencies

```bash
# Ensure you're in backend folder with venv activated
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
# Should show: FastAPI, SQLAlchemy, psycopg2, pydantic, etc.
```

**Required dependencies** (in requirements.txt):
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
python-dotenv==1.0.0
python-multipart==0.0.6
aiofiles==23.2.1
google-cloud-translate==3.14.0
redis==5.0.1
celery==5.3.4
```

### Step 4: Create Environment File

```bash
# In backend folder, create .env file
cat > .env << EOF
# Database
DATABASE_URL=postgresql://civio_user:civio_password@localhost:5432/civio_db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# API Keys (get from respective services)
GOOGLE_TRANSLATE_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here

# JWT Secret
SECRET_KEY=your_super_secret_key_change_this_in_production

# Environment
ENVIRONMENT=development
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Server
HOST=0.0.0.0
PORT=8000
EOF
```

**On Windows PowerShell:**
```powershell
$env:DATABASE_URL="postgresql://civio_user:civio_password@localhost:5432/civio_db"
# OR
# Create .env manually in VS Code
```

### Step 5: Initialize Database

```bash
# Create tables from schema
python -c "from database import init_db; init_db()"

# OR using psql directly
psql -U civio_user -d civio_db -f ../database/schema.sql

# Seed sample data
psql -U civio_user -d civio_db -f ../database/seed.sql
```

### Step 6: Start Backend Server

```bash
# Make sure venv is activated
# Run FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Output should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Backend Running ✅
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc Docs: http://localhost:8000/redoc

---

## Frontend Setup

### Step 1: Navigate to Frontend

```bash
cd ../frontend
```

### Step 2: Install Node Modules

```bash
# Install dependencies (takes 1-2 minutes)
npm install

# Verify installation
npm list | head -20
# Should show installed packages
```

### Step 3: Create Environment File

```bash
# Create .env.local
cat > .env.local << EOF
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Maps
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key_here

# Language
NEXT_PUBLIC_DEFAULT_LANGUAGE=en

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
EOF
```

### Step 4: Start Frontend Development Server

```bash
# Start Next.js dev server
npm run dev

# Output should show:
# ▲ Next.js 14.0.0
# - ready on 0.0.0.0:3000
```

### Frontend Running ✅
- App: http://localhost:3000
- Works live-reload on file changes

---

## Running the Application

### Terminal Setup (Recommended: 3 Terminals)

#### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

#### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

#### Terminal 3: Database Management (Optional)
```bash
# For monitoring database or running SQL queries
psql -U civio_user -d civio_db
```

### Access the Application

| Component | URL | Login | Notes |
|-----------|-----|-------|-------|
| Frontend | http://localhost:3000 | None needed | Open in browser |
| Backend API | http://localhost:8000 | None needed | Test with curl/Postman |
| API Docs | http://localhost:8000/docs | None needed | Swagger interactive docs |
| Database | localhost:5432 | civio_user | Via psql tool |

---

## Docker Setup

### Option 1: Docker Compose (Easiest - All-in-One)

```bash
# From project root (civio/)
cd ..

# Create docker-compose.yml (or use provided file)
# See section below for docker-compose.yml content

# Start all services
docker-compose up -d

# Check running containers
docker ps

# View logs
docker-compose logs -f backend  # Backend logs
docker-compose logs -f frontend # Frontend logs

# Stop everything
docker-compose down

# Remove volumes too (WARNING: deletes data)
docker-compose down -v
```

### Option 2: Manual Docker Build

```bash
# Build backend image
docker build -f Dockerfile.backend -t civio-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t civio-frontend:latest .

# Run backend container
docker run -d \
  --name civio-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://civio_user:civio_password@host.docker.internal:5432/civio_db \
  civio-backend:latest

# Run frontend container
docker run -d \
  --name civio-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  civio-frontend:latest
```

### Docker Compose File Content

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:14-alpine
    container_name: civio_postgres
    environment:
      POSTGRES_DB: civio_db
      POSTGRES_USER: civio_user
      POSTGRES_PASSWORD: civio_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
      - ./database/seed.sql:/docker-entrypoint-initdb.d/02-seed.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U civio_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: civio_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Backend API
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: civio_backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://civio_user:civio_password@postgres:5432/civio_db
      REDIS_URL: redis://redis:6379/0
      ENVIRONMENT: development
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app/backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: civio_frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
    volumes:
      - ./frontend:/app/frontend
      - /app/frontend/node_modules

volumes:
  postgres_data:
  redis_data:
```

---

## Production Deployment

### Option 1: Railway.app (Recommended for Hackathon)

1. **Create Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Connect your GitHub repository

2. **Configure Services**
   - Click "New" → "Database" → PostgreSQL
   - Click "New" → "GitHub Repo" → civio
   - Railway auto-detects Python/Node.js

3. **Set Environment Variables**
   - In Railway dashboard: Settings → Variables
   - Add all variables from `.env` files
   - Copy `DATABASE_URL` from PostgreSQL service

4. **Deploy**
   - Push to GitHub → Auto-deploys
   - Monitor logs in Railway dashboard
   - Access: `your-app.up.railway.app`

### Option 2: Vercel (Frontend) + Render (Backend)

**Frontend on Vercel:**
```bash
# Connect GitHub repo to Vercel
# Vercel auto-detects Next.js
# Add .env.local variables in Vercel dashboard
# Auto-deploys on git push
```

**Backend on Render:**
```bash
# 1. Go to render.com
# 2. Create account, connect GitHub
# 3. New Web Service → Select civio repo
# 4. Configure:
#    - Build Command: pip install -r backend/requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Add environment variables
# 6. Connect PostgreSQL database
# 7. Deploy
```

### Option 3: Self-Hosted (AWS/GCP/Azure)

```bash
# Using Docker containers on any cloud provider
# 1. Build Docker images
# 2. Push to container registry (ECR/GCR/ACR)
# 3. Deploy using:
#    - AWS ECS / Fargate
#    - GCP Cloud Run
#    - Azure Container Instances
#    - Kubernetes (EKS/GKE/AKS)
```

---

## Troubleshooting

### Python/Backend Issues

**Issue: `ModuleNotFoundError: No module named 'fastapi'`**
```bash
# Solution: Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Then install requirements
pip install -r requirements.txt
```

**Issue: `psycopg2.OperationalError: could not connect to database`**
```bash
# Check PostgreSQL is running
# Check DATABASE_URL is correct in .env
# Test connection:
psql -U civio_user -d civio_db -h localhost

# Restart PostgreSQL
# Windows: Services > PostgreSQL
# macOS: brew services restart postgresql
# Linux: sudo systemctl restart postgresql
```

**Issue: `CORS error when frontend calls backend`**
```bash
# Check ALLOWED_ORIGINS in backend/.env includes frontend URL
ALLOWED_ORIGINS=http://localhost:3000

# Check backend is using CORS middleware (in main.py)
```

### Frontend/Node.js Issues

**Issue: `npm: command not found`**
```bash
# Install Node.js from nodejs.org
# Check installation:
node --version
npm --version
```

**Issue: `Port 3000 already in use`**
```bash
# Change port in frontend
npm run dev -- -p 3001

# OR kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :3000
kill -9 <PID>
```

### Database Issues

**Issue: `FATAL: password authentication failed for user`**
```bash
# Reset PostgreSQL password
# Windows: Use pgAdmin to reset
# macOS/Linux:
sudo -u postgres psql
ALTER USER civio_user WITH PASSWORD 'civio_password';
\q
```

**Issue: `Database civio_db does not exist`**
```bash
# Create database
psql -U postgres
CREATE DATABASE civio_db;
CREATE USER civio_user WITH PASSWORD 'civio_password';
GRANT ALL PRIVILEGES ON DATABASE civio_db TO civio_user;
\q

# Then run schema
psql -U civio_user -d civio_db -f database/schema.sql
```

### Docker Issues

**Issue: `docker: command not found`**
```bash
# Install Docker from docker.com
# Restart terminal after installation
```

**Issue: `Port 5432 already in use`**
```bash
# Change port in docker-compose.yml
ports:
  - "5433:5432"  # Use 5433 instead of 5432
```

**Issue: Containers not communicating**
```bash
# Restart docker daemon
docker system prune  # Clean up
docker-compose down
docker-compose up -d --build
```

### API Testing

**Test Backend Health:**
```bash
# Using curl
curl -X GET http://localhost:8000/health

# Using PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health

# Using browser
# Visit: http://localhost:8000/health
```

**Test API Documentation:**
```bash
# Swagger UI (interactive):
http://localhost:8000/docs

# ReDoc (read-only):
http://localhost:8000/redoc
```

---

## Performance Tuning

### Backend Optimization
```python
# In config.py
- Enable gzip compression
- Configure database connection pooling
- Use async/await properly
- Add caching for frequently accessed schemes
```

### Frontend Optimization
```javascript
// In next.config.ts
- Enable image optimization
- Implement dynamic code splitting
- Use compression
- Optimize bundle size
```

### Database Optimization
```sql
-- Create indexes for common queries
CREATE INDEX idx_schemes_state ON schemes(eligible_states);
CREATE INDEX idx_complaints_category ON complaints(category);
CREATE INDEX idx_complaints_location ON complaints(location);
CREATE INDEX idx_complaints_created ON complaints(created_at DESC);

-- Analyze query plans
EXPLAIN ANALYZE SELECT * FROM schemes WHERE eligible_states LIKE '%Karnataka%';
```

---

## Getting Help

- **Documentation**: See [README.md](README.md) and [PROJECT_DESIGN.md](PROJECT_DESIGN.md)
- **API Docs**: Open http://localhost:8000/docs in browser
- **Issues**: [GitHub Issues](https://github.com/yourusername/civio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/civio/discussions)

---

*Last Updated: January 2024*
