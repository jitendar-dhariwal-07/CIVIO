-- ============================================================================
-- CitizenAI - Complete PostgreSQL Database Schema
-- AI-Powered Multilingual Hyperlocal Citizen Assistance Platform for India
-- Version: 1.0.0
-- Created: 2026-06-15
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";      -- For gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pg_trgm";       -- For fuzzy text search
CREATE EXTENSION IF NOT EXISTS "postgis";       -- For geospatial queries (hotspots)
CREATE EXTENSION IF NOT EXISTS "unaccent";      -- For accent-insensitive search

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

CREATE TYPE user_role AS ENUM ('citizen', 'admin', 'moderator', 'department_official');
CREATE TYPE gender_type AS ENUM ('male', 'female', 'transgender', 'other', 'prefer_not_to_say');
CREATE TYPE category_type AS ENUM ('general', 'obc', 'sc', 'st', 'ews');
CREATE TYPE scheme_type AS ENUM ('central', 'state', 'joint');
CREATE TYPE benefit_type AS ENUM ('dbt', 'in_kind', 'subsidy', 'loan', 'insurance', 'pension', 'scholarship', 'free_service', 'tax_benefit');
CREATE TYPE application_status AS ENUM ('bookmarked', 'documents_collected', 'applied', 'under_review', 'approved', 'rejected', 'disbursed');
CREATE TYPE complaint_status AS ENUM ('submitted', 'acknowledged', 'in_progress', 'escalated', 'resolved', 'closed', 'reopened');
CREATE TYPE complaint_priority AS ENUM ('low', 'medium', 'high', 'critical');
CREATE TYPE complaint_category AS ENUM (
    'roads', 'water_supply', 'drainage', 'streetlights', 'garbage',
    'electricity', 'public_transport', 'healthcare', 'education',
    'ration_shop', 'land_revenue', 'police', 'housing',
    'environment', 'corruption', 'other'
);
CREATE TYPE supported_language AS ENUM ('en', 'hi', 'ta', 'te', 'kn', 'ml');
CREATE TYPE audit_action AS ENUM ('create', 'update', 'delete', 'login', 'logout', 'apply', 'escalate', 'resolve');

-- ============================================================================
-- TABLE: users
-- Citizens, admins, department officials
-- ============================================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(15) UNIQUE NOT NULL,
    phone_verified BOOLEAN DEFAULT FALSE,
    age INTEGER CHECK (age >= 0 AND age <= 150),
    date_of_birth DATE,
    gender gender_type,
    state VARCHAR(100),
    district VARCHAR(100),
    block VARCHAR(100),
    village_or_city VARCHAR(200),
    pincode VARCHAR(6) CHECK (pincode ~ '^\d{6}$'),
    preferred_language supported_language DEFAULT 'en',
    occupation VARCHAR(100),
    income_range VARCHAR(50),       -- e.g., 'below_1l', '1l_2.5l', '2.5l_5l', '5l_10l', 'above_10l'
    annual_income NUMERIC(12,2),
    education VARCHAR(100),
    family_status VARCHAR(50),      -- e.g., 'single', 'married', 'widow', 'divorced'
    family_size INTEGER CHECK (family_size >= 1),
    category category_type DEFAULT 'general',
    is_bpl BOOLEAN DEFAULT FALSE,
    is_differently_abled BOOLEAN DEFAULT FALSE,
    disability_percentage INTEGER CHECK (disability_percentage >= 0 AND disability_percentage <= 100),
    documents_available TEXT[],     -- Array: aadhaar, pan, voter_id, ration_card, etc.
    role user_role DEFAULT 'citizen',
    department_id UUID,             -- If role is department_official
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_state_district ON users(state, district);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_category ON users(category);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================================================
-- TABLE: schemes
-- Government schemes (central, state, joint)
-- ============================================================================

