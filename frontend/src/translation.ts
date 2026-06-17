const translations: Record<string, Record<string, string>> = {
  en: {
    welcome: "Welcome",
    home: "Home",
    about: "About",
    contact: "Contact",
    // Add all your English translations here
  },
  hi: {
    welcome: "स्वागत है",
    home: "होम",
    about: "परिचय",
    contact: "संपर्क",
    // Add all your Hindi translations here
  },
  ta: {
    welcome: "வரவேற்கிறோம்",
    home: "முகப்பு",
    about: "பற்றி",
    contact: "தொடர்பு",
  },
  te: {
    welcome: "స్వాగతం",
    home: "హోమ్",
    about: "గురించి",
    contact: "సంపర్కం",
  },
  kn: {
    welcome: "ಸ್ವಾಗತ",
    home: "ಮನೆ",
    about: "ಬಗ್ಗೆ",
    contact: "ಸಂಪರ್ಕ",
  },
  ml: {
    welcome: "സ്വാഗതം",
    home: "ഹോം",
    about: "വിവരണം",
    contact: "ബന്ധം",
  },
};

export function getTranslation(key: string, language: string): string {
  return translations[language]?.[key] ?? key;
}
