import dbus_next.introspection
from dbus_next.aio import MessageBus, ProxyInterface, ProxyObject
from dbus_next.constants import BusType

from ttsystemd.systemd.cache import cache_home
from ttsystemd.systemd.runtime.object import split_object_path
from ttsystemd.systemd.cache import dbus_load_interface_definition


async def dbus_message_bus(bus_type: BusType = BusType.SYSTEM) -> MessageBus:
    bus = MessageBus(bus_type=bus_type)
    await bus.connect()
    return bus


# region Introspection
async def _dbus_introspect(
    bus: MessageBus, object_path: str
) -> dbus_next.introspection.Node:
    introspection = await bus.introspect("org.freedesktop.systemd1", object_path)
    return introspection


async def _dbus_introspection_get_proxy(
    bus: MessageBus, introspection: dbus_next.introspection.Node, object_path: str
) -> ProxyObject:
    systemd_proxy = bus.get_proxy_object(
        "org.freedesktop.systemd1",
        object_path,
        introspection,
    )
    return systemd_proxy


def _dbus_introspection_get_interface(
    systemd_proxy: ProxyObject, interface_name: str
) -> dbus_next.introspection.Interface:
    return systemd_proxy.get_interface(interface_name)


async def _dbus_get_interface(
    bus: MessageBus,
    object_path: str,
    interface_name: str,
):
    introspection = await _dbus_introspect(bus, object_path)
    proxy = await _dbus_introspection_get_proxy(bus, introspection, object_path)
    interface = _dbus_introspection_get_interface(proxy, interface_name)
    return interface


async def _dbus_get_interface_definition(
    bus: MessageBus,
    object_path: str,
):
    introspectable = await _dbus_get_interface(
        bus, object_path, "org.freedesktop.DBus.Introspectable"
    )
    return await introspectable.call_introspect()


# endregion


# region Interfaces
async def dbus_get_manager_interface(
    bus: MessageBus,
) -> ProxyInterface:
    interface_name = "org.freedesktop.systemd1.Manager"
    try:
        interface_definition = dbus_load_interface_definition(interface_name + ".xml")
    except IOError:
        interface_definition = await _dbus_get_interface_definition(
            bus, "/org/freedesktop/systemd1"
        )

    systemd_proxy = bus.get_proxy_object(
        "org.freedesktop.systemd1",
        "/org/freedesktop/systemd1",
        interface_definition,
    )
    interface = systemd_proxy.get_interface(interface_name)
    return interface


async def dbus_get_unit_interface(
    bus: MessageBus, object_path: str, interface_name: str
):
    try:
        interface_definition = dbus_load_interface_definition(interface_name + ".xml")
    except IOError:
        interface_definition = await _dbus_get_interface_definition(bus, object_path)

    systemd_proxy = bus.get_proxy_object(
        "org.freedesktop.systemd1",
        object_path,
        interface_definition,
    )
    interface = systemd_proxy.get_interface(interface_name)
    return interface


# endregion
