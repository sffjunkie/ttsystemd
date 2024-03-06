from dataclasses import fields

from dbus_next import InterfaceNotFoundError
from dbus_next.aio import MessageBus, ProxyInterface

from ttsystemd.systemd.runtime.connect import dbus_get_unit_interface
from ttsystemd.systemd.runtime.properties import INTERFACE_PROPERTIES
from ttsystemd.systemd.runtime.types import (
    DBusUnit,
    UnitType,
    DBusUnitInterfaceProperties,
    SystemdDBusProperties,
)


async def dbus_manager_list_units(interface: ProxyInterface) -> dict[str, DBusUnit]:
    data = await interface.call_list_units()
    units = {}
    field_names = [f.name for f in fields(DBusUnit)[1:]]  # skip unit_type
    for item in data:
        u = {k: v for k, v in zip(field_names, item)}
        u["unit_type"] = UnitType(u["unit_name"].split(".")[-1])
        units[u["unit_name"]] = DBusUnit(**u)

    return units


async def dbus_unit_collect(
    bus: MessageBus,
    unit_path: str,
) -> DBusUnitInterfaceProperties:
    return DBusUnitInterfaceProperties(
        device=await dbus_unit_collect_interface(bus, unit_path, "device"),
        mount=await dbus_unit_collect_interface(bus, unit_path, "mount"),
        path=await dbus_unit_collect_interface(bus, unit_path, "path"),
        scope=await dbus_unit_collect_interface(bus, unit_path, "scope"),
        service=await dbus_unit_collect_interface(bus, unit_path, "service"),
        slice=await dbus_unit_collect_interface(bus, unit_path, "slice"),
        socket=await dbus_unit_collect_interface(bus, unit_path, "socket"),
        swap=await dbus_unit_collect_interface(bus, unit_path, "swap"),
        timer=await dbus_unit_collect_interface(bus, unit_path, "timer"),
        unit=await dbus_unit_collect_interface(bus, unit_path, "unit"),
    )


async def dbus_unit_collect_interface(
    bus: MessageBus,
    unit_path: str,
    interface_type: str,
) -> SystemdDBusProperties:
    try:
        interface = await dbus_get_unit_interface(
            bus, unit_path, f"org.freedesktop.systemd1.{interface_type.capitalize()}"
        )
        data = {}
        properties = INTERFACE_PROPERTIES[interface_type.lower()]
        for item in properties.keys():
            value = await getattr(interface, f"get_{item}")()
            data[item] = value

        return data
    except InterfaceNotFoundError:
        return None
