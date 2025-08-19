
import json
import locale
from pathlib import Path
from typing import Dict, Any

class LocalizationService:
    """Simple i18n loader with fallback to 'en' and string interpolation."""
    def __init__(self, language: str, path: Path = Path("./locales")):
        self.path = Path(path)
        self.lang = self._detect_language(language or "en")
        self._cache: Dict[str, Dict[str, str]] = {}

    def _detect_language(self, language: str) -> str:
        if language.lower() == "auto":
            try:
                lang_code, _ = locale.getdefaultlocale()
            except Exception:
                lang_code = None
            return (lang_code.split("_")[0] if lang_code else "en").lower()
        return language.lower()

    def _load_lang(self, lang: str) -> Dict[str, str]:
        if lang not in self._cache:
            file = self.path / f"{lang}.json"
            if file.exists():
                self._cache[lang] = json.loads(file.read_text(encoding="utf-8"))
            else:
                self._cache[lang] = {}
        return self._cache[lang]

    def set_language(self, language: str) -> None:
        self.lang = self._detect_language(language)
        # Lazy reload: clear only active lang cache; keep others
        self._cache.pop(self.lang, None)

    def reload(self) -> None:
        self._cache.clear()

    def has(self, key: str) -> bool:
        return key in self._load_lang(self.lang) or key in self._load_lang("en")

    def t(self, key: str, **vars: Any) -> str:
        """Translate key with fallback to English; if missing, return key itself."""
        data = self._load_lang(self.lang)
        if key in data:
            value = data[key]
        else:
            value = self._load_lang("en").get(key, key)
        # simple interpolation using str.format style
        try:
            return value.format(**vars) if vars else value
        except Exception:
            # If formatting fails, return raw to avoid crashing UI
            return value

    # Backwards compatibility for your previous `.get()` usage
    def get(self, key: str) -> str:
        return self.t(key)
