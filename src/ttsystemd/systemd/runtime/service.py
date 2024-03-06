from dataclasses import fields
from dbus_next.aio import ProxyInterface

from ttsystemd.runtime.types import Service, Process


def dbus_service(interface: ProxyInterface, dbus_path: str) -> Service:
    data = await interface.call_get_processes()
    processes = []
    field_names = [f.name for f in fields(Process)]
    for item in data:
        d = {k: v for k, v in zip(field_names, item)}
        processes.append(Process(**d))

    allowed_cpus = await interface.call_allowed_cpus()
    allowed_memory_nodes = await interface.call_allowed_memory_nodes()

    return Service(
        processes=processes,
        allowed_cpus=allowed_cpus,
        allowed_memory_nodes=allowed_memory_nodes,
    )
