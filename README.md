# CIVIO: AI-Powered Multilingual Civic Assistance Platform

[![GitHub](https://img.shields.io/badge/GitHub-Civio-blue?logo=github)](https://github.com/yourusername/civio)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Hackathon%20MVP-orange)]()

**CIVIO** is a unified platform that empowers Indian citizens to discover government benefits they're eligible for and intelligently route civic complaints to the right departments. Built for the hackathon with scalability to all Indian states in mind.

## 🎯 What is CIVIO?

CIVIO solves two critical problems:

### 1. **Government Scheme Navigator** 📋
- Discover which government benefits you're eligible for in minutes
- Support for 120+ schemes across central, state, and local levels
- Eligibility matching based on age, income, occupation, location, caste/category, and available documents
- Multilingual support (English, Hindi, Tamil, Telugu, and more)
- Direct links to official application portals

### 2. **Civic Complaint Intelligence** 🚨
- Submit complaints (text + image) about civic issues
- AI-powered automatic categorization (Roads, Water, Electricity, Sanitation, Transport, Parks)
- Smart priority assignment
- Duplicate detection to prevent redundant reports
- Real-time status tracking
- Heatmap visualization of problem hotspots

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis (optional, for caching)
- Git

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/civio.git
cd civio
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://username:password@localhost:5432/civio_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your_secret_key_here
GOOGLE_TRANSLATE_API_KEY=your_api_key
ENVIRONMENT=development
EOF

# Initialize database
python -c "from database import init_db; init_db()"

# (Optional) Seed sample data
python -c "from database import seed_db; seed_db()"

# Start backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`
API documentation (Swagger): `http://localhost:8000/docs`

#### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key
EOF

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

#### 4. Database Setup

```bash
# Option 1: Using Docker Compose (Recommended)
docker-compose up -d

# Option 2: Manual PostgreSQL setup
createdb civio_db
psql civio_db < database/schema.sql
psql civio_db < database/seed.sql
```

### 5. Run Everything Together

```bash
# From project root, if you have docker-compose.yml
docker-compose up
```

---

## 📁 Project Structure

```
civio/
├── backend/                          # Python FastAPI backend
│   ├── config.py                     # Configuration management
│   ├── database.py                   # Database connection & setup
│   ├── main.py                       # FastAPI application entry point
│   ├── requirements.txt               # Python dependencies
│   ├── db/
│   │   ├── __init__.py
│   │   ├── crud.py                   # Database CRUD operations
│   │   └── models.py                 # SQLAlchemy models
│   ├── models/
│   │   ├── __init__.py
│   │   ├── common.py                 # Common response models
│   │   ├── complaint.py              # Complaint data models
│   │   ├── scheme.py                 # Scheme data models
│   │   └── user.py                   # User profile models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── complaint_service.py      # Complaint handling logic
│   │   ├── eligibility_service.py    # Scheme eligibility matching
│   │   ├── embedding_service.py      # Text embeddings for duplicate detection
│   │   ├── gemini_service.py         # Google Gemini AI integration
│   │   ├── hotspot_service.py        # Hotspot analysis
│   │   └── translation_service.py    # Multilingual translation
│   └── routes/                       # API endpoint definitions
│       ├── __init__.py
│       ├── schemes.py                # /api/schemes endpoints
│       ├── complaints.py             # /api/complaints endpoints
│       ├── admin.py                  # /api/admin endpoints
│       └── health.py                 # Health check endpoint
│
├── frontend/                         # Next.js React frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx            # Root layout
│   │   │   ├── page.tsx              # Home page
│   │   │   ├── globals.css           # Global styles
│   │   │   ├── schemes/
│   │   │   │   ├── page.tsx          # Scheme navigator page
│   │   │   │   ├── [id]/page.tsx     # Scheme details page
│   │   │   │   └── questionnaire.tsx # Eligibility form
│   │   │   ├── complaints/
│   │   │   │   ├── page.tsx          # Complaint submission page
│   │   │   │   ├── track/[id].tsx    # Complaint tracking page
│   │   │   │   └── map.tsx           # Hotspot map view
│   │   │   └── admin/
│   │   │       ├── page.tsx          # Admin dashboard
│   │   │       └── complaints/       # Complaint management
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── LanguageSwitcher.tsx  # i18n language selection
│   │   │   ├── SchemeCard.tsx
│   │   │   ├── ComplaintForm.tsx
│   │   │   ├── Map.tsx
│   │   │   └── Charts.tsx
│   │   ├── context/
│   │   │   └── LanguageContext.tsx   # Multilingual support
│   │   ├── hooks/
│   │   │   ├── useSchemes.ts         # Scheme API hooks
│   │   │   ├── useComplaints.ts      # Complaint API hooks
│   │   │   └── useLocation.ts        # Location/GPS hooks
│   │   ├── lib/
│   │   │   ├── api.ts                # API client
│   │   │   ├── translations.ts       # i18n configuration
│   │   │   └── types.ts              # TypeScript type definitions
│   │   └── styles/
│   │       └── variables.css         # CSS variables & theme
│   ├── public/
│   │   └── locales/
│   │       ├── en/common.json        # English translations
│   │       ├── hi/common.json        # Hindi translations
│   │       ├── ta/common.json        # Tamil translations
│   │       └── ...                   # Other language translations
│   └── .env.local                    # Environment variables (local)
│
├── database/
│   ├── schema.sql                    # Database schema
│   └── seed.sql                      # Sample data
│
├── docker-compose.yml                # Docker compose for easy local setup
├── Dockerfile.backend                # Backend container definition
├── Dockerfile.frontend               # Frontend container definition
├── PROJECT_DESIGN.md                 # Detailed project design document
├── README.md                         # This file
├── SETUP.md                          # Detailed setup instructions
├── API_DOCUMENTATION.md              # API endpoint documentation
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # MIT License
└── .github/
    └── workflows/
        └── ci-cd.yml                 # GitHub Actions CI/CD pipeline
```

---

## 🔧 Configuration

### Backend Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/civio_db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# API Keys
GOOGLE_TRANSLATE_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here
AWS_ACCESS_KEY_ID=your_key (for image analysis)
AWS_SECRET_ACCESS_KEY=your_key

# Application
SECRET_KEY=your_secret_key_for_jwt
ENVIRONMENT=development  # or production
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Environment Variables
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Maps
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_api_key

# Translation
NEXT_PUBLIC_DEFAULT_LANGUAGE=en

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
```

---

## 📊 Key Features in Detail

### Feature 1: Scheme Navigator

**User Flow:**
1. User selects language (English/Hindi/Tamil/etc.)
2. Fills in personal profile (Age, Income, Occupation, Location, etc.)
3. System matches eligibility rules instantly
4. Shows list of applicable schemes ranked by relevance
5. Click on scheme → View full details, documents checklist, official link
6. Bookmark schemes or proceed to official application portal

**Example:**
```
Input: 35-year-old small business owner in Karnataka earning ₹4 lakh/year
Output: 12 matching schemes including:
  • PM Mudra Loan Scheme (₹10 lakh subsidy)
  • Karnataka Small Business Grant (₹2 lakh)
  • SIDBI Entrepreneurship Support (0% interest initially)
```

### Feature 2: Civic Complaint System

**User Flow:**
1. Click "Report Issue"
2. Describe problem in native language (text + optional image)
3. System auto-detects location (GPS or map picker)
4. AI categorizes complaint & assigns priority automatically
5. Generate unique complaint ID
6. User can track status in real-time

**Example:**
```
Input: "Streetlight near ABC School broken for 2 weeks" + photo
Output:
  ID: CIVIO-2024-001234
  Category: Electricity (95% confidence)
  Priority: Medium
  Department: Electrical Maintenance
  Status: Assigned to North Delhi Zone
  Estimated Resolution: 2-3 days
```

### Feature 3: Admin Dashboard

**For Government Officials:**
- View pending complaints
- Filter by category, priority, status, location
- Assign to teams
- Update status
- View department performance metrics
- Identify complaint hotspots on map
- Analyze trends and patterns

---

## 🤖 AI/ML Components

### 1. Complaint Categorization
- **Model**: Text classification (SVM/BERT)
- **Input**: Complaint text + optional image
- **Output**: Category + confidence score
- **Training**: Fine-tuned on Indian complaint dataset

### 2. Priority Assignment
- **Algorithm**: Rule-based + ML scoring
- **Factors**: Category, location density, time, critical keywords
- **Output**: Low/Medium/High/Critical

### 3. Duplicate Detection
- **Method**: Embedding similarity + geospatial matching
- **Threshold**: 0.85 cosine similarity + 5km radius + 7 days
- **Output**: Merge decision with vote count

### 4. Hotspot Analysis
- **Method**: K-means clustering on GPS coordinates
- **Frequency**: Daily batch processing
- **Output**: Heatmap, trend analysis, recommendations

### 5. Multilingual Support
- **Translation**: Google Translate API / IndicTrans
- **Language Detection**: Auto-detect from user input
- **Supported**: 7 major Indian languages (expandable to 22)

---

## 📱 API Endpoints (Key Examples)

### Scheme Navigator
```
GET    /api/schemes                    # List all schemes
POST   /api/schemes/match              # Match eligible schemes for user
GET    /api/schemes/{id}               # Get scheme details
POST   /api/users/profile              # Save user profile
GET    /api/users/{id}/bookmarks       # Get bookmarked schemes
```

### Complaints
```
POST   /api/complaints                 # Submit new complaint
GET    /api/complaints/{id}            # Get complaint status
GET    /api/complaints/track/{id}      # Track complaint
POST   /api/complaints/{id}/update     # Admin: Update status
GET    /api/complaints/map             # Get all complaints for map
GET    /api/hotspots                   # Get hotspot data
```

### Admin
```
GET    /api/admin/dashboard            # Dashboard metrics
GET    /api/admin/complaints           # All complaints (admin)
GET    /api/admin/analytics            # Analytics & trends
POST   /api/admin/complaints/{id}/assign  # Assign complaint
```

**Full API documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🌐 Multilingual Support

CIVIO supports multiple Indian languages with more coming soon:

- ✅ **English** (100%)
- ✅ **Hindi** (100%)
- ✅ **Tamil** (95%)
- 🚧 **Telugu** (In Progress)
- 🚧 **Kannada** (Planned)
- 🚧 **Bengali** (Planned)
- 🚧 **Marathi** (Planned)

**Language Selection**: Users can choose language from the home page or settings.

**Translation Approach**:
- Static UI strings: Stored in `/frontend/public/locales/{lang}/common.json`
- Scheme content: Stored in database with language variants
- Real-time translation: Google Translate API for user inputs

---

## 🗄️ Database Schema

### Main Tables
```
users
  ├─ id (PK)
  ├─ phone
  ├─ email
  ├─ language_preference
  └─ profile_data (JSON)

schemes
  ├─ id (PK)
  ├─ name
  ├─ description
  ├─ category
  ├─ eligible_states
  ├─ eligibility_rules (JSON)
  └─ required_documents

complaints
  ├─ id (PK)
  ├─ user_id (FK)
  ├─ title
  ├─ description
  ├─ category
  ├─ priority
  ├─ status
  ├─ location (lat, lng)
  ├─ image_url
  └─ created_at

assignments
  ├─ id (PK)
  ├─ complaint_id (FK)
  ├─ department
  ├─ assigned_to
  └─ status

hotspots
  ├─ id (PK)
  ├─ location_cluster
  ├─ category
  ├─ complaint_count
  └─ trend
```

See [database/schema.sql](database/schema.sql) for full schema.

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=.  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Integration Tests
```bash
npm run test:integration
```

---

## 📦 Deployment

### Local Development
```bash
# Option 1: Traditional setup (see Quick Start above)

# Option 2: Docker Compose (Recommended)
docker-compose up -d
```

### Production Deployment

#### Option 1: Railway.app (Recommended for Hackathon)
```bash
# Connect GitHub repo to Railway
# Railway auto-detects Python/Node.js
# Configure env variables in Railway dashboard
# Auto-deploys on git push
```

#### Option 2: Vercel + Heroku
```bash
# Frontend: Deploy to Vercel (git push)
# Backend: Deploy to Heroku (buildpack for Python + PostgreSQL add-on)
```

#### Option 3: AWS / GCP / Azure
```bash
# Use CloudFormation / Terraform for infrastructure
# Docker images for both frontend and backend
# RDS for PostgreSQL
# ElastiCache for Redis
```

**See [SETUP.md](SETUP.md) for detailed deployment instructions.**

---

## 🚀 MVP Scope (What's Included)

✅ **Scheme Navigator:**
- ✅ User registration & profile
- ✅ Eligibility questionnaire
- ✅ Scheme matching engine
- ✅ Scheme search & filtering
- ✅ Document checklist
- ✅ Links to official portals

✅ **Complaint System:**
- ✅ Complaint submission (text + image)
- ✅ Auto-categorization (6 categories)
- ✅ Priority assignment
- ✅ Complaint tracking
- ✅ Map visualization
- ✅ Admin dashboard

✅ **Multilingual:**
- ✅ English + Hindi UI
- ✅ Complaint submission in 2 languages
- ✅ Scheme browsing in 2 languages

❌ **Out of Scope (Post-Hackathon):**
- Real government integration (API only)
- Advanced ML models
- SMS/Email notifications (mocked)
- Full state-wise data (top 5 states only)
- Advanced analytics

---

## 🔄 Workflow for Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

Built for the Hackathon by:
- **[Your Name]** - Full Stack Development
- **[Team Member 2]** - AI/ML Components
- **[Team Member 3]** - UI/UX Design
- **[Team Member 4]** - DevOps & Deployment

---

## 🤝 Support & Feedback

- **Issues**: [GitHub Issues](https://github.com/yourusername/civio/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/civio/discussions)
- **Email**: civio@example.com

---

## 🙏 Acknowledgments

- Government of India for open data sources
- MyScheme.gov.in for scheme reference
- Data.gov.in for public datasets
- Open-source community (FastAPI, Next.js, PostgreSQL, etc.)

---

## 📞 Contact

For questions or suggestions about CIVIO:
- **Project Lead**: [Your Email]
- **GitHub**: [Your GitHub Profile]
- **Twitter**: [@civio_india](https://twitter.com/civio_india)

---

## 🗓️ Roadmap

### Completed ✅
- [x] Project design & architecture
- [x] Database schema
- [x] API scaffolding
- [x] Frontend UI components
- [x] Basic scheme matching
- [x] Complaint categorization
- [x] MVP feature set

### In Progress 🚧
- [ ] Deployment & testing
- [ ] Documentation completion
- [ ] Performance optimization
- [ ] Security audit

### Planned 📅
- [ ] Real government integrations
- [ ] Advanced ML models
- [ ] All 28 states + 8 UTs coverage
- [ ] All 22 official languages
- [ ] Mobile apps (iOS/Android)
- [ ] Voice-first interface
- [ ] Blockchain for transparency

---

**Made with ❤️ for India's citizens**

---

*Last Updated: January 2024*
*For the latest version, visit: [https://github.com/yourusername/civio](https://github.com/yourusername/civio)*
