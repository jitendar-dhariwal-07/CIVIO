"""
Google Gemini AI integration service.
Provides AI-powered features: complaint classification, priority generation,
summarization, scheme recommendation, eligibility analysis, and translation.

Every prompt is production-ready with detailed role definitions, context about
Indian governance, structured JSON output formats, examples, and edge-case handling.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_model: Optional[genai.GenerativeModel] = None


def initialize_gemini() -> None:
    """Configure the Gemini SDK and warm up the model instance."""
    global _model
    if not settings.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set – AI features will be unavailable.")
        return
    genai.configure(api_key=settings.GEMINI_API_KEY)
    _model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        generation_config=genai.GenerationConfig(
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
        ),
    )
    logger.info("Gemini AI model '%s' initialized successfully.", settings.GEMINI_MODEL)


def _get_model() -> genai.GenerativeModel:
    """Return the cached model; initialise lazily if needed."""
    global _model
    if _model is None:
        initialize_gemini()
    if _model is None:
        raise RuntimeError("Gemini AI is not available. Set GEMINI_API_KEY in .env")
    return _model


def _safe_parse_json(text: str) -> Any:
    """Best-effort JSON extraction from Gemini's response."""
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find the first { ... } or [ ... ] block
        start = text.find("{")
        if start == -1:
            start = text.find("[")
        if start != -1:
            try:
                return json.loads(text[start:])
            except json.JSONDecodeError:
                pass
    return {"raw_text": text}


# ════════════════════════════════════════════════════════════════════════
# 1. Classify Complaint
# ════════════════════════════════════════════════════════════════════════

