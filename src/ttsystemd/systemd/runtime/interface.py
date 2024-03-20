from dbus_next.aio import MessageBus

from ttsystemd.systemd.runtime.connect import (
    dbus_introspect,
    dbus_introspection_get_proxy,
    dbus_introspection_get_interface,
)
from ttsystemd.systemd.runtime.cache.interface_definition import (
    dbus_load_interface_definition,
)

# region Interfaces


async def dbus_get_interface(
    bus: MessageBus,
    object_path: str,
    interface_name: str,
):
    introspection = await dbus_introspect(bus, object_path)
    proxy = await dbus_introspection_get_proxy(bus, introspection, object_path)
    interface = dbus_introspection_get_interface(proxy, interface_name)
    return interface


async def dbus_object_introspect(
    bus: MessageBus,
    object_path: str,
):
    introspectable = await dbus_get_interface(
        bus, object_path, "org.freedesktop.DBus.Introspectable"
    )
    return await introspectable.call_introspect()


async def dbus_get_object_interface(
    bus: MessageBus, bus_name: str, object_path: str, interface_def: str, interface_name: str
):
    try:
        interface_definition = dbus_load_interface_definition(interface_def + ".xml")
    except IOError:
        interface_definition = await dbus_object_introspect(bus, object_path)

    systemd_proxy = bus.get_proxy_object(
        bus_name,
        object_path,
        interface_definition,
    )
    interface = systemd_proxy.get_interface(interface_name)
    return interface


async def systemd_get_object_interface(
    bus: MessageBus,
    object_path: str,
    interface_def: str,
    interface_name: str,
):
    def_full_name = f"org.freedesktop.{interface_def}"
    interface_full_name=f"org.freedesktop.{interface_name}"
    return await dbus_get_object_interface(
        bus,
        "org.freedesktop.systemd1",
        object_path,
        def_full_name,
        interface_full_name,
    )


# endregion
