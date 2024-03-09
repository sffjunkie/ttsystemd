from dbus_next.aio import ProxyInterface
from dbus_next.constants import BusType

from ttsystemd.systemd.runtime.connect import (
    dbus_get_manager_interface,
    dbus_message_bus,
)
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES
from ttsystemd.systemd.runtime.types import (
    SystemdDBusProperties,
    SystemdDBusUnits,
)
from ttsystemd.systemd.runtime.unit import dbus_manager_list_units
from ttsystemd.systemd.runtime.unit_file import dbus_manager_list_unit_files
from ttsystemd.systemd.types import SessionType


async def dbus_manager_collect_properties(
    session_type: SessionType,
) -> SystemdDBusProperties:
    bus_type = BusType.SYSTEM if session_type == SessionType.SYSTEM else BusType.SESSION

    bus = await dbus_message_bus(bus_type)
    interface = await dbus_get_manager_interface(bus)
    properties = await _collect_properties(interface)

    return SystemdDBusProperties(
        bus_type=bus_type,
        properties=properties,
    )


async def dbus_manager_collect_units(
    session_type: SessionType,
) -> SystemdDBusUnits:
    bus_type = BusType.SYSTEM if session_type == SessionType.SYSTEM else BusType.SESSION

    bus = await dbus_message_bus(bus_type)
    interface = await dbus_get_manager_interface(bus)
    units = await dbus_manager_list_units(interface)
    unit_files = await dbus_manager_list_unit_files(interface)

    return SystemdDBusUnits(
        bus_type=bus_type,
        units=units,
        unit_files=unit_files,
    )


async def _collect_properties(
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
