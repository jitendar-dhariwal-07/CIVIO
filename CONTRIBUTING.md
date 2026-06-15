# Contributing to CIVIO

Thank you for your interest in contributing to CIVIO! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inspiring community. Please read and follow our Code of Conduct:
- Be respectful and inclusive
- Welcome different perspectives
- Focus on constructive feedback
- Report harassment or problematic behavior

## How to Contribute

### 1. Report Bugs

If you find a bug, please create an issue on GitHub:
- **Clear Title**: Describe the bug clearly
- **Description**: Explain what you expected vs. what happened
- **Steps to Reproduce**: Provide exact steps to reproduce
- **Environment**: OS, Python version, Node version, etc.
- **Attachments**: Screenshots or error logs if relevant

**Example:**
```
Title: Complaint categorization fails for Hindi text with numbers

Description:
When submitting a Hindi complaint with numbers (e.g., "रोड पर 2 गड्ढे हैं"), 
the categorization API returns a 500 error instead of categorizing the complaint.

Steps:
1. Open complaint form
2. Select Hindi language
3. Type: "रोड पर 2 गड्ढे हैं"
4. Click Submit

Expected: Should categorize as "Road"
Actual: Returns 500 error

Environment: Windows 10, Python 3.11, Node 18.12
```

### 2. Suggest Features

Have an idea? Share it!
- **Title**: Clear feature description
- **Problem**: What problem does it solve?
- **Proposed Solution**: How would it work?
- **Alternatives**: Other approaches considered?

**Example:**
```
Title: Add SMS notifications for complaint status updates

Problem: 
Citizens without constant internet access can't track complaint status. 
SMS would be accessible to all, even with 2G connections.

Proposed Solution:
- Add SMS notification preference in settings
- Send SMS when complaint status changes
- Use open-source SMS API (Twilio fallback)

Use Case:
Rural users with basic phones can know when their complaint is being worked on.
```

### 3. Submit Pull Requests

#### Setup Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/civio.git
cd civio

# Create a feature branch
git checkout -b feature/your-feature-name

# Make changes and test
# Commit with clear messages
git commit -m "feat: add SMS notifications for complaint status"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

#### Branch Naming Convention

```
feature/feature-name          # New features
bugfix/bug-description        # Bug fixes
docs/documentation-update     # Documentation
refactor/code-improvement     # Code refactoring
test/test-addition           # Test additions
chore/maintenance-task       # Maintenance
```

#### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**: feat, fix, docs, style, refactor, test, chore
**Scope**: complaint, scheme, auth, api, db, frontend
**Subject**: Concise description (50 chars max)

**Example:**
```
feat(complaint): add duplicate detection using embeddings

Implement TF-IDF and cosine similarity based duplicate detection
for complaints. Merge duplicate complaints and preserve vote counts.

Fixes #123
Closes #456
```

#### Code Quality Requirements

**Python (Backend):**
```bash
# Code style
pip install black
black backend/

# Linting
pip install flake8
flake8 backend/

# Type checking
pip install mypy
mypy backend/

# Testing
pytest tests/ -v
```

**TypeScript/JavaScript (Frontend):**
```bash
# Code style
npm run format

# Linting
npm run lint

# Type checking
npm run type-check

# Testing
npm run test
```

### 4. Documentation Contributions

Documentation is as important as code!

**Areas for contribution:**
- Tutorials for new users
- API endpoint documentation
- Troubleshooting guides
- Architecture explanations
- Deployment guides
- Language improvements (English clarity)

**Guidelines:**
- Use Markdown format
- Include code examples where relevant
- Add links to related sections
- Proofread before submitting
- Keep docs up-to-date with code changes

---

## Development Workflow

### Project Structure

```
civio/
├── backend/
│   ├── db/              # Database models and CRUD
│   ├── models/          # Pydantic data models
│   ├── services/        # Business logic
│   ├── routes/          # API endpoints
│   ├── tests/           # Unit & integration tests
│   ├── config.py        # Configuration
│   ├── database.py      # DB connection
│   └── main.py          # FastAPI app entry
│
├── frontend/
│   ├── src/app/         # Next.js pages
│   ├── src/components/  # React components
│   ├── src/lib/         # Utilities and hooks
│   ├── src/context/     # Context providers
│   ├── public/          # Static files & translations
│   └── tests/           # Jest tests
│
└── database/
    ├── schema.sql       # Database schema
    └── seed.sql         # Sample data
```

### Before Starting Development

1. **Check existing issues** - Avoid duplicate work
2. **Discuss large changes** - Open an issue first
3. **Assign yourself** - Comment "I'll work on this"
4. **Keep branch updated** - Sync with main frequently

### During Development

1. **Write tests** - For every feature/fix
2. **Run linters** - Before committing
3. **Document changes** - Update relevant docs
4. **Keep commits small** - Logical, reviewable chunks
5. **Push regularly** - Don't hold changes locally too long

### Before Submitting PR

