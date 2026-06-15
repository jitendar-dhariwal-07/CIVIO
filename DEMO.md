# CIVIO Demo Guide

This document provides a step-by-step guide to demo CIVIO at a hackathon or presentation.

## Demo Duration: 10 Minutes

### Pre-Demo Checklist
- [ ] All services running (Backend, Frontend, Database)
- [ ] Sample data seeded in database
- [ ] Internet connection stable
- [ ] Open http://localhost:3000 in browser
- [ ] API documentation open at http://localhost:8000/docs (in another tab)

---

## Demo Scenario 1: Government Scheme Navigator (3 minutes)

### Setup
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Database (optional, for monitoring)
# Keep terminal available for checking logs
```

### Demo Steps

**1. Home Page (30 seconds)**
- Show the CIVIO home page
- Highlight two main features: "Discover Schemes" and "Report Civic Issues"
- Show language selector (English/Hindi)

**2. Start Scheme Discovery (2 minutes)**
- Click "Discover Schemes" button
- Show multilingual questionnaire
- Fill in sample profile:
  - **Age**: 35 years
  - **Annual Income**: ₹4,00,000
  - **Occupation**: Small Business Owner
  - **State**: Karnataka
  - **Category**: General
  - **Available Documents**: Aadhar, PAN
  - **Education**: Graduate

**3. Show Results (30 seconds)**
```
"Wow! We found 12 schemes you're eligible for!"

Top Results Displayed:
✓ PM Mudra Loan Scheme (95% match)
  - Loan: ₹50,000 - ₹10,00,000
  - Interest: Variable (MCLR based)
  - Status: Direct link to official portal

✓ Karnataka Small Business Grant (88% match)
  - Grant: ₹2,00,000
  - Documents needed: Aadhar ✓, PAN ✓, Business Reg ✗
  
✓ SIDBI Entrepreneurship Support (82% match)
```

**4. Click on a Scheme (to see details)**
- Show scheme details page
- Show eligibility criteria
- Show document checklist
- Show "Apply Now" → Links to official portal
- Show FAQ section

**Key Talking Points:**
- "Instead of visiting 5 different government websites, you see all relevant schemes in one place"
- "The system matches based on your profile, not just random search"
- "We don't claim to give benefits, we direct you to the right portal"
- "Available in Hindi and other languages for accessibility"

---

## Demo Scenario 2: Civic Complaint Intelligence (4 minutes)

### Demo Steps

**1. Home Page → Report Issue (30 seconds)**
- Click "Report Civic Issues" button
- Show the complaint form
- Emphasize: Simple, multilingual, with image support

**2. Submit a Sample Complaint (1 minute)**
```
Language: English (or switch to Hindi for drama!)

Title: "Streetlight near ABC School not working"

Description: 
"The streetlight near ABC School hasn't worked for 2 weeks. 
It's dangerous for students at night. Please fix it soon."

Location: [Show auto-detected location on map, or manually select]

Image: [Upload a streetlight photo - you can prepare one]

Click: "SUBMIT"
```

**3. AI Processing in Real-Time (1 minute)**
```
Show loading animation:
"🤖 Analyzing complaint..."

Then show results:
━━━━━━━━━━━━━━━━━━━━━━━━
✓ CATEGORIZED: Electricity
  Confidence: 95%

✓ PRIORITY: Medium
  Reason: Safety concern but not critical

✓ DEPARTMENT: Electrical Maintenance
  Zone: North Delhi Zone 3

✓ COMPLAINT ID: CIVIO-2024-001234

━━━━━━━━━━━━━━━━━━━━━━━━
Status: ✓ Submitted
        → Assigned to North Delhi Team
        → Estimated resolution: 2-3 days
```

**4. Show Hotspot Map (30 seconds)**
- Switch to "View on Map" tab
- Show map with all complaints visualized
- Highlight hotspots (red zones with 5+ complaints)
- Show: "North Delhi Market: 23 complaints in past week"
- Explain: "Administrators see hotspots and prioritize maintenance"

**5. Show Complaint Tracking (1 minute)**
- Copy the Complaint ID
- Show "Track Complaint" page
- Display status timeline:
  ```
  CIVIO-2024-001234
  
  ✓ Submitted (2 hours ago)
    "Complaint received"
  
  ✓ Assigned (1.5 hours ago)
    "Assigned to North Zone Electrical Team"
  
  ○ In Progress (30 mins ago)
    "Work started on repair"
  
  ○ Resolved (Expected in 48 hours)
  ```

**Key Talking Points:**
- "Citizens know exactly where their complaint went and when it will be resolved"
- "Duplicate complaints are automatically detected and merged"
- "AI understands complaints in multiple languages"
- "Administrators see hotspots and prioritize problem areas"
- "Response time improves because routing is instant, not manual"

---

## Demo Scenario 3: Admin Dashboard (2 minutes)

### Access Admin Panel
```
URL: http://localhost:8000/admin/dashboard

(In production, this would have login. For demo, bypass with mock auth)
```

### Show Metrics
```
Today's Statistics:
├─ Total Complaints: 1,250
├─ Pending: 47
├─ Resolved Today: 12
├─ Avg Response Time: 36 hours
└─ Resolution Rate: 87.3%

By Category:
├─ Water Issues: 356 (28.5%)
├─ Electricity: 298 (23.8%)
├─ Roads/Potholes: 245 (19.6%)
├─ Sanitation: 198 (15.8%)
└─ Other: 153 (12.2%)

