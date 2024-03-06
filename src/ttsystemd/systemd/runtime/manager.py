from dbus_next.aio.proxy_object import ProxyInterface

from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES
from ttsystemd.systemd.runtime.types import SystemdDBusProperties


async def dbus_manager_collect_properties(
    interface: ProxyInterface,
) -> SystemdDBusProperties:
    data = {}
    for item in MANAGER_PROPERTIES.keys():
        value = await getattr(interface, f"get_{item}")()
        data[item] = value

    environment = {}
    for elem in data["environment"]:
        k, v = elem.split("=", maxsplit=1)
        environment[k] = v

    data["environment"] = environment
    data["features"] = data["features"].split(" ")
    return data
