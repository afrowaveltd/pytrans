import json
import locale
from pathlib import Path

class LocalizationService:
    def __init__(self, language: str, path: Path = Path("./locales")):
        self.path = path
        self.language = self._detect_language(language)
        self._cache = {}

    def _detect_language(self, language: str) -> str:
        if language.lower() == "auto":
            lang_code, _ = locale.getdefaultlocale()
            return lang_code.split("_")[0] if lang_code else "en"
        return language
    
    def _load(self) -> dict:
        if self.language not in self._cache:
            locale_file = self.path / f"{self.language}.json"
            if locale_file.exists():
                with open(locale_file, "r", encoding="utf-8") as f:
                    self._cache[self.language] = json.load(f)
            else:
                self._cache[self.language] = {}
        return self._cache[self.language]
    
    def get(self, key: str) -> str:
        return self._load().get(key, key)