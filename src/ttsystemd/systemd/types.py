from enum import Enum, StrEnum, auto
from typing import Any

Properties = dict[str, Any]


class SessionType(Enum):
    SYSTEM = auto()  #: System
    USER_SESSION = auto()  #: User Session


class UnitType(StrEnum):
    Automount = "automount"
    Device = "device"
    Mount = "mount"
    Path = "path"
    Scope = "scope"
    Service = "service"
    Slice = "slice"
    Socket = "socket"
    Swap = "swap"
    Target = "target"
    Timer = "timer"
