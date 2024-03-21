from dataclasses import dataclass
from typing import TypedDict, NotRequired, Any

from ttsystemd.systemd.types import UnitType


@dataclass
class JSONUnitFile:
    unit_file: str
    state: str
    preset: str | None


@dataclass
class JSONUnit:
    unit_type: UnitType
    unit_name: str
    load: str
    active: str
    sub: str
    description: str


@dataclass
class JSONUnitInfo:
    unit_files: dict[str, JSONUnitFile]
    units: dict[str, JSONUnit]


@dataclass
class CommandResult:
    returncode: int | None = -1
    text: str | None = None
    json: Any | None = None


class UnitBackingFile(TypedDict):
    filename: NotRequired[str]
    contents: NotRequired[str]
