
import json
from pathlib import Path
from typing import Any, Dict, Optional
import uuid

DEFAULTS: Dict[str, Any] = {
    "language": "en",
    "theme": "textual-dark",
    "application-id": "",  # will be filled on first run
    "icon_set": "text"   # << přidáno: "text" | "emoji" | "none"
}

class Settings:
    def __init__(self, file_path: Path = Path("./settings/settings.json")) -> None:
        self.file_path = Path(file_path)
        self.settings: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.file_path.exists():
            self.settings = json.loads(self.file_path.read_text(encoding="utf-8"))
        else:
            self.settings = DEFAULTS.copy()

        # Migration & defaults
        if not self.settings.get("application-id"):
            # Support legacy key 'id'
            legacy = self.settings.get("id")
            self.settings["application-id"] = legacy or str(uuid.uuid4())
        for k, v in DEFAULTS.items():
            self.settings.setdefault(k, v)

        self._save()  # ensure file exists and defaults applied

    def _save(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file_path.write_text(json.dumps(self.settings, ensure_ascii=False, indent=4), encoding="utf-8")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self._save()

    @property
    def language(self) -> str:
        return str(self.get("language", "en"))

    @property
    def theme(self) -> str:
        return str(self.get("theme", "textual-dark"))

    @property
    def application_id(self) -> str:
        return str(self.get("application-id", ""))

    @property
    def icon_set(self) -> str:
        return self .get("icon_set", "text")
