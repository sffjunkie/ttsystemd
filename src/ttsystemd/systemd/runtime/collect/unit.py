from dbus_next import InterfaceNotFoundError
from dbus_next.aio import MessageBus

from ttsystemd.systemd.runtime.interface import dbus_get_object_interface
from ttsystemd.systemd.runtime.properties import INTERFACE_PROPERTIES
from ttsystemd.systemd.runtime.types import Properties


class Unit:
    device: Properties | None
    mount: Properties | None
    path: Properties | None
    scope: Properties | None
    service: Properties | None
    slice: Properties | None
    socket: Properties | None
    swap: Properties | None
    timer: Properties | None
    unit: Properties | None

    async def collect(
        self,
        bus: MessageBus,
        object_path: str,
    ):
        self.device = await self._collect_interface(bus, object_path, "device")
        self.mount = await self._collect_interface(bus, object_path, "mount")
        self.path = await self._collect_interface(bus, object_path, "path")
        self.scope = await self._collect_interface(bus, object_path, "scope")
        self.service = await self._collect_interface(bus, object_path, "service")
        self.slice = await self._collect_interface(bus, object_path, "slice")
        self.socket = await self._collect_interface(bus, object_path, "socket")
        self.swap = await self._collect_interface(bus, object_path, "swap")
        self.timer = await self._collect_interface(bus, object_path, "timer")
        self.unit = await self._collect_interface(bus, object_path, "unit")

    async def _collect_interface(
        self,
        bus: MessageBus,
        unit_path: str,
        interface_type: str,
    ) -> Properties:
        try:
            interface = await dbus_get_object_interface(
                bus,
                unit_path,
                f"org.freedesktop.systemd1.{interface_type.capitalize()}",
            )
            data = {}
            properties = INTERFACE_PROPERTIES[interface_type.lower()]
            for item in properties.keys():
                value = await getattr(interface, f"get_{item}")()
                data[item] = value

            return data
        except InterfaceNotFoundError:
            return None