Department Performance:
├─ Water Supply: Avg 42 hours, 89% resolution rate
├─ Roads: Avg 72 hours, 76% resolution rate
└─ Electricity: Avg 36 hours, 92% resolution rate
```

### Show Hotspot Visualization
```
Heatmap displayed on map:
- Red zones (critical): 5+ complaints/week
- Orange zones (high): 3-4 complaints/week
- Yellow zones (medium): 1-2 complaints/week

Top Hotspot: North Delhi Market
├─ 45 complaints (past week)
├─ Top issue: Water (25 complaints)
├─ Trend: Increasing ⚠️
└─ Recommendation: Priority maintenance needed
```

**Key Talking Points:**
- "Before this, complaints were handled randomly"
- "Now administrators have data-driven insights"
- "They can see problem areas and prevent issues before they escalate"
- "Performance metrics help them track team efficiency"

---

## Demo Talking Points (General)

### The Problem (30 seconds)
- **Scheme Discovery**: Citizens don't know which benefits they qualify for. Massive welfare funds go unclaimed.
- **Complaint Handling**: Thousands of complaints daily, but manual routing causes delays. Citizens don't know status.

### The Solution (2 minutes)
1. **Scheme Navigator**: One platform, all schemes, eligibility matching in 5 minutes
2. **Complaint Intelligence**: Instant AI categorization, automatic routing, real-time tracking
3. **Multilingual**: Hindi, Tamil, Telugu, Kannada for accessibility
4. **Admin Insights**: Hotspots, trends, performance metrics for better planning

### The Impact
- **Citizens**: Find benefits they didn't know existed (₹10-20 lakhs saved per person annually)
- **Government**: 40-50% faster complaint resolution, better resource planning
- **Scalability**: Built for all 28 states + 8 UTs with 2000+ schemes and 22 languages

### Why It Matters in India
- **1.4 billion people**: Most don't know which schemes they qualify for
- **Regional complexity**: Different rules in each state
- **Language barrier**: 70% prefer local languages, not English-only portals
- **Trust factor**: Citizens need to see their complaints are being handled

---

## Live API Testing (Bonus: 2 minutes)

If audience wants to see backend capabilities:

### Open API Documentation
```
http://localhost:8000/docs
```

### Test Endpoint 1: Match Schemes
```
POST /api/schemes/match

Body:
{
  "age": 35,
  "income_annual": 400000,
  "occupation": "business_owner",
  "state": "Karnataka",
  "available_documents": ["aadhar", "pan"]
}

Response: Shows 12 matching schemes with relevance scores
```

### Test Endpoint 2: Submit Complaint
```
POST /api/complaints

Body:
{
  "title": "Pothole in road",
  "description": "Large hole blocking traffic",
  "category": "road",
  "location": {"latitude": 28.6139, "longitude": 77.2090},
  "language": "en"
}

Response: Auto-categorized, prioritized, and routed
```

---

## Common Questions to Anticipate

**Q: Why is this better than existing portals?**
A: Existing portals are fragmented. MyScheme has 800+ schemes but no eligibility matching. Complaint portals are municipal-specific. CIVIO unifies everything with AI intelligence.

**Q: What about government API integration?**
A: MVP uses open data sources. Full integration happens post-hackathon through official government partnerships. We link to official portals, not claim to give approvals.

**Q: How do you ensure accuracy?**
A: We use official government scheme data and have feedback loops. Citizens flag inaccuracies, which gets corrected. Disclaimers are clear.

**Q: What about rural areas without internet?**
A: Phase 2 includes SMS-based access and partnerships with NGOs for offline access.

**Q: How do you handle Hindi/regional languages?**
A: Google Translate API + IndicTrans for better regional language support. Fine-tuned models for complaint categorization in Hindi.

---

## Post-Demo: Engagement

1. **GitHub**: Share repository link for interested developers
2. **Contact**: Provide email for feedback and partnerships
3. **Demo Link**: Live version deployed on Railway/Vercel for hands-on testing
4. **Feedback Form**: Collect insights from judges/audience

---

## Technical Troubleshooting During Demo

**If Frontend Doesn't Load:**
```bash
# Restart frontend
cd frontend
npm run dev
```

**If Backend API Fails:**
```bash
# Check database connection
psql -U civio_user -d civio_db
# Check API health
curl http://localhost:8000/health
```

**If Sample Data Missing:**
```bash
# Reseed database
cd backend
python -c "from database import seed_db; seed_db()"
```

**If Port Already in Use:**
```bash
# Change port
npm run dev -- -p 3001  # Frontend on 3001
uvicorn main:app --port 8001  # Backend on 8001
```

---

## Time Management

```
Total Time: 10 minutes

0:00 - 0:30  | Introduction to CIVIO
0:30 - 3:30  | Scheme Navigator Demo
3:30 - 7:30  | Complaint Intelligence Demo
7:30 - 9:30  | Admin Dashboard + Impact
9:30 - 10:00 | Q&A + Next Steps
```

**Pro Tips:**
- Pre-load all pages in browser tabs
- Have sample data ready (don't waste time filling forms)
- Keep demo script nearby but don't read it word-for-word
- Make eye contact with judges/audience
- Be ready to pivot to live API testing if asked

---

## Success Metrics

Judges will be looking for:
- ✓ **Problem clarity**: Do they understand the gaps in Indian civic systems?
- ✓ **Solution elegance**: Is the MVP achievable in hackathon time?
- ✓ **Scalability**: Can it work across 28 states with 2000+ schemes?
- ✓ **Impact**: How many citizens will benefit?
- ✓ **Technical depth**: Is there real AI/ML, not just UI?
- ✓ **Implementation**: Are they close to deployment-ready?

---

*This demo guide is designed for a 10-minute presentation. Adjust timing based on audience engagement and questions.*

**Good luck! 🚀**
