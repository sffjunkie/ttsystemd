from enum import Enum, StrEnum, auto


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
    Target = "target"
    Timer = "timer"
