"""
Eligibility matching engine.

Implements a rule-based scoring system with support for multiple comparison
operators. Combines rule-engine scores with AI analysis for final eligibility.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# ════════════════════════════════════════════════════════════════════════
# Default Eligibility Rules (used when DB schemes have no rules defined)
# ════════════════════════════════════════════════════════════════════════

DEFAULT_ELIGIBILITY_RULES: Dict[str, Dict[str, Any]] = {
    "education": {
        "rules": [
            {"field": "age", "operator": "between", "value": [6, 25], "weight": 30, "mandatory": False},
            {"field": "annual_income", "operator": "lte", "value": 800000, "weight": 25, "mandatory": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "weight": 20, "mandatory": False},
            {"field": "is_bpl", "operator": "eq", "value": True, "weight": 15, "mandatory": False},
        ],
        "min_score": 40,
    },
    "health": {
        "rules": [
            {"field": "annual_income", "operator": "lte", "value": 500000, "weight": 35, "mandatory": True},
            {"field": "is_bpl", "operator": "eq", "value": True, "weight": 25, "mandatory": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "weight": 20, "mandatory": False},
        ],
        "min_score": 35,
    },
    "agriculture": {
        "rules": [
            {"field": "occupation", "operator": "in", "value": ["farmer", "agriculture", "kisan"], "weight": 40, "mandatory": True},
            {"field": "annual_income", "operator": "lte", "value": 600000, "weight": 25, "mandatory": False},
            {"field": "is_rural", "operator": "eq", "value": True, "weight": 20, "mandatory": False},
        ],
        "min_score": 40,
    },
    "housing": {
        "rules": [
            {"field": "annual_income", "operator": "lte", "value": 300000, "weight": 35, "mandatory": True},
            {"field": "is_bpl", "operator": "eq", "value": True, "weight": 25, "mandatory": False},
            {"field": "is_rural", "operator": "eq", "value": True, "weight": 15, "mandatory": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "ews"], "weight": 15, "mandatory": False},
        ],
        "min_score": 35,
    },
    "employment": {
        "rules": [
            {"field": "age", "operator": "between", "value": [18, 60], "weight": 30, "mandatory": True},
            {"field": "annual_income", "operator": "lte", "value": 500000, "weight": 25, "mandatory": False},
            {"field": "education", "operator": "in", "value": ["10th", "12th", "graduate", "post_graduate", "diploma"], "weight": 20, "mandatory": False},
        ],
        "min_score": 30,
    },
    "social_welfare": {
        "rules": [
            {"field": "annual_income", "operator": "lte", "value": 250000, "weight": 30, "mandatory": False},
            {"field": "is_bpl", "operator": "eq", "value": True, "weight": 25, "mandatory": False},
            {"field": "category", "operator": "in", "value": ["sc", "st", "obc", "ews"], "weight": 25, "mandatory": False},
        ],
        "min_score": 25,
    },
    "women_and_child": {
        "rules": [
            {"field": "gender", "operator": "eq", "value": "female", "weight": 40, "mandatory": True},
            {"field": "annual_income", "operator": "lte", "value": 500000, "weight": 25, "mandatory": False},
            {"field": "is_bpl", "operator": "eq", "value": True, "weight": 20, "mandatory": False},
        ],
        "min_score": 40,
    },
    "disability": {
        "rules": [
            {"field": "is_disabled", "operator": "eq", "value": True, "weight": 50, "mandatory": True},
            {"field": "annual_income", "operator": "lte", "value": 500000, "weight": 25, "mandatory": False},
        ],
        "min_score": 50,
    },
    "minority": {
        "rules": [
            {"field": "is_minority", "operator": "eq", "value": True, "weight": 40, "mandatory": True},
            {"field": "annual_income", "operator": "lte", "value": 600000, "weight": 25, "mandatory": False},
        ],
        "min_score": 40,
    },
}


# ════════════════════════════════════════════════════════════════════════
# Rule evaluation operators
# ════════════════════════════════════════════════════════════════════════

def _evaluate_rule(profile_value: Any, operator: str, rule_value: Any) -> bool:
    """Evaluate a single rule against a profile value."""
    if profile_value is None:
        return False

    try:
        if operator == "eq":
            if isinstance(profile_value, str) and isinstance(rule_value, str):
                return profile_value.lower() == rule_value.lower()
            return profile_value == rule_value

        elif operator == "neq":
            if isinstance(profile_value, str) and isinstance(rule_value, str):
                return profile_value.lower() != rule_value.lower()
            return profile_value != rule_value

        elif operator == "in":
            if isinstance(rule_value, list):
                if isinstance(profile_value, str):
                    return profile_value.lower() in [str(v).lower() for v in rule_value]
                return profile_value in rule_value
            return False

        elif operator == "not_in":
            if isinstance(rule_value, list):
                if isinstance(profile_value, str):
                    return profile_value.lower() not in [str(v).lower() for v in rule_value]
                return profile_value not in rule_value
            return True

        elif operator == "gte":
            return float(profile_value) >= float(rule_value)

        elif operator == "lte":
            return float(profile_value) <= float(rule_value)

        elif operator == "gt":
            return float(profile_value) > float(rule_value)

        elif operator == "lt":
            return float(profile_value) < float(rule_value)

        elif operator == "between":
            if isinstance(rule_value, list) and len(rule_value) == 2:
                return float(rule_value[0]) <= float(profile_value) <= float(rule_value[1])
            return False

        elif operator == "contains":
            if isinstance(profile_value, str) and isinstance(rule_value, str):
                return rule_value.lower() in profile_value.lower()
            return False

        else:
            logger.warning("Unknown operator: %s", operator)
            return False

    except (ValueError, TypeError) as e:
        logger.debug("Rule evaluation error: %s (operator=%s, value=%s vs %s)", e, operator, profile_value, rule_value)
        return False


# ════════════════════════════════════════════════════════════════════════
# Core scoring
# ════════════════════════════════════════════════════════════════════════

def calculate_eligibility_score(
    user_profile: Dict[str, Any],
    scheme_rules: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Calculate an eligibility score by evaluating all rules against the user profile.

    Args:
        user_profile: Dict with keys matching rule field names (age, gender, etc.)
        scheme_rules: Dict with "rules" (list of rule dicts) and "min_score" (int).

    Returns:
        Dict with keys: score, is_eligible, matched, unmatched, total_weight
    """
    rules = scheme_rules.get("rules", [])
    min_score = scheme_rules.get("min_score", 50)

    if not rules:
        return {
            "score": 0,
            "is_eligible": False,
            "matched": [],
            "unmatched": ["No eligibility rules defined"],
            "total_weight": 0,
        }

    total_weight = sum(r.get("weight", 10) for r in rules)
    earned_weight = 0
    matched: List[str] = []
    unmatched: List[str] = []
    mandatory_failed = False

    for rule in rules:
        field = rule.get("field", "")
        operator = rule.get("operator", "eq")
        value = rule.get("value")
        weight = rule.get("weight", 10)
        is_mandatory = rule.get("mandatory", False)

        profile_value = user_profile.get(field)
        rule_label = f"{field} {operator} {value}"

        passed = _evaluate_rule(profile_value, operator, value)

        if passed:
            earned_weight += weight
            matched.append(rule_label)
        else:
            unmatched.append(rule_label)
            if is_mandatory:
                mandatory_failed = True

    score = round((earned_weight / total_weight) * 100, 1) if total_weight > 0 else 0
    is_eligible = score >= min_score and not mandatory_failed

    return {
        "score": score,
        "is_eligible": is_eligible,
        "matched": matched,
        "unmatched": unmatched,
        "total_weight": total_weight,
    }


