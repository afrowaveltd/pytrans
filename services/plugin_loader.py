# services/plugin_loader.py
import json
from pathlib import Path
from typing import Iterable, List
from enums.plugin_type import PluginType
from models.plugin import Plugin
from services.plugin_validation import validate_plugin

def load_plugins(path: Path = Path("./settings/plugins.json")) -> List[Plugin]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    plugins: List[Plugin] = []
    for item in data:
        ptype = PluginType(item["plugin_type"])  # "translator" -> PluginType.TRANSLATOR
        p = Plugin(name=item["name"], plugin_type=ptype, params=item.get("params", {}))
        validate_plugin(p)
        plugins.append(p)
    return plugins
