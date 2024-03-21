import dbus_next.introspection
from dbus_next.aio import MessageBus, ProxyObject, ProxyInterface
from dbus_next.constants import BusType


async def dbus_message_bus(bus_type: BusType = BusType.SYSTEM) -> MessageBus:
    bus = MessageBus(bus_type=bus_type)
    await bus.connect()
    return bus


# region Introspection
async def dbus_introspect(
    bus: MessageBus, object_path: str
) -> dbus_next.introspection.Node:
    introspection = await bus.introspect("org.freedesktop.systemd1", object_path)
    return introspection


async def dbus_introspection_get_proxy(
    bus: MessageBus, introspection: dbus_next.introspection.Node, object_path: str
) -> ProxyObject:
    systemd_proxy = bus.get_proxy_object(
        "org.freedesktop.systemd1",
        object_path,
        introspection,
    )
    return systemd_proxy


def dbus_introspection_get_interface(
    systemd_proxy: ProxyObject, interface_name: str
) -> ProxyInterface:
    return systemd_proxy.get_interface(interface_name)


# endregion