CREATE TABLE schemes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id VARCHAR(100) UNIQUE NOT NULL,   -- Human-readable ID e.g. 'pm_kisan'
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    short_description VARCHAR(500),
    ministry VARCHAR(255),
    department VARCHAR(255),
    type scheme_type NOT NULL,
    state VARCHAR(100),                       -- NULL for central schemes
    benefit_type benefit_type NOT NULL,
    benefit_amount VARCHAR(255),
    benefit_description TEXT,
    eligibility_summary TEXT,
    application_process TEXT,
    application_url VARCHAR(500),
    helpline VARCHAR(50),
    launch_date DATE,
    last_date DATE,                           -- NULL if ongoing
    is_active BOOLEAN DEFAULT TRUE,
    tags TEXT[],
    icon_url VARCHAR(500),
    priority_score INTEGER DEFAULT 0,         -- For recommendation ordering
    total_beneficiaries BIGINT,
    budget_allocation VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_schemes_scheme_id ON schemes(scheme_id);
CREATE INDEX idx_schemes_type ON schemes(type);
CREATE INDEX idx_schemes_state ON schemes(state);
CREATE INDEX idx_schemes_benefit_type ON schemes(benefit_type);
CREATE INDEX idx_schemes_is_active ON schemes(is_active);
CREATE INDEX idx_schemes_tags ON schemes USING GIN(tags);
CREATE INDEX idx_schemes_name_trgm ON schemes USING GIN(name gin_trgm_ops);
CREATE INDEX idx_schemes_full_name_trgm ON schemes USING GIN(full_name gin_trgm_ops);

-- ============================================================================
-- TABLE: scheme_eligibility_rules
-- Machine-readable eligibility rules for automated matching
-- ============================================================================

CREATE TABLE scheme_eligibility_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id UUID NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    rule_group INTEGER DEFAULT 1,              -- Rules in same group are AND-ed; groups are OR-ed
    field VARCHAR(100) NOT NULL,               -- User profile field to check
    operator VARCHAR(20) NOT NULL,             -- eq, neq, in, not_in, lt, lte, gt, gte, between, contains
    value JSONB NOT NULL,                      -- Value(s) to compare against
    is_mandatory BOOLEAN DEFAULT TRUE,         -- If false, adds to score but doesn't disqualify
    score_weight NUMERIC(3,2) DEFAULT 1.0,     -- Weight for recommendation scoring
    error_message VARCHAR(500),                -- Human-readable message if rule fails
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_eligibility_rules_scheme ON scheme_eligibility_rules(scheme_id);
CREATE INDEX idx_eligibility_rules_field ON scheme_eligibility_rules(field);

-- ============================================================================
-- TABLE: scheme_documents_required
-- Documents required for each scheme application
-- ============================================================================

CREATE TABLE scheme_documents_required (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheme_id UUID NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    document_name VARCHAR(255) NOT NULL,       -- e.g., 'Aadhaar Card', 'Income Certificate'
    document_key VARCHAR(100) NOT NULL,        -- e.g., 'aadhaar', 'income_certificate'
    is_mandatory BOOLEAN DEFAULT TRUE,
    description VARCHAR(500),
    issuing_authority VARCHAR(255),
    how_to_obtain TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_scheme_docs_scheme ON scheme_documents_required(scheme_id);

-- ============================================================================
-- TABLE: scheme_applications
-- User applications, bookmarks, and tracking
-- ============================================================================

CREATE TABLE scheme_applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    scheme_id UUID NOT NULL REFERENCES schemes(id) ON DELETE CASCADE,
    status application_status DEFAULT 'bookmarked',
    eligibility_score NUMERIC(5,2),           -- 0 to 100
    eligibility_matched_rules JSONB,          -- Which rules matched
    eligibility_failed_rules JSONB,           -- Which rules failed
    documents_submitted TEXT[],
    application_reference VARCHAR(100),        -- Govt application number
    applied_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, scheme_id)                -- One application per user per scheme
);

CREATE INDEX idx_scheme_apps_user ON scheme_applications(user_id);
CREATE INDEX idx_scheme_apps_scheme ON scheme_applications(scheme_id);
CREATE INDEX idx_scheme_apps_status ON scheme_applications(status);
CREATE INDEX idx_scheme_apps_user_status ON scheme_applications(user_id, status);

-- ============================================================================
-- TABLE: departments
-- Government departments for complaint routing
-- ============================================================================

