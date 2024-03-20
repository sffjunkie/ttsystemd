from dataclasses import dataclass
from typing import Any, Callable

from dbus_next.constants import BusType

from ttsystemd.systemd.types import UnitType

Properties = dict[str, Any]
ValueFormatter = Callable[[Any], str]


@dataclass
class DBusUnitProperties:
    device: Properties | None
    mount: Properties | None
    scope: Properties | None
    service: Properties | None
    socket: Properties | None
    swap: Properties | None
    unit: Properties | None


@dataclass
class DBusUnitFile:
    unit_type: UnitType
    unit_name: str
    unit_path: str
    enable: str


@dataclass
class DBusUnit:
    unit_type: UnitType
    unit_name: str
    description: str
    load_state: str
    active_state: str
    sub_state: str
    followed: str
    object_path: str
    job_id: int
    job_type: str
    job_object_path: str


@dataclass
class DBusUnitInfo:
    units: list[DBusUnit]
    unit_files: list[DBusUnitFile]


@dataclass
class Process:
    service: str
    pid: int
    command_line: str
