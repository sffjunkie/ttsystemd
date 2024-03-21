from dbus_next.constants import BusType
from dbus_next.aio import MessageBus

from ttsystemd.systemd.runtime.connect import dbus_message_bus
from ttsystemd.systemd.runtime.collect.unit import Unit


class UnitCache:
    _bus: MessageBus | None
    _bus_type: BusType
    _cache: dict[str, Unit] = {}

    def __init__(self, bus_type: BusType) -> None:
        self._bus = None
        self._bus_type = bus_type

    async def get(self, object_path: str) -> Unit:
        if object_path in self._cache:
            return self._cache[object_path]

        if self._bus is None:
            self._bus = await dbus_message_bus(self._bus_type)

        unit = Unit()
        await unit.collect(self._bus, object_path)
        self._cache[object_path] = unit
        return unit


class SystemUnitCache(UnitCache):
    def __init__(self):
        super().__init__(BusType.SYSTEM)


class SessionUnitCache(UnitCache):
    def __init__(self):
        super().__init__(BusType.SESSION)