async def classify_complaint(text: str, image_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Classify a citizen's complaint into a predefined category, identify
    a sub-category, extract keywords, and provide reasoning.

    Returns dict with keys: category, confidence, sub_category, keywords, reasoning
    """
    prompt = f"""You are an expert Indian government complaint classification officer with deep
knowledge of municipal services, state and central government departments, and
citizen grievance redressal systems across India (CPGRAMS, IGMS, state portals).

YOUR TASK:
Classify the following citizen complaint into exactly ONE primary category from
the allowed list. Also identify a sub-category, extract relevant keywords, and
explain your reasoning.

ALLOWED CATEGORIES (use the exact string):
- roads              → Potholes, road damage, construction delays, missing signage, road encroachments
- water_supply       → Water shortage, contaminated water, pipeline leaks, irregular supply, borewell issues
- electricity        → Power outages, voltage fluctuation, illegal connections, street light faults, billing disputes
- sanitation         → Garbage collection, open drains, sewage overflow, public toilet maintenance, vector breeding
- public_transport   → Bus/metro delays, overcrowding, route issues, safety, fare problems
- healthcare         → Hospital services, medicine shortage, doctor availability, ambulance, insurance
- education          → School infrastructure, teacher shortage, mid-day meal, scholarship, exam issues
- pollution          → Air, water, noise, industrial pollution, construction dust
- corruption         → Bribery, embezzlement, nepotism, tender irregularities
- public_safety      → Crime, harassment, missing persons, fire safety, disaster relief
- housing            → Encroachment, building permission, housing scheme, rent disputes
- food_safety        → Food adulteration, license violations, restaurant hygiene
- telecom            → Network issues, broadband, SIM fraud, spam calls
- banking            → Account issues, loan fraud, ATM, digital payment failures
- government_service → Aadhaar, ration card, passport, pension, certificate delays
- other              → Anything that does not fit the above categories

RULES:
1. Choose the MOST specific matching category.
2. If the complaint spans multiple categories, pick the primary one that the citizen
   is most concerned about.
3. Confidence should be between 0.0 and 1.0. Use values above 0.8 only when the
   match is unambiguous.
4. Keywords should be 3-7 relevant words from the complaint.
5. Be sensitive to regional Indian English, Hindi transliterations, and colloquial terms
   (e.g., "nala" = drain, "bijli" = electricity, "sadak" = road).

COMPLAINT TEXT:
\"\"\"
{text}
\"\"\"

RESPOND in this exact JSON format:
{{
  "category": "<category_string>",
  "confidence": <float 0.0-1.0>,
  "sub_category": "<more specific label>",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "reasoning": "<1-2 sentence explanation>"
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        result = _safe_parse_json(response.text)
        # Validate category
        valid_categories = [
            "roads", "water_supply", "electricity", "sanitation", "public_transport",
            "healthcare", "education", "pollution", "corruption", "public_safety",
            "housing", "food_safety", "telecom", "banking", "government_service", "other",
        ]
        if result.get("category") not in valid_categories:
            result["category"] = "other"
        return result
    except Exception as e:
        logger.error("Complaint classification failed: %s", e)
        return {
            "category": "other",
            "confidence": 0.0,
            "sub_category": "unknown",
            "keywords": [],
            "reasoning": f"Classification failed: {str(e)}",
        }


# ════════════════════════════════════════════════════════════════════════
# 2. Generate Priority
# ════════════════════════════════════════════════════════════════════════

async def generate_priority(text: str, category: str) -> Dict[str, Any]:
    """
    Determine the priority level of a complaint based on its content, category,
    urgency indicators, and potential public impact.

    Returns dict with keys: priority, score, reasoning, urgency_indicators
    """
    prompt = f"""You are an AI-powered grievance triage officer working for the Government of India's
citizen complaint management system. You must assess the PRIORITY of a citizen
complaint so that critical issues receive immediate attention.

PRIORITY LEVELS (use exact string):
- critical → Immediate danger to life, health emergency, communal tension, large-scale
              infrastructure failure, natural disaster impact. Expected response: < 4 hours.
- high     → Significant public inconvenience, safety risks, affects vulnerable populations
              (children, elderly, disabled), widespread service disruption. Response: < 24 hours.
- medium   → Moderate inconvenience, affects a neighbourhood or locality, non-emergency
              service failures, pending beyond normal SLA. Response: < 72 hours.
- low      → Minor inconvenience, cosmetic issues, information requests, already partially
              addressed. Response: < 7 days.

ASSESSMENT CRITERIA (weighted):
1. **Life & Safety Risk** (weight: 40%) — Is anyone in physical danger?
2. **Scale of Impact** (weight: 25%) — How many people are affected?
3. **Vulnerability** (weight: 15%) — Does it affect children, elderly, disabled, pregnant women?
4. **Duration** (weight: 10%) — How long has the problem persisted?
5. **Public Sentiment** (weight: 10%) — Could this escalate or draw media attention?

COMPLAINT CATEGORY: {category}
COMPLAINT TEXT:
\"\"\"
{text}
\"\"\"

Identify any urgency indicators (e.g., "children sick", "no water for 3 days",
"live wire exposed", "pregnant woman") and factor them into your assessment.

RESPOND in this exact JSON format:
{{
  "priority": "<critical|high|medium|low>",
  "score": <integer 1-100, where 100 is most urgent>,
  "reasoning": "<2-3 sentence explanation of your assessment>",
  "urgency_indicators": ["indicator1", "indicator2"]
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        result = _safe_parse_json(response.text)
        valid_priorities = ["low", "medium", "high", "critical"]
        if result.get("priority") not in valid_priorities:
            result["priority"] = "medium"
        return result
    except Exception as e:
        logger.error("Priority generation failed: %s", e)
        return {
            "priority": "medium",
            "score": 50,
            "reasoning": f"Auto-assigned medium priority. AI error: {str(e)}",
            "urgency_indicators": [],
        }


# ════════════════════════════════════════════════════════════════════════
# 3. Summarize Complaint
# ════════════════════════════════════════════════════════════════════════

async def summarize_complaint(text: str) -> Dict[str, Any]:
    """
    Generate a concise, actionable summary of a citizen complaint.

    Returns dict with keys: summary, key_issues, affected_area, urgency_indicators
    """
    prompt = f"""You are a senior government analyst summarizing citizen complaints for quick review
by officials in India's grievance redressal system. Your summaries are used in
dashboards and notification alerts, so they must be concise yet complete.

GUIDELINES:
1. The summary must be 1-2 sentences (max 50 words).
2. Capture: WHAT is the problem, WHERE is it, WHO is affected, and HOW LONG
   has it persisted (if mentioned).
3. Identify 2-5 key issues as bullet points.
4. Identify the affected area (locality, ward, village, etc.) if mentioned.
5. List any urgency indicators (health risk, safety hazard, etc.).
6. Maintain neutral, professional tone. Do not editorialise.
7. If the complaint is in Hindi or another Indian language transliterated in English,
   still produce the summary in clear English.

COMPLAINT TEXT:
\"\"\"
{text}
\"\"\"

RESPOND in this exact JSON format:
{{
  "summary": "<concise summary, max 50 words>",
  "key_issues": ["issue1", "issue2"],
  "affected_area": "<area name or null>",
  "urgency_indicators": ["indicator1", "indicator2"]
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return _safe_parse_json(response.text)
    except Exception as e:
        logger.error("Complaint summarization failed: %s", e)
        return {
            "summary": text[:150] + ("..." if len(text) > 150 else ""),
            "key_issues": [],
            "affected_area": None,
            "urgency_indicators": [],
        }


# ════════════════════════════════════════════════════════════════════════
# 4. Recommend Schemes
# ════════════════════════════════════════════════════════════════════════

async def recommend_schemes(
    user_profile: Dict[str, Any],
    available_schemes: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    AI-powered scheme recommendation based on a citizen's profile and
    the catalogue of available government schemes.

    Returns a list of dicts with keys: scheme_id, relevance_score, match_reasons, summary
    """
    # Truncate scheme list to avoid token overflow – send name + id + eligibility only
    scheme_summaries = []
    for s in available_schemes[:50]:
        scheme_summaries.append({
            "id": s.get("id"),
            "name": s.get("name"),
            "category": s.get("category"),
            "level": s.get("level"),
            "state": s.get("state"),
            "eligibility_criteria": s.get("eligibility_criteria", "")[:300],
            "benefits": s.get("benefits", "")[:200],
        })

    prompt = f"""You are a Government of India welfare scheme advisor AI. Your role is to help
Indian citizens discover government schemes (central and state) they are eligible for.

You have extensive knowledge of schemes like PM-KISAN, PMJDY, MGNREGA, Ayushman Bharat,
Ujjwala Yojana, Mudra Yojana, Digital India, Skill India, Beti Bachao Beti Padhao, etc.

CITIZEN PROFILE:
{json.dumps(user_profile, indent=2, default=str)}

AVAILABLE SCHEMES (catalogue):
{json.dumps(scheme_summaries, indent=2, default=str)}

INSTRUCTIONS:
1. Analyse the citizen's age, gender, income, location, category (SC/ST/OBC/EWS/General),
   disability status, BPL status, rural/urban, occupation, and education.
2. Match them against each scheme's eligibility criteria.
3. Return the TOP 10 most relevant schemes, ranked by relevance.
4. For each, provide:
   - scheme_id (from the catalogue)
   - relevance_score (0-100, where 100 = perfect match)
   - match_reasons (list of 2-4 reasons why this scheme is relevant)
   - summary (1 sentence explaining what the citizen would get)
5. Consider state-specific schemes only if the citizen's state matches.
6. Central schemes are available to all states.
7. If the citizen is BPL, prioritise poverty alleviation schemes.
8. If the citizen is female, include women-specific schemes.
9. If the citizen is disabled, include disability welfare schemes.

RESPOND in this exact JSON format:
{{
  "recommendations": [
    {{
      "scheme_id": "<id>",
      "relevance_score": <0-100>,
      "match_reasons": ["reason1", "reason2"],
      "summary": "<what the citizen gets>"
    }}
  ]
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        result = _safe_parse_json(response.text)
        return result.get("recommendations", [])
    except Exception as e:
        logger.error("Scheme recommendation failed: %s", e)
        return []


# ════════════════════════════════════════════════════════════════════════
# 5. Check Eligibility
# ════════════════════════════════════════════════════════════════════════

async def check_eligibility(
    user_profile: Dict[str, Any],
    scheme: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Perform a detailed eligibility analysis for a citizen against a specific
    government scheme.

    Returns dict with keys: is_eligible, score, matched_criteria, unmatched_criteria,
    explanation, documents_needed, next_steps
    """
    prompt = f"""You are a meticulous Government of India eligibility verification officer. You must
determine whether a citizen is eligible for a specific government scheme by
cross-referencing their profile against the scheme's eligibility criteria.

SCHEME DETAILS:
- Name: {scheme.get('name', 'Unknown')}
- Category: {scheme.get('category', 'Unknown')}
- Level: {scheme.get('level', 'Unknown')}
- Eligibility Criteria: {scheme.get('eligibility_criteria', 'Not specified')}
- Benefits: {scheme.get('benefits', 'Not specified')}
- Eligibility Rules (structured): {json.dumps(scheme.get('eligibility_rules', {}), default=str)}
- Documents Required: {json.dumps(scheme.get('documents_required', []), default=str)}

CITIZEN PROFILE:
{json.dumps(user_profile, indent=2, default=str)}

INSTRUCTIONS:
1. Check EACH eligibility criterion against the citizen's profile.
2. Mark each criterion as "matched" or "unmatched".
3. If a criterion cannot be verified (data missing), mark as "unmatched" but note
   "data not provided" in the explanation.
4. Calculate an eligibility score from 0-100:
   - 100 = All criteria matched
   - 0 = No criteria matched
   - Partial matches get proportional scores
5. A citizen is "eligible" if their score >= 60 AND no mandatory criteria are unmatched.
6. Provide a clear, citizen-friendly explanation in simple English.
7. List the documents the citizen would need to apply.
8. Suggest concrete next steps.

RESPOND in this exact JSON format:
{{
  "is_eligible": <true|false>,
  "score": <0-100>,
  "matched_criteria": ["criterion1", "criterion2"],
  "unmatched_criteria": ["criterion3"],
  "explanation": "<citizen-friendly explanation, 2-3 sentences>",
  "documents_needed": ["doc1", "doc2"],
  "next_steps": ["step1", "step2"]
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return _safe_parse_json(response.text)
    except Exception as e:
        logger.error("Eligibility check failed: %s", e)
        return {
            "is_eligible": False,
            "score": 0,
            "matched_criteria": [],
            "unmatched_criteria": ["Unable to verify – AI service error"],
            "explanation": f"Eligibility check could not be completed: {str(e)}",
            "documents_needed": [],
            "next_steps": ["Please try again or visit your nearest CSC centre."],
        }


# ════════════════════════════════════════════════════════════════════════
# 6. Translate Text
# ════════════════════════════════════════════════════════════════════════

async def translate_text(
    text: str,
    source_lang: str = "en",
    target_lang: str = "hi",
) -> Dict[str, Any]:
    """
    Translate text between Indian languages using Gemini.

    Returns dict with keys: translated_text, source_language, target_language
    """
    lang_names = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
        "mr": "Marathi",
        "bn": "Bengali",
        "gu": "Gujarati",
        "pa": "Punjabi",
        "ur": "Urdu",
    }

    source_name = lang_names.get(source_lang, source_lang)
    target_name = lang_names.get(target_lang, target_lang)

    prompt = f"""You are a professional Indian government translator. Translate the following
text from {source_name} to {target_name}.

RULES:
1. Maintain the original meaning and tone.
2. Use simple, citizen-friendly language.
3. Keep government/technical terms in their commonly understood form in the target language.
4. Do NOT transliterate – use the native script of the target language.
5. If the text contains proper nouns (names, places), keep them as-is or use the
   standard target-language form if one exists.
6. If the source text contains a mix of languages, translate the entire text into the
   target language.
7. Preserve any numbers, dates, and reference IDs exactly as they appear.

TEXT TO TRANSLATE:
\"\"\"
{text}
\"\"\"

RESPOND in this exact JSON format:
{{
  "translated_text": "<translated text in target language script>",
  "source_language": "{source_lang}",
  "target_language": "{target_lang}"
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return _safe_parse_json(response.text)
    except Exception as e:
        logger.error("Translation failed: %s", e)
        return {
            "translated_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
            "error": str(e),
        }


# ════════════════════════════════════════════════════════════════════════
# 7. Explain Scheme in Simple Language
# ════════════════════════════════════════════════════════════════════════

async def explain_scheme_simple(
    scheme: Dict[str, Any],
    language: str = "en",
) -> Dict[str, Any]:
    """
    Explain a government scheme in simple, easy-to-understand language,
    optionally in a regional Indian language.

    Returns dict with keys: explanation, who_can_apply, what_you_get, how_to_apply
    """
    lang_names = {
        "en": "English",
        "hi": "Hindi",
        "ta": "Tamil",
        "te": "Telugu",
        "kn": "Kannada",
        "ml": "Malayalam",
    }
    lang_name = lang_names.get(language, "English")

    prompt = f"""You are a friendly Indian government scheme explainer. Your audience is common
citizens, many of whom may have limited education. You must explain the following
government scheme in very simple {lang_name}.

SCHEME DETAILS:
- Name: {scheme.get('name', 'Unknown')}
- Ministry: {scheme.get('ministry', 'Unknown')}
- Category: {scheme.get('category', 'Unknown')}
- Description: {scheme.get('description', '')}
- Benefits: {scheme.get('benefits', '')}
- Eligibility: {scheme.get('eligibility_criteria', '')}
- Application Process: {scheme.get('application_process', '')}
- Documents Required: {json.dumps(scheme.get('documents_required', []), default=str)}

INSTRUCTIONS:
1. Use SIMPLE language – imagine explaining to a farmer or a daily wage worker.
2. Avoid bureaucratic jargon.
3. Use bullet points and short sentences.
4. If the language is not English, write in the native script of that language.
5. Include relatable examples (e.g., "If you are a farmer with less than 2 hectares…").
6. Explain the benefit in terms of what the citizen actually receives (money, service, etc.).
7. Make the application process sound easy and achievable.

RESPOND in this exact JSON format:
{{
  "explanation": "<simple overall explanation, 3-5 sentences>",
  "who_can_apply": "<who is eligible, in simple terms>",
  "what_you_get": "<what benefits you receive>",
  "how_to_apply": "<step-by-step in simple language>",
  "language": "{language}"
}}"""

    try:
        model = _get_model()
        response = model.generate_content(prompt)
        return _safe_parse_json(response.text)
    except Exception as e:
        logger.error("Scheme explanation failed: %s", e)
        return {
            "explanation": scheme.get("description", ""),
            "who_can_apply": scheme.get("eligibility_criteria", ""),
            "what_you_get": scheme.get("benefits", ""),
            "how_to_apply": scheme.get("application_process", ""),
            "language": language,
            "error": str(e),
        }
