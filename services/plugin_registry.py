from typing import Callable
from enums.plugin_type import PluginType
from models.plugin import Plugin

Handler = Callable[[Plugin], None]

def handle_backend(p: Plugin) -> None:
    # TODO: napojení na tvoje backendy
    ...

def handle_translator(p: Plugin) -> None:
    ...

REGISTRY: dict[PluginType, Handler] = {
    PluginType.BACKEND: handle_backend,
    PluginType.TRANSLATOR: handle_translator,
    # ostatní doplníš
}

def run_plugin(p: Plugin) -> None:
    REGISTRY[p.plugin_type](p)