from dataclasses import dataclass, field
from typing import Any, Mapping
from enums.plugin_type import PluginType

@dataclass(slots = True)
class Plugin:
    name: str
    plugin_type: PluginType
    params: Mapping[str, Any] = field(default_factory=dict)