CREATE TABLE departments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    short_name VARCHAR(50),
    state VARCHAR(100) NOT NULL,
    category complaint_category NOT NULL,
    parent_department_id UUID REFERENCES departments(id),
    head_name VARCHAR(255),
    head_designation VARCHAR(255),
    address TEXT,
    email VARCHAR(255),
    phone VARCHAR(50),
    website VARCHAR(500),
    grievance_portal VARCHAR(500),
    sla_hours INTEGER DEFAULT 72,             -- Expected resolution time
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_departments_state ON departments(state);
CREATE INDEX idx_departments_category ON departments(category);
CREATE INDEX idx_departments_state_category ON departments(state, category);

-- ============================================================================
-- TABLE: department_contacts
-- Multiple contact points per department (district-level, block-level)
-- ============================================================================

CREATE TABLE department_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    department_id UUID NOT NULL REFERENCES departments(id) ON DELETE CASCADE,
    district VARCHAR(100),
    block VARCHAR(100),
    contact_person VARCHAR(255),
    designation VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    office_address TEXT,
    office_hours VARCHAR(100),                -- e.g., 'Mon-Fri 10:00-17:00'
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_dept_contacts_dept ON department_contacts(department_id);
CREATE INDEX idx_dept_contacts_district ON department_contacts(district);

-- ============================================================================
-- TABLE: complaints
-- Citizen grievances and complaints
-- ============================================================================

CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_number VARCHAR(20) UNIQUE NOT NULL, -- e.g., 'CIT-TN-2026-000001'
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category complaint_category NOT NULL,
    subcategory VARCHAR(100),
    subject VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    original_language supported_language DEFAULT 'en',
    translated_description TEXT,              -- English translation if original is in regional language
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    block VARCHAR(100),
    locality VARCHAR(255),
    pincode VARCHAR(6),
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7),
    location GEOGRAPHY(POINT, 4326),          -- PostGIS geography column
    department_id UUID REFERENCES departments(id),
    assigned_to UUID REFERENCES users(id),    -- Department official
    status complaint_status DEFAULT 'submitted',
    priority complaint_priority DEFAULT 'medium',
    ai_priority_score NUMERIC(5,2),           -- AI-computed priority 0-100
    ai_category_confidence NUMERIC(3,2),      -- Confidence of AI categorization
    upvote_count INTEGER DEFAULT 0,
    is_anonymous BOOLEAN DEFAULT FALSE,
    is_duplicate BOOLEAN DEFAULT FALSE,
    parent_complaint_id UUID REFERENCES complaints(id),  -- If merged as duplicate
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT,
    satisfaction_rating INTEGER CHECK (satisfaction_rating >= 1 AND satisfaction_rating <= 5),
    satisfaction_feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_complaints_user ON complaints(user_id);
CREATE INDEX idx_complaints_number ON complaints(complaint_number);
CREATE INDEX idx_complaints_category ON complaints(category);
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_priority ON complaints(priority);
CREATE INDEX idx_complaints_state_district ON complaints(state, district);
CREATE INDEX idx_complaints_department ON complaints(department_id);
CREATE INDEX idx_complaints_assigned_to ON complaints(assigned_to);
CREATE INDEX idx_complaints_created_at ON complaints(created_at DESC);
CREATE INDEX idx_complaints_location ON complaints USING GIST(location);
CREATE INDEX idx_complaints_subject_trgm ON complaints USING GIN(subject gin_trgm_ops);

-- ============================================================================
-- TABLE: complaint_images
-- Photos/evidence attached to complaints
-- ============================================================================

CREATE TABLE complaint_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    thumbnail_url TEXT,
    caption VARCHAR(500),
    ai_analysis JSONB,                        -- AI image analysis results
    file_size INTEGER,                        -- In bytes
    mime_type VARCHAR(50),
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_complaint_images_complaint ON complaint_images(complaint_id);

-- ============================================================================
-- TABLE: complaint_updates
-- Timeline of complaint status changes and communications
-- ============================================================================

CREATE TABLE complaint_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    updated_by UUID REFERENCES users(id),
    old_status complaint_status,
    new_status complaint_status,
    comment TEXT,
    is_public BOOLEAN DEFAULT TRUE,           -- If visible to complainant
    attachment_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_complaint_updates_complaint ON complaint_updates(complaint_id);
CREATE INDEX idx_complaint_updates_created ON complaint_updates(created_at);

