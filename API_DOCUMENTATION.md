# API Documentation - CIVIO

Complete REST API documentation for CIVIO backend.

## Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com/api`

## API Endpoints Reference

### Table of Contents
1. [Health Check](#health-check)
2. [Authentication](#authentication)
3. [Users & Profiles](#users--profiles)
4. [Schemes](#schemes)
5. [Complaints](#complaints)
6. [Admin](#admin)
7. [Error Responses](#error-responses)

---

## Health Check

### Get API Status
```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

---

## Authentication

Currently, CIVIO uses simple token-based authentication. JWT support is planned.

### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "phone": "+91-9876543210",
  "email": "user@example.com",
  "language_preference": "hi"
}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "phone": "+91-9876543210",
  "email": "user@example.com",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "phone": "+91-9876543210"
}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 86400
}
```

---

## Users & Profiles

### Create User Profile
```
POST /api/users/{user_id}/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "age": 35,
  "income_annual": 400000,
  "income_source": "small_business",
  "occupation": "business_owner",
  "state": "Karnataka",
  "district": "Bangalore",
  "caste_category": "general",
  "family_status": "married",
  "education_level": "graduate",
  "available_documents": ["aadhar", "pan", "income_certificate"],
  "has_disability": false,
  "is_senior_citizen": false,
  "is_woman": false,
  "is_veteran": false
}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "profile_id": "prof_789012",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get User Profile
```
GET /api/users/{user_id}/profile
Authorization: Bearer {token}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "age": 35,
  "income_annual": 400000,
  "state": "Karnataka",
  "occupation": "business_owner",
  "available_documents": ["aadhar", "pan", "income_certificate"],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

### Update User Profile
```
PATCH /api/users/{user_id}/profile
Authorization: Bearer {token}
Content-Type: application/json

{
  "age": 36,
  "income_annual": 450000
}
```

**Response:**
```json
{
  "user_id": "usr_123456",
  "profile_id": "prof_789012",
  "updated_at": "2024-01-15T11:05:00Z"
}
```

---

## Schemes

### List All Schemes
```
GET /api/schemes
Query Parameters:
  - page: integer (default: 1)
  - limit: integer (default: 20)
  - state: string (optional, filter by state)
  - category: string (optional, e.g., "education", "health", "agriculture")
  - search: string (optional, search by name/description)
  - language: string (optional, default: "en")
```

**Example:**
```
GET /api/schemes?page=1&limit=10&state=Karnataka&language=hi
```

**Response:**
```json
{
  "total": 156,
  "page": 1,
  "limit": 10,
  "schemes": [
    {
      "id": "scheme_001",
      "name": "PM Mudra Loan Scheme",
      "description": "Government-backed loans for small businesses",
      "category": "business",
      "eligible_states": ["all"],
      "min_amount": 50000,
      "max_amount": 1000000,
      "application_deadline": "2024-12-31",
      "official_link": "https://www.mudrascheme.gov.in",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Get Scheme Details
```
GET /api/schemes/{scheme_id}
Query Parameters:
  - language: string (optional, default: "en")
```

**Response:**
```json
{
  "id": "scheme_001",
  "name": "PM Mudra Loan Scheme",
  "description": "Government-backed loans for small businesses",
  "long_description": "PM MUDRA Yojana aims to promote the growth of small and micro enterprises...",
  "category": "business",
  "eligible_states": ["all"],
  "eligibility_criteria": {
    "min_age": 18,
    "max_age": null,
    "occupation": ["business_owner", "entrepreneur"],
    "education_required": false,
    "income_limit": null,
    "caste_category": ["general", "obc", "sc", "st"],
    "required_documents": ["aadhar", "pan", "business_registration"]
  },
  "benefits": {
    "loan_amount": "50000 - 10 lakh",
    "interest_rate": "Variable (MCLR based)",
    "tenure": "5-7 years",
    "collateral": "No collateral"
  },
  "documents_checklist": [
    {
      "document": "Aadhar Card",
      "mandatory": true,
      "digital_acceptable": true
    },
    {
      "document": "PAN Card",
      "mandatory": true,
      "digital_acceptable": true
    },
    {
      "document": "Bank Statement (6 months)",
      "mandatory": false,
      "digital_acceptable": true
    }
  ],
  "application_process": [
    "Visit authorized bank",
    "Fill application form",
    "Submit documents",
    "Get approval in 5-7 days"
  ],
  "contact": {
    "ministry": "Ministry of Small Business",
    "website": "https://www.mudrascheme.gov.in",
    "email": "info@mudra.org.in",
    "phone": "1800-123-4567"
  },
  "state_variations": {
    "Karnataka": {
      "additional_subsidy": 25000,
      "special_requirements": "Karnataka residency 2+ years"
    }
  },
  "faq": [
    {
      "question": "Can I apply if I have existing loans?",
      "answer": "Yes, but total liability should not exceed 10 lakhs"
    }
  ],
  "official_link": "https://www.mudrascheme.gov.in/apply",
  "application_deadline": "2024-12-31",
  "created_at": "2024-01-01T00:00:00Z"
}
```

### Find Eligible Schemes for User
```
POST /api/schemes/match
Authorization: Bearer {token}
Content-Type: application/json

{
  "user_id": "usr_123456"
}
```

**or pass profile directly:**
```
POST /api/schemes/match
Content-Type: application/json

{
  "age": 35,
  "income_annual": 400000,
  "occupation": "business_owner",
  "state": "Karnataka",
  "caste_category": "general",
  "available_documents": ["aadhar", "pan"],
  "education_level": "graduate"
}
```

**Response:**
```json
{
  "matched_schemes": [
    {
      "id": "scheme_001",
      "name": "PM Mudra Loan Scheme",
      "relevance_score": 95,
      "reason": "All eligibility criteria met",
      "benefits": "₹50,000 - ₹10,00,000 loan",
      "missing_documents": [],
      "state_specific_info": "Karnataka: Additional ₹25,000 subsidy"
    },
    {
      "id": "scheme_012",
      "name": "Startup India Scheme",
      "relevance_score": 87,
      "reason": "Mostly eligible, education preferred",
      "benefits": "Tax benefits, reduced compliance burden",
      "missing_documents": [],
      "state_specific_info": null
    }
  ],
  "total_matched": 12,
  "evaluation_timestamp": "2024-01-15T10:30:00Z"
}
```

### Bookmark Scheme
```
POST /api/users/{user_id}/bookmarks
Authorization: Bearer {token}
Content-Type: application/json

{
  "scheme_id": "scheme_001"
}
```

**Response:**
```json
{
  "bookmark_id": "bm_123456",
  "user_id": "usr_123456",
  "scheme_id": "scheme_001",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Get User's Bookmarked Schemes
```
GET /api/users/{user_id}/bookmarks
Authorization: Bearer {token}
Query Parameters:
  - page: integer (default: 1)
  - limit: integer (default: 20)
```

**Response:**
```json
{
  "bookmarks": [
    {
      "bookmark_id": "bm_123456",
      "scheme_id": "scheme_001",
      "scheme_name": "PM Mudra Loan Scheme",
      "bookmarked_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 20
}
```

---

## Complaints

### Submit Complaint
```
POST /api/complaints
Content-Type: multipart/form-data

{
  "title": "Streetlight not working",
  "description": "The streetlight near ABC School hasn't worked for 2 weeks",
  "language": "en",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address": "ABC School, New Delhi"
  },
  "category": "electricity",
  "image": <binary_file> (optional),
  "user_phone": "+91-9876543210" (optional),
  "user_email": "user@example.com" (optional)
}
```

**Response:**
```json
{
  "complaint_id": "CIVIO-2024-001234",
  "status": "submitted",
  "title": "Streetlight not working",
  "category": "electricity",
  "category_confidence": 0.95,
  "priority": "medium",
  "assigned_department": "Electrical Maintenance",
  "assigned_zone": "North Delhi Zone 3",
  "submission_time": "2024-01-15T10:30:00Z",
  "estimated_resolution": "2024-01-18T10:30:00Z",
  "tracking_link": "https://civio.app/track/CIVIO-2024-001234"
}
```

### Get Complaint Details
```
GET /api/complaints/{complaint_id}
Query Parameters:
  - language: string (optional, for response language)
```

**Response:**
```json
{
  "complaint_id": "CIVIO-2024-001234",
  "status": "in_progress",
  "title": "Streetlight not working",
  "description": "The streetlight near ABC School hasn't worked for 2 weeks",
  "category": "electricity",
  "priority": "medium",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address": "ABC School, New Delhi",
    "zone": "North Delhi Zone 3"
  },
  "department": "Electrical Maintenance",
  "assigned_to": "North Zone Team",
  "submission_time": "2024-01-15T10:30:00Z",
  "last_updated": "2024-01-15T14:00:00Z",
  "estimated_resolution": "2024-01-18T10:30:00Z",
  "image_url": "https://civio-images.s3.amazonaws.com/CIVIO-2024-001234.jpg",
  "status_timeline": [
    {
      "status": "submitted",
      "timestamp": "2024-01-15T10:30:00Z",
      "note": "Complaint received"
    },
    {
      "status": "assigned",
      "timestamp": "2024-01-15T10:45:00Z",
      "note": "Assigned to North Zone Electrical Team"
    },
    {
      "status": "in_progress",
      "timestamp": "2024-01-15T14:00:00Z",
      "note": "Work started on repair"
    }
  ]
}
```

### Update Complaint Status (Admin Only)
```
PATCH /api/complaints/{complaint_id}/status
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "status": "in_progress",
  "note": "Work started on repair",
  "assigned_to": "North Zone Team",
  "estimated_resolution": "2024-01-18T10:30:00Z"
}
```

**Response:**
```json
{
  "complaint_id": "CIVIO-2024-001234",
  "status": "in_progress",
  "updated_at": "2024-01-15T14:00:00Z",
  "last_updated_by": "admin_north_zone"
}
```

### Get Complaints Map Data
```
GET /api/complaints/map
Query Parameters:
  - bounds: string (optional, "lat_min,lng_min,lat_max,lng_max")
  - category: string (optional, filter by category)
  - priority: string (optional, filter by priority)
  - status: string (optional, filter by status)
```

**Response:**
```json
{
  "complaints": [
    {
      "complaint_id": "CIVIO-2024-001234",
      "location": {
        "latitude": 28.6139,
        "longitude": 77.2090
      },
      "category": "electricity",
      "priority": "medium",
      "status": "in_progress",
      "title": "Streetlight not working"
    },
    {
      "complaint_id": "CIVIO-2024-001235",
      "location": {
        "latitude": 28.6140,
        "longitude": 77.2091
      },
      "category": "water",
      "priority": "high",
      "status": "submitted",
      "title": "Water pipeline leak"
    }
  ],
  "hotspots": [
    {
      "center": {
        "latitude": 28.6140,
        "longitude": 77.2090
      },
      "radius": 500,
      "complaint_count": 23,
      "category": "electricity",
      "severity": "high"
    }
  ]
}
```

### Get Hotspot Data
```
GET /api/hotspots
Query Parameters:
  - state: string (optional)
  - city: string (optional)
  - category: string (optional)
  - days: integer (optional, default: 30, complaints in last N days)
```

**Response:**
```json
{
  "hotspots": [
    {
      "hotspot_id": "hs_001",
      "location_name": "North Delhi Market Area",
      "center": {
        "latitude": 28.6140,
        "longitude": 77.2090
      },
      "radius_meters": 500,
      "category": "electricity",
      "complaint_count": 23,
      "trend": "increasing",
      "avg_resolution_time_hours": 48,
      "status": "high_priority"
    }
  ],
  "summary": {
    "total_hotspots": 15,
    "critical_hotspots": 3,
    "high_priority_hotspots": 7
  }
}
```

### Search Complaints
```
GET /api/complaints/search
Query Parameters:
  - q: string (search term)
  - category: string (optional)
  - priority: string (optional)
  - status: string (optional)
  - state: string (optional)
  - from_date: date (optional, ISO format)
  - to_date: date (optional, ISO format)
  - page: integer (default: 1)
  - limit: integer (default: 20)
```

**Response:**
```json
{
  "results": [
    {
      "complaint_id": "CIVIO-2024-001234",
      "title": "Streetlight not working",
      "category": "electricity",
      "priority": "medium",
      "status": "in_progress",
      "location": "ABC School, New Delhi",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "limit": 20
}
```

### Submit Complaint Feedback
```
POST /api/complaints/{complaint_id}/feedback
Content-Type: application/json

{
  "rating": 4,
  "comment": "Work was done quickly, very satisfied",
  "resolution_status": "resolved"
}
```

**Response:**
```json
{
  "feedback_id": "fb_123456",
  "complaint_id": "CIVIO-2024-001234",
  "created_at": "2024-01-15T15:00:00Z"
}
```

---

## Admin

### Admin Dashboard Metrics
```
GET /api/admin/dashboard
Authorization: Bearer {admin_token}
Query Parameters:
  - date_range: string (optional, "7d", "30d", "90d")
  - region: string (optional, state/city filter)
```

**Response:**
```json
{
  "metrics": {
    "total_complaints": 1250,
    "pending_complaints": 47,
    "complaints_resolved_today": 12,
    "avg_resolution_time_hours": 36,
    "resolution_rate_percent": 87.3,
    "top_categories": [
      {
        "category": "water",
        "count": 356,
        "percent": 28.5
      },
      {
        "category": "electricity",
        "count": 298,
        "percent": 23.8
      }
    ]
  },
  "performance": {
    "department_performance": [
      {
        "department": "Water Supply",
        "avg_resolution_time": 42,
        "resolution_rate": 89,
        "pending": 12
      }
    ]
  },
  "hotspots": [
    {
      "location": "North Delhi Market",
      "complaint_count": 45,
      "trend": "increasing"
    }
  ]
}
```

### Get All Complaints (Admin)
```
GET /api/admin/complaints
Authorization: Bearer {admin_token}
Query Parameters:
  - status: string (optional, "submitted", "assigned", "in_progress", "resolved")
  - priority: string (optional)
  - category: string (optional)
  - department: string (optional)
  - page: integer (default: 1)
  - limit: integer (default: 50)
```

**Response:**
```json
{
  "complaints": [
    {
      "complaint_id": "CIVIO-2024-001234",
      "title": "Streetlight not working",
      "description": "...",
      "category": "electricity",
      "priority": "medium",
      "status": "in_progress",
      "department": "Electrical Maintenance",
      "assigned_to": "North Zone Team",
      "created_at": "2024-01-15T10:30:00Z",
      "last_updated": "2024-01-15T14:00:00Z",
      "estimated_resolution": "2024-01-18T10:30:00Z"
    }
  ],
  "total": 1250,
  "page": 1,
  "limit": 50
}
```

### Assign Complaint to Team
```
POST /api/admin/complaints/{complaint_id}/assign
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "assigned_to": "North Zone Team",
  "department": "Electrical Maintenance",
  "priority": "high",
  "note": "Priority escalated due to school area"
}
```

**Response:**
```json
{
  "complaint_id": "CIVIO-2024-001234",
  "assigned_to": "North Zone Team",
  "department": "Electrical Maintenance",
  "priority": "high",
  "assigned_at": "2024-01-15T15:00:00Z"
}
```

### Get Analytics & Trends
```
GET /api/admin/analytics
Authorization: Bearer {admin_token}
Query Parameters:
  - metric: string (optional, "complaints_trend", "category_distribution", "response_time")
  - period: string (optional, "daily", "weekly", "monthly")
  - days: integer (optional, default: 30)
```

**Response:**
```json
{
  "complaints_trend": [
    {
      "date": "2024-01-15",
      "submitted": 45,
      "resolved": 38,
      "pending": 47
    }
  ],
  "category_distribution": [
    {
      "category": "water",
      "count": 356,
      "percent": 28.5,
      "avg_resolution_time": 42
    }
  ],
  "response_time_stats": {
    "avg_hours": 36,
    "median_hours": 24,
    "percentile_95_hours": 120
  }
}
```

---

## Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "age",
        "error": "Must be between 18 and 120"
      }
    ],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Common Error Codes

| Status | Code | Message |
|--------|------|---------|
| 400 | VALIDATION_ERROR | Invalid input parameters |
| 400 | MISSING_REQUIRED_FIELD | Required field missing |
| 401 | UNAUTHORIZED | Authentication required |
| 403 | FORBIDDEN | Permission denied |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Duplicate entry |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |

### Example Error Response
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Complaint CIVIO-2024-999999 not found",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## Rate Limiting

All endpoints are rate-limited to prevent abuse:

```
- Public endpoints: 100 requests per minute per IP
- Authenticated endpoints: 1000 requests per minute per user
- Admin endpoints: 5000 requests per minute per admin
```

Rate limit info in response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705315800
```

---

## Examples

### Complete Flow: Register & Get Eligible Schemes

**Step 1: Register**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+91-9876543210",
    "email": "user@example.com",
    "language_preference": "hi"
  }'
```

**Step 2: Create Profile**
```bash
curl -X POST http://localhost:8000/api/users/usr_123456/profile \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income_annual": 400000,
    "occupation": "business_owner",
    "state": "Karnataka",
    "available_documents": ["aadhar", "pan"]
  }'
```

**Step 3: Get Eligible Schemes**
```bash
curl -X POST http://localhost:8000/api/schemes/match \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usr_123456"}'
```

### Complete Flow: Submit & Track Complaint

**Step 1: Submit Complaint**
```bash
curl -X POST http://localhost:8000/api/complaints \
  -F "title=Streetlight broken" \
  -F "description=Not working for 2 weeks" \
  -F "category=electricity" \
  -F "language=en" \
  -F 'location={"latitude": 28.6139, "longitude": 77.2090}' \
  -F "image=@streetlight.jpg"
```

**Step 2: Track Complaint**
```bash
curl -X GET http://localhost:8000/api/complaints/CIVIO-2024-001234
```

---

## Interactive API Testing

### Using Swagger UI
1. Open: http://localhost:8000/docs
2. Click "Try it out" on any endpoint
3. Fill in parameters
4. Click "Execute"

### Using ReDoc
1. Open: http://localhost:8000/redoc
2. Read API documentation
3. Test using Swagger UI (linked from ReDoc)

### Using Postman
1. Install Postman
2. Import OpenAPI spec: http://localhost:8000/openapi.json
3. Create environment variables for token/user_id
4. Run requests

---

## Webhooks (Planned)

Future version will support webhooks for:
- Complaint status updates
- Scheme eligibility changes
- Hotspot alerts

---

*Last Updated: January 2024*
*For questions, check [README.md](README.md) or open an issue on GitHub*
