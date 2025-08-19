# ui/icons.py
# Sada bezpečných ikon s fallbacky (1-cell znaky). Lze přepnout v settings: icon_set = "text" | "emoji" | "none".

ICON_SETS = {
    "emoji": {
        "home": "🏠",
        "back": "⬅️",
        "targets": "🎯",
        "scheduler": "⏱️",
        "plugins": "🧩",
        "dictionaries": "📚",
        "settings": "⚙️",
    },
    "text": {  # preferovaná výchozí sada – stabilní šířka
        "home": "⌂",
        "back": "←",
        "targets": "◆",
        "scheduler": "⏱︎",   # U+23F1 + FE0E (text presentation)
        "plugins": "⊞",
        "dictionaries": "≡",
        "settings": "⚙︎",   # U+2699 + FE0E
    },
    "none": {
        "home": "", "back": "", "targets": "", "scheduler": "",
        "plugins": "", "dictionaries": "", "settings": "",
    },
}

def icon(name: str, set_name: str) -> str:
    """Vrátí symbol ikony podle aktuální sady (s bezpečným fallbackem)."""
    return ICON_SETS.get(set_name, ICON_SETS["text"]).get(name, "")