-- ============================================================================
-- TABLE: complaint_duplicates
-- Tracks duplicate/similar complaints for clustering
-- ============================================================================

CREATE TABLE complaint_duplicates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    duplicate_of UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    similarity_score NUMERIC(3,2) NOT NULL,   -- 0.00 to 1.00
    detected_by VARCHAR(20) DEFAULT 'ai',     -- 'ai' or 'manual'
    confirmed BOOLEAN DEFAULT FALSE,
    confirmed_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(complaint_id, duplicate_of),
    CHECK (complaint_id != duplicate_of)
);

CREATE INDEX idx_complaint_dups_complaint ON complaint_duplicates(complaint_id);
CREATE INDEX idx_complaint_dups_duplicate_of ON complaint_duplicates(duplicate_of);

-- ============================================================================
-- TABLE: hotspots
-- Geographic areas with clustered complaints
-- ============================================================================

CREATE TABLE hotspots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category complaint_category NOT NULL,
    state VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    locality VARCHAR(255),
    center_latitude NUMERIC(10,7) NOT NULL,
    center_longitude NUMERIC(10,7) NOT NULL,
    center_location GEOGRAPHY(POINT, 4326),
    radius_meters INTEGER DEFAULT 500,
    complaint_count INTEGER DEFAULT 0,
    severity_score NUMERIC(5,2) DEFAULT 0,    -- Aggregated severity 0-100
    first_reported_at TIMESTAMP WITH TIME ZONE,
    last_reported_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB,                           -- Additional data like avg resolution time
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_hotspots_category ON hotspots(category);
CREATE INDEX idx_hotspots_state_district ON hotspots(state, district);
CREATE INDEX idx_hotspots_location ON hotspots USING GIST(center_location);
CREATE INDEX idx_hotspots_active ON hotspots(is_active);
CREATE INDEX idx_hotspots_severity ON hotspots(severity_score DESC);

-- ============================================================================
-- TABLE: translations
-- Content translations for schemes, complaints, UI strings
-- ============================================================================

CREATE TABLE translations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,         -- 'scheme', 'complaint', 'department', 'ui'
    entity_id VARCHAR(255) NOT NULL,          -- UUID or string key
    field_name VARCHAR(100) NOT NULL,         -- e.g., 'name', 'description', 'subject'
    language supported_language NOT NULL,
    translated_text TEXT NOT NULL,
    is_machine_translated BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(entity_type, entity_id, field_name, language)
);

CREATE INDEX idx_translations_entity ON translations(entity_type, entity_id);
CREATE INDEX idx_translations_language ON translations(language);
CREATE INDEX idx_translations_lookup ON translations(entity_type, entity_id, language);

-- ============================================================================
-- TABLE: audit_log
-- Comprehensive audit trail for all user and system actions
-- ============================================================================

CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    action audit_action NOT NULL,
    entity_type VARCHAR(50) NOT NULL,         -- 'user', 'complaint', 'scheme_application', etc.
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_action ON audit_log(action);
CREATE INDEX idx_audit_entity ON audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created_at ON audit_log(created_at DESC);

-- ============================================================================
-- TABLE: complaint_upvotes
-- Track which users have upvoted a complaint
-- ============================================================================

CREATE TABLE complaint_upvotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    complaint_id UUID NOT NULL REFERENCES complaints(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(complaint_id, user_id)
);

CREATE INDEX idx_upvotes_complaint ON complaint_upvotes(complaint_id);
CREATE INDEX idx_upvotes_user ON complaint_upvotes(user_id);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_schemes_updated_at
    BEFORE UPDATE ON schemes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_scheme_applications_updated_at
    BEFORE UPDATE ON scheme_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_departments_updated_at
    BEFORE UPDATE ON departments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_complaints_updated_at
    BEFORE UPDATE ON complaints
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_hotspots_updated_at
    BEFORE UPDATE ON hotspots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_translations_updated_at
    BEFORE UPDATE ON translations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Auto-generate complaint number
CREATE OR REPLACE FUNCTION generate_complaint_number()
RETURNS TRIGGER AS $$
DECLARE
    state_code VARCHAR(5);
    seq_num INTEGER;
