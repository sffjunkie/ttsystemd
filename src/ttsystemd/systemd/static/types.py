from dataclasses import dataclass
from typing import TypedDict

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
class SystemdJSONUnits:
    unit_files: list[JSONUnitFile]
    units: list[JSONUnit]


@dataclass
class CommandResult:
    returncode: int = -1
    text: str | None = None
    json: str | None = None


class UnitBackingFile(TypedDict):
    filename: str
    contents: str
