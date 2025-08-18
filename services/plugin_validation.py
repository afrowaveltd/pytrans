from typing import Mapping, Set
from enums.plugin_type import PluginType
from models.plugin import Plugin

REQUIRED_BY_TYPE: Mapping[PluginType, Set[str]] = {
    PluginType.DATA_ACCESSOR: {"endpoint", "method"},
    PluginType.BACKEND: {"connection_string"},
    PluginType.TRANSLATOR: {"server_url"},
    PluginType.MIDDLEWARE: set(),
    PluginType.SCHEDULER: {"cron"},
    PluginType.CUSTOM: set(),
}

ALLOWED_BY_TYPE: Mapping[PluginType, Set[str]] = {
    PluginType.DATA_ACCESSOR: {"endpoint", "method", "auth_token"},
    PluginType.BACKEND: {"connection_string", "cache_enabled"},
    PluginType.TRANSLATOR: {"server_url", "api_key", "timeout"},
    PluginType.MIDDLEWARE: {"order", "enabled"},
    PluginType.SCHEDULER: {"cron", "timezone"},
    PluginType.CUSTOM: set(),  # volné – nebo vyplň později
}

def validate_plugin(p: Plugin) -> None:
    req = REQUIRED_BY_TYPE.get(p.plugin_type, set())
    allowed = ALLOWED_BY_TYPE.get(p.plugin_type, set())
    missing = req - set(p.params.keys())
    if missing:
        raise ValueError(f"Missing required for {p.plugin_type.value}: {sorted(missing)}")
    unknown = set(p.params.keys()) - allowed
    if unknown:
        raise ValueError(f"Unknown params for {p.plugin_type.value}: {sorted(unknown)}")