BEGIN
    -- Get state abbreviation
    state_code := UPPER(LEFT(REPLACE(NEW.state, ' ', ''), 2));

    -- Get next sequence number for this state and year
    SELECT COALESCE(MAX(
        CAST(SPLIT_PART(complaint_number, '-', 4) AS INTEGER)
    ), 0) + 1
    INTO seq_num
    FROM complaints
    WHERE state = NEW.state
      AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW());

    NEW.complaint_number := 'CIT-' || state_code || '-' ||
                            EXTRACT(YEAR FROM NOW())::TEXT || '-' ||
                            LPAD(seq_num::TEXT, 6, '0');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_complaint_number
    BEFORE INSERT ON complaints
    FOR EACH ROW
    WHEN (NEW.complaint_number IS NULL)
    EXECUTE FUNCTION generate_complaint_number();

-- Auto-update upvote count
CREATE OR REPLACE FUNCTION update_upvote_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE complaints SET upvote_count = upvote_count + 1 WHERE id = NEW.complaint_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE complaints SET upvote_count = upvote_count - 1 WHERE id = OLD.complaint_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_upvote_count_insert
    AFTER INSERT ON complaint_upvotes
    FOR EACH ROW EXECUTE FUNCTION update_upvote_count();

CREATE TRIGGER trg_upvote_count_delete
    AFTER DELETE ON complaint_upvotes
    FOR EACH ROW EXECUTE FUNCTION update_upvote_count();

-- PostGIS location auto-population for complaints
CREATE OR REPLACE FUNCTION set_complaint_location()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.latitude IS NOT NULL AND NEW.longitude IS NOT NULL THEN
        NEW.location := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326)::geography;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_complaint_location
    BEFORE INSERT OR UPDATE OF latitude, longitude ON complaints
    FOR EACH ROW EXECUTE FUNCTION set_complaint_location();

-- PostGIS location for hotspots
CREATE OR REPLACE FUNCTION set_hotspot_location()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.center_latitude IS NOT NULL AND NEW.center_longitude IS NOT NULL THEN
        NEW.center_location := ST_SetSRID(ST_MakePoint(NEW.center_longitude, NEW.center_latitude), 4326)::geography;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hotspot_location
    BEFORE INSERT OR UPDATE OF center_latitude, center_longitude ON hotspots
    FOR EACH ROW EXECUTE FUNCTION set_hotspot_location();

-- ============================================================================
-- VIEWS
-- ============================================================================

-- Active schemes with application counts
CREATE OR REPLACE VIEW v_scheme_stats AS
SELECT
    s.*,
    COUNT(sa.id) AS total_applications,
    COUNT(sa.id) FILTER (WHERE sa.status = 'approved') AS approved_applications,
    COUNT(sa.id) FILTER (WHERE sa.status = 'bookmarked') AS bookmarked_count
FROM schemes s
LEFT JOIN scheme_applications sa ON s.id = sa.scheme_id
WHERE s.is_active = TRUE
GROUP BY s.id;

-- Complaint summary view
CREATE OR REPLACE VIEW v_complaint_summary AS
SELECT
    c.id,
    c.complaint_number,
    c.subject,
    c.category,
    c.status,
    c.priority,
    c.state,
    c.district,
    c.upvote_count,
    c.created_at,
    c.resolved_at,
    u.name AS complainant_name,
    d.name AS department_name,
    EXTRACT(EPOCH FROM (COALESCE(c.resolved_at, NOW()) - c.created_at)) / 3600 AS hours_open,
    (SELECT COUNT(*) FROM complaint_images ci WHERE ci.complaint_id = c.id) AS image_count,
    (SELECT COUNT(*) FROM complaint_updates cu WHERE cu.complaint_id = c.id) AS update_count
FROM complaints c
JOIN users u ON c.user_id = u.id
LEFT JOIN departments d ON c.department_id = d.id;

-- Hotspot leaderboard
CREATE OR REPLACE VIEW v_hotspot_leaderboard AS
SELECT
    state,
    district,
    category,
    COUNT(*) AS complaint_count,
    AVG(ai_priority_score) AS avg_priority,
    COUNT(*) FILTER (WHERE status NOT IN ('resolved', 'closed')) AS open_count
FROM complaints
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY state, district, category
HAVING COUNT(*) >= 3
ORDER BY complaint_count DESC;
