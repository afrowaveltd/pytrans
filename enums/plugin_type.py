from enum import auto

try:
    from enum import StrEnum # type: ignore
except ImportError:
    from enum import Enum
    class StrEnum(str, Enum):
        pass

class PluginType(StrEnum):

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    DATA_ACCESSOR = auto()
    BACKEND = auto()
    TRANSLATOR = auto()
    MIDDLEWARE = auto()
    SCHEDULER = auto()
    CUSTOM = auto()