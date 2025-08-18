import json
from pathlib import Path

class Settings: 
    def __init__(self, file_path: Path = Path("./settings/settings.json")):
        self.file_path = file_path
        self._load()

    def _load(self):
        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        else:
            # Create default settings
            self.settings = {
                "language": "en",
                "theme": "dark",
                "id": "", # to do - generate GUID 
            }
            self._save()

    
    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value):
        self.settings[key] = value
        self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=4)

    @property
    def all(self):
        return self.settings
    
    @property
    def language(self) -> str:
        return self.get("language", "en") # pyright: ignore[reportReturnType]

    @property
    def theme(self) -> str:
        return self.get("theme", "dark") # pyright: ignore[reportReturnType]