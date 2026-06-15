"""
Multilingual translation service.

Wraps Gemini-based translation and provides static UI translation bundles
for the supported Indian languages.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from services.gemini_service import translate_text as _gemini_translate

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
}

# ════════════════════════════════════════════════════════════════════════
# Static UI translation bundles
# ════════════════════════════════════════════════════════════════════════

_UI_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "app_name": "CitizenAI",
        "home": "Home",
        "schemes": "Government Schemes",
        "complaints": "File a Complaint",
        "my_complaints": "My Complaints",
        "track_complaint": "Track Complaint",
        "login": "Login",
        "register": "Register",
        "profile": "My Profile",
        "logout": "Logout",
        "submit": "Submit",
        "cancel": "Cancel",
        "search": "Search",
        "filter": "Filter",
        "status": "Status",
        "priority": "Priority",
        "category": "Category",
        "description": "Description",
        "location": "Location",
        "date": "Date",
        "actions": "Actions",
        "view_details": "View Details",
        "check_eligibility": "Check Eligibility",
        "recommend_schemes": "Find Schemes for Me",
        "translate": "Translate",
        "dashboard": "Dashboard",
        "analytics": "Analytics",
        "hotspots": "Complaint Hotspots",
        "loading": "Loading...",
        "no_results": "No results found",
        "error_occurred": "An error occurred. Please try again.",
        "success": "Success!",
        "complaint_submitted": "Your complaint has been submitted successfully.",
        "tracking_id": "Tracking ID",
        "eligible": "You are eligible!",
        "not_eligible": "You may not be eligible.",
        "select_language": "Select Language",
    },
    "hi": {
        "app_name": "सिटीज़नAI",
        "home": "होम",
        "schemes": "सरकारी योजनाएं",
        "complaints": "शिकायत दर्ज करें",
        "my_complaints": "मेरी शिकायतें",
        "track_complaint": "शिकायत ट्रैक करें",
        "login": "लॉगिन",
        "register": "रजिस्टर",
        "profile": "मेरी प्रोफ़ाइल",
        "logout": "लॉगआउट",
        "submit": "जमा करें",
        "cancel": "रद्द करें",
        "search": "खोजें",
        "filter": "फ़िल्टर",
        "status": "स्थिति",
        "priority": "प्राथमिकता",
        "category": "श्रेणी",
        "description": "विवरण",
        "location": "स्थान",
        "date": "तारीख",
        "actions": "कार्रवाई",
        "view_details": "विवरण देखें",
        "check_eligibility": "पात्रता जांचें",
        "recommend_schemes": "मेरे लिए योजनाएं खोजें",
        "translate": "अनुवाद करें",
        "dashboard": "डैशबोर्ड",
        "analytics": "विश्लेषण",
        "hotspots": "शिकायत हॉटस्पॉट",
        "loading": "लोड हो रहा है...",
        "no_results": "कोई परिणाम नहीं मिला",
        "error_occurred": "एक त्रुटि हुई। कृपया पुनः प्रयास करें।",
        "success": "सफल!",
        "complaint_submitted": "आपकी शिकायत सफलतापूर्वक दर्ज हो गई है।",
        "tracking_id": "ट्रैकिंग आईडी",
        "eligible": "आप पात्र हैं!",
        "not_eligible": "आप पात्र नहीं हो सकते।",
        "select_language": "भाषा चुनें",
    },
    "ta": {
        "app_name": "சிட்டிசன்AI",
        "home": "முகப்பு",
        "schemes": "அரசு திட்டங்கள்",
        "complaints": "புகார் பதிவு",
        "my_complaints": "எனது புகார்கள்",
        "track_complaint": "புகார் கண்காணிப்பு",
        "login": "உள்நுழை",
        "register": "பதிவு செய்",
        "profile": "எனது சுயவிவரம்",
        "logout": "வெளியேறு",
        "submit": "சமர்ப்பி",
        "cancel": "ரத்து",
        "search": "தேடு",
        "filter": "வடிகட்டி",
        "status": "நிலை",
        "priority": "முன்னுரிமை",
        "category": "வகை",
        "description": "விளக்கம்",
        "location": "இடம்",
        "date": "தேதி",
        "actions": "செயல்கள்",
        "view_details": "விவரங்களைக் காண",
        "check_eligibility": "தகுதி சோதனை",
        "recommend_schemes": "எனக்கான திட்டங்கள்",
        "translate": "மொழிபெயர்",
        "dashboard": "டாஷ்போர்ட்",
        "analytics": "பகுப்பாய்வு",
        "hotspots": "புகார் ஹாட்ஸ்பாட்",
        "loading": "ஏற்றுகிறது...",
        "no_results": "முடிவுகள் இல்லை",
        "error_occurred": "பிழை ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
        "success": "வெற்றி!",
        "complaint_submitted": "உங்கள் புகார் வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது.",
        "tracking_id": "ட்ராக்கிங் ஐடி",
        "eligible": "நீங்கள் தகுதியானவர்!",
        "not_eligible": "நீங்கள் தகுதியற்றவராக இருக்கலாம்.",
        "select_language": "மொழியைத் தேர்ந்தெடுக்கவும்",
    },
    "te": {
        "app_name": "సిటిజన్AI",
        "home": "హోమ్",
        "schemes": "ప్రభుత్వ పథకాలు",
        "complaints": "ఫిర్యాదు దాఖలు",
        "my_complaints": "నా ఫిర్యాదులు",
        "track_complaint": "ఫిర్యాదు ట్రాక్",
        "login": "లాగిన్",
        "register": "రిజిస్టర్",
        "profile": "నా ప్రొఫైల్",
        "logout": "లాగౌట్",
        "submit": "సమర్పించు",
        "cancel": "రద్దు",
        "search": "శోధన",
        "filter": "ఫిల్టర్",
        "status": "స్థితి",
        "priority": "ప్రాధాన్యత",
        "category": "వర్గం",
        "description": "వివరణ",
        "location": "స్థానం",
        "date": "తేదీ",
        "actions": "చర్యలు",
        "view_details": "వివరాలు చూడండి",
        "check_eligibility": "అర్హత తనిఖీ",
        "recommend_schemes": "నాకు పథకాలు కనుగొనండి",
        "translate": "అనువాదం",
        "dashboard": "డాష్‌బోర్డ్",
        "analytics": "విశ్లేషణ",
        "hotspots": "ఫిర్యాదు హాట్‌స్పాట్‌లు",
        "loading": "లోడ్ అవుతోంది...",
        "no_results": "ఫలితాలు కనుగొనబడలేదు",
        "error_occurred": "లోపం సంభవించింది. దయచేసి మళ్ళీ ప్రయత్నించండి.",
        "success": "విజయం!",
        "complaint_submitted": "మీ ఫిర్యాదు విజయవంతంగా సమర్పించబడింది.",
        "tracking_id": "ట్రాకింగ్ ఐడి",
        "eligible": "మీరు అర్హులు!",
        "not_eligible": "మీరు అర్హులు కాకపోవచ్చు.",
        "select_language": "భాషను ఎంచుకోండి",
    },
    "kn": {
        "app_name": "ಸಿಟಿಜನ್AI",
        "home": "ಮುಖಪುಟ",
        "schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "complaints": "ದೂರು ನೀಡಿ",
        "my_complaints": "ನನ್ನ ದೂರುಗಳು",
        "track_complaint": "ದೂರು ಟ್ರ್ಯಾಕ್",
        "login": "ಲಾಗಿನ್",
        "register": "ನೋಂದಣಿ",
        "profile": "ನನ್ನ ಪ್ರೊಫೈಲ್",
        "logout": "ಲಾಗ್ಔಟ್",
        "submit": "ಸಲ್ಲಿಸಿ",
        "cancel": "ರದ್ದು",
        "search": "ಹುಡುಕಿ",
        "filter": "ಫಿಲ್ಟರ್",
        "status": "ಸ್ಥಿತಿ",
        "priority": "ಆದ್ಯತೆ",
        "category": "ವರ್ಗ",
        "description": "ವಿವರಣೆ",
        "location": "ಸ್ಥಳ",
        "date": "ದಿನಾಂಕ",
        "actions": "ಕ್ರಮಗಳು",
        "view_details": "ವಿವರಗಳನ್ನು ನೋಡಿ",
        "check_eligibility": "ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ",
        "recommend_schemes": "ನನಗಾಗಿ ಯೋಜನೆಗಳು",
        "translate": "ಅನುವಾದ",
        "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "analytics": "ವಿಶ್ಲೇಷಣೆ",
        "hotspots": "ದೂರು ಹಾಟ್‌ಸ್ಪಾಟ್",
        "loading": "ಲೋಡ್ ಆಗುತ್ತಿದೆ...",
        "no_results": "ಫಲಿತಾಂಶಗಳಿಲ್ಲ",
        "error_occurred": "ದೋಷ ಸಂಭವಿಸಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "success": "ಯಶಸ್ವಿ!",
        "complaint_submitted": "ನಿಮ್ಮ ದೂರು ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ.",
        "tracking_id": "ಟ್ರ್ಯಾಕಿಂಗ್ ಐಡಿ",
        "eligible": "ನೀವು ಅರ್ಹರು!",
        "not_eligible": "ನೀವು ಅರ್ಹರಲ್ಲದಿರಬಹುದು.",
        "select_language": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ",
    },
    "ml": {
        "app_name": "സിറ്റിസൺAI",
        "home": "ഹോം",
        "schemes": "സർക്കാർ പദ്ധതികൾ",
        "complaints": "പരാതി രജിസ്റ്റർ",
        "my_complaints": "എന്റെ പരാതികൾ",
        "track_complaint": "പരാതി ട്രാക്ക്",
        "login": "ലോഗിൻ",
        "register": "രജിസ്റ്റർ",
        "profile": "എന്റെ പ്രൊഫൈൽ",
        "logout": "ലോഗൗട്ട്",
        "submit": "സമർപ്പിക്കുക",
        "cancel": "റദ്ദാക്കുക",
        "search": "തിരയുക",
        "filter": "ഫിൽറ്റർ",
        "status": "സ്ഥിതി",
        "priority": "മുൻഗണന",
        "category": "വിഭാഗം",
        "description": "വിവരണം",
        "location": "സ്ഥലം",
        "date": "തീയതി",
        "actions": "നടപടികൾ",
        "view_details": "വിശദാംശങ്ങൾ കാണുക",
        "check_eligibility": "യോഗ്യത പരിശോധിക്കുക",
        "recommend_schemes": "എനിക്കുള്ള പദ്ധതികൾ",
        "translate": "പരിഭാഷ",
        "dashboard": "ഡാഷ്‌ബോർഡ്",
        "analytics": "വിശകലനം",
        "hotspots": "പരാതി ഹോട്ട്‌സ്പോട്ട്",
        "loading": "ലോഡ് ചെയ്യുന്നു...",
        "no_results": "ഫലങ്ങളൊന്നും കണ്ടെത്തിയില്ല",
        "error_occurred": "ഒരു പിശക് സംഭവിച്ചു. വീണ്ടും ശ്രമിക്കുക.",
        "success": "വിജയം!",
        "complaint_submitted": "നിങ്ങളുടെ പരാതി വിജയകരമായി സമർപ്പിച്ചു.",
        "tracking_id": "ട്രാക്കിംഗ് ഐഡി",
        "eligible": "നിങ്ങൾ യോഗ്യരാണ്!",
        "not_eligible": "നിങ്ങൾ യോഗ്യരല്ലായിരിക്കാം.",
        "select_language": "ഭാഷ തിരഞ്ഞെടുക്കുക",
    },
}


async def translate(text: str, target_lang: str, source_lang: str = "en") -> Dict[str, Any]:
    """
    Translate text to the target language. Uses Gemini AI.

    Args:
        text: Source text.
        target_lang: Target language code (en, hi, ta, te, kn, ml).
        source_lang: Source language code.

    Returns:
        Dict with translated_text, source_language, target_language.
    """
    if source_lang == target_lang:
        return {
            "translated_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
        }

    if target_lang not in SUPPORTED_LANGUAGES:
        return {
            "translated_text": text,
            "source_language": source_lang,
            "target_language": target_lang,
            "error": f"Unsupported target language: {target_lang}",
        }

    return await _gemini_translate(text, source_lang, target_lang)


def get_ui_translations(lang: str) -> Dict[str, str]:
    """
    Return the static UI translation bundle for the given language.
    Falls back to English if the language is not supported.
    """
    return _UI_TRANSLATIONS.get(lang, _UI_TRANSLATIONS["en"])


def get_supported_languages() -> List[Dict[str, str]]:
    """Return a list of supported language objects."""
    return [
        {"code": code, "name": name}
        for code, name in SUPPORTED_LANGUAGES.items()
    ]
