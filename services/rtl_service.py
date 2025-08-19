# services/rtl_service.py
from __future__ import annotations
import json
from pathlib import Path

class RTLService:
    def __init__(self, languages_json: str | Path) -> None:
        self._rtl = set()
        p = Path(languages_json)
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                # očekává se struktura: { "ar": {"rtl": true}, "he": {"rtl": true}, ... }
                for code, info in data.items():
                    if isinstance(info, dict) and info.get("rtl") is True:
                        self._rtl.add(code.lower())
            except Exception:
                pass

    def is_rtl(self, lang: str) -> bool:
        if not lang:
            return False
        # "ar", "ar-SA" → testuj prefix
        lang = lang.lower()
        if lang in self._rtl:
            return True
        base = lang.split("-", 1)[0]
        return base in self._rtl
