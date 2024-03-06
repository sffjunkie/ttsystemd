from dbus_next.constants import BusType

from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.runtime.connect import (
    dbus_get_manager_interface,
    dbus_message_bus,
)
from ttsystemd.systemd.runtime.manager import dbus_manager_collect_properties
from ttsystemd.systemd.runtime.types import (
    SystemdDBusProperties,
    SystemdDBusUnits,
)
from ttsystemd.systemd.runtime.unit import dbus_manager_list_units
from ttsystemd.systemd.runtime.unit_file import dbus_manager_list_unit_files


async def dbus_collect_properties(
    session_type: SessionType,
) -> SystemdDBusProperties:
    bus_type = BusType.SYSTEM if session_type == SessionType.SYSTEM else BusType.SESSION

    bus = await dbus_message_bus(bus_type)
    interface = await dbus_get_manager_interface(bus)
    properties = await dbus_manager_collect_properties(interface)

    return SystemdDBusProperties(
        bus_type=bus_type,
        properties=properties,
    )


async def dbus_collect_units(
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


async def dbus_collect_unit_properties(
    session_type: SessionType, unit_name: str
) -> SystemdDBusUnits:
    bus_type = BusType.SYSTEM if session_type == SessionType.SYSTEM else BusType.SESSION