def load_eligibility_rules(scheme_category: str) -> Dict[str, Any]:
    """
    Load eligibility rules for a given scheme category.
    Falls back to default rules if no custom rules exist.
    """
    return DEFAULT_ELIGIBILITY_RULES.get(scheme_category, {
        "rules": [],
        "min_score": 50,
    })


def get_matching_schemes(
    user_profile: Dict[str, Any],
    schemes: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Evaluate all schemes against a user profile and return those the user
    is eligible for, sorted by score descending.

    Args:
        user_profile: User's profile data.
        schemes: List of scheme dicts, each with at least 'id', 'name', 'category',
                 and optionally 'eligibility_rules'.

    Returns:
        List of dicts with keys: scheme_id, scheme_name, score, is_eligible, matched, unmatched
    """
    results: List[Dict[str, Any]] = []

    for scheme in schemes:
        # Use scheme-specific rules if available, else default by category
        rules = scheme.get("eligibility_rules") or load_eligibility_rules(scheme.get("category", ""))
        if not rules or not rules.get("rules"):
            rules = load_eligibility_rules(scheme.get("category", ""))

        evaluation = calculate_eligibility_score(user_profile, rules)

        results.append({
            "scheme_id": scheme.get("id", ""),
            "scheme_name": scheme.get("name", ""),
            "category": scheme.get("category", ""),
            "score": evaluation["score"],
            "is_eligible": evaluation["is_eligible"],
            "matched": evaluation["matched"],
            "unmatched": evaluation["unmatched"],
        })

    # Sort eligible first, then by score descending
    results.sort(key=lambda x: (x["is_eligible"], x["score"]), reverse=True)
    return results
