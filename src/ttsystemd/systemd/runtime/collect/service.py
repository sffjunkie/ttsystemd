from dataclasses import fields
from dbus_next.aio import ProxyInterface

from ttsystemd.systemd.runtime.types import Process


class Service:
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

    async def collect(self, interface: ProxyInterface) -> None:
        data = await interface.call_get_processes()  # type: ignore

        self.processes = []
        field_names = [f.name for f in fields(Process)]
        for item in data:
            d = {k: v for k, v in zip(field_names, item)}
            self.processes.append(Process(**d))

        self.allowed_cpus = await interface.call_allowed_cpus()  # type: ignore
        self.allowed_memory_nodes = await interface.call_allowed_memory_nodes()  # type: ignore