1. **Test locally** - All scenarios
2. **Update documentation** - If API changes
3. **Run tests** - Full test suite should pass
4. **Check CI/CD** - GitHub Actions must pass
5. **Review your own code** - Catch obvious issues
6. **No conflicts** - Merge latest main branch

---

## Testing Guidelines

### Backend Tests

**Test file location:** `backend/tests/`
**Run:** `pytest tests/ -v`

```python
# Example test
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_schemes():
    response = client.get("/api/schemes")
    assert response.status_code == 200
    assert "schemes" in response.json()

def test_complaint_submission():
    payload = {
        "title": "Pothole in road",
        "description": "Large hole blocking traffic",
        "category": "road",
        "location": {"latitude": 28.6, "longitude": 77.2},
        "language": "en"
    }
    response = client.post("/api/complaints", json=payload)
    assert response.status_code == 201
    assert "complaint_id" in response.json()
```

### Frontend Tests

**Test file location:** `frontend/__tests__/`
**Run:** `npm run test`

```typescript
// Example test
import { render, screen } from '@testing-library/react';
import SchemeCard from '@/components/SchemeCard';

describe('SchemeCard', () => {
  it('displays scheme information', () => {
    const scheme = {
      id: 'scheme_001',
      name: 'PM Mudra',
      description: 'Loan scheme'
    };
    
    render(<SchemeCard scheme={scheme} />);
    expect(screen.getByText('PM Mudra')).toBeInTheDocument();
  });
});
```

### Integration Tests

Test end-to-end flows:
- User registration → Profile creation → Scheme matching
- Complaint submission → AI categorization → Assignment
- Admin dashboard → Complaint filtering → Status updates

---

## Performance Considerations

### Backend
- Use database indexes for frequent queries
- Cache expensive operations (eligibility matching)
- Implement pagination for large result sets
- Use async/await for I/O operations
- Profile code before optimization

### Frontend
- Optimize images (use WebP)
- Code splitting for large bundles
- Use React.memo for expensive components
- Lazy load map and charts
- Implement virtual scrolling for long lists

---

## Security Considerations

### Backend
- Validate all user inputs
- Use parameterized SQL queries (SQLAlchemy)
- Implement rate limiting
- Validate API tokens
- Encrypt sensitive data
- Log security-relevant events
- Use HTTPS in production

### Frontend
- Sanitize user input
- Don't store sensitive data in localStorage
- Use secure headers
- Validate file uploads
- Implement CSRF protection

---

## Documentation Standards

### Code Comments
```python
# Good: Explains WHY, not WHAT
# User profile needs to be cached to reduce DB queries during eligibility matching
cache.set(user_id, profile, ttl=3600)

# Bad: Explains obvious WHAT
# Set cache key with user profile
cache.set(user_id, profile, ttl=3600)
```

### Docstrings
```python
def match_schemes(user_profile: UserProfile) -> List[Scheme]:
    """
    Match eligible schemes for a user based on their profile.
    
    Args:
        user_profile: User's personal and demographic information
        
    Returns:
        List of eligible schemes sorted by relevance score
        
    Raises:
        ValueError: If profile is missing required fields
        
    Example:
        >>> profile = UserProfile(age=35, income=400000, state="Karnataka")
        >>> schemes = match_schemes(profile)
        >>> print(len(schemes))
        12
    """
```

### README Sections
Every major component should have:
- What it does
- How to use it
- Example usage
- Configuration options
- Troubleshooting

---

## Review Process

### PR Review

1. **Automated checks**
   - Code quality (linting)
   - Tests (must pass)
   - Coverage (should be >80%)
   - Build success

2. **Code review**
   - Two approvals required
   - Follows style guidelines
   - Includes tests
   - Documentation updated
   - No breaking changes

3. **Feedback cycle**
   - Author responds to comments
   - Request changes or approve
   - Mark "conversation resolved"
   - Push updated code

4. **Merge**
   - Squash commits if needed
   - Delete feature branch
   - Close related issues

### Reviewer Guidelines

Be respectful and constructive:
- Praise good code
- Ask questions instead of demanding
- Suggest improvements
- Acknowledge effort
- Be patient with learning contributions

---

## Getting Help

- **Questions**: Open a discussion or issue
- **Stuck?**: Ask in GitHub discussions
- **Want feedback?**: Open draft PR early
- **Chat**: Join community discussions

## Contributor Benefits

Contributors who make meaningful contributions become:
- Listed in `CONTRIBUTORS.md`
- Eligible for core team membership
- Priority consideration for feature requests
- Recognition in project announcements

---

## Related Documentation

- [README.md](README.md) - Project overview
- [PROJECT_DESIGN.md](PROJECT_DESIGN.md) - Architecture & design
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API endpoints
- [SETUP.md](SETUP.md) - Development setup

---

Thank you for contributing to CIVIO! 🙏

Together, we're building something that helps millions of Indians access government benefits and services faster.

*Last Updated: January 2024*
