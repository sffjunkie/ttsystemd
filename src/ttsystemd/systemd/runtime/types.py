from dataclasses import dataclass
from typing import Any, Callable

from dbus_next.constants import BusType

from ttsystemd.systemd.types import UnitType

SystemdDBusProperties = dict[str, Any] | None
ValueFormatter = Callable[[Any], str]


@dataclass
class DBusUnitInterfaceProperties:
    device: SystemdDBusProperties | None
    mount: SystemdDBusProperties | None
    scope: SystemdDBusProperties | None
    service: SystemdDBusProperties | None
    socket: SystemdDBusProperties | None
    unit: SystemdDBusProperties | None


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
class SystemdDBusProperties:
    bus_type: BusType
    properties: SystemdDBusProperties


@dataclass
class SystemdDBusUnits:
    bus_type: BusType
    units: list[DBusUnit]
    unit_files: list[DBusUnitFile]


@dataclass
class Process:
    service: str
    pid: int
    command_line: str


@dataclass
class ServiceInfo:
    processes: list[Process]
    allowed_cpus: list[int]
    allowed_memory_nodes: list[int]
    ambient_capabilities: int
    app_armor_profile: str
    bpf_program: tuple[str, str]
    bind_paths: tuple[str, str, int, int]
    bind_read_only_paths: tuple[str, str, int, int]
    block_io_accounting: bool
    block_io_device_weight: tuple[str, int]
    block_io_read_bandwidth: tuple[str, int]
    block_io_weight: int
    block_io_write_bandwidth: tuple[str, int]
    bus_name: str
    cpu_accounting: bool
    cpu_affinity: bytes
    cpu_affinity_from_numa: bool
    cpu_quota_per_sec_usec: int


@dataclass
class UnitInfo: ...


@dataclass
class Service:
    unit_info: UnitInfo
    service_info: ServiceInfo
