import asyncio
from dataclasses import fields
from pathlib import Path

from dbus_next.aio import MessageBus, ProxyInterface
from dbus_next.constants import BusType

from ttsystemd.systemd.runtime.connect import dbus_message_bus
from ttsystemd.systemd.runtime.interface import (
    systemd_get_object_interface,
)
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES
from ttsystemd.systemd.runtime.types import (
    DBusUnit,
    DBusUnitFile,
    Properties,
)
from ttsystemd.systemd.types import UnitType


class DBusSystemCollector:
    properties: Properties

    _system_bus: MessageBus | None
    _session_bus: MessageBus | None

    system_units: dict[str, DBusUnit]
    system_unit_files: dict[str, DBusUnitFile]

    session_units: dict[str, DBusUnit]
    session_unit_files: dict[str, DBusUnitFile]

    def __init__(self):
        self.properties = {}

        self._system_bus = None
        self.system_units = {}
        self.system_unit_files = {}

        self._session_bus = None
        self.session_units = {}
        self.session_unit_files = {}

    async def collect(self) -> None:
        self._system_bus = await dbus_message_bus(BusType.SYSTEM)
        self.system_interface = await self._get_manager_interface(self._system_bus)

        self._session_bus = await dbus_message_bus(BusType.SESSION)
        self.session_interface = await self._get_manager_interface(self._session_bus)

        (
            self.properties,
            self.system_units,
            self.system_unit_files,
            self.session_units,
            self.session_unit_files,
        ) = await asyncio.gather(
            self.get_properties(),
            self.get_unit_list(self.system_interface),
            self.get_unit_file_list(self.system_interface),
            self.get_unit_list(self.session_interface),
            self.get_unit_file_list(self.session_interface),
        )

    async def get_properties(self) -> Properties:
        if self._system_bus is None:
            raise ValueError(
                "Not connected to message bus - You need to run `collect` first"
            )

        properties_interface = await self._get_properties_interface(self._system_bus)
        all_props = await properties_interface.call_get_all(  # type: ignore
            "org.freedesktop.systemd1.Manager"
        )
        data: Properties = {}
        for item in MANAGER_PROPERTIES.keys():
            value = all_props[item].value
            data[item] = value

        environment = {}
        for elem in data["Environment"]:
            k, v = elem.split("=", maxsplit=1)
            environment[k] = v

        data["Environment"] = environment
        data["Features"] = data["Features"].split(" ")
        return data

    async def get_unit_list(self, interface: ProxyInterface) -> dict[str, DBusUnit]:
        data = await interface.call_list_units()  # type: ignore
        units = {}
        field_names = [f.name for f in fields(DBusUnit)[1:]]  # skip unit_type
        for item in data:
            u = {k: v for k, v in zip(field_names, item)}
            u["unit_type"] = UnitType(u["unit_name"].split(".")[-1])
            units[u["unit_name"]] = DBusUnit(**u)

        return units

    async def get_unit_file_list(
        self, interface: ProxyInterface
    ) -> dict[str, DBusUnitFile]:
        data = await interface.call_list_unit_files()  # type: ignore
        unit_files = {}
        for item in data:
            unit_file_path = Path(item[0])
            unit_name = unit_file_path.name
            unit_files[unit_name] = DBusUnitFile(
                unit_name=unit_name,
                unit_type=UnitType(unit_file_path.suffix.lstrip(".")),
                unit_path=item[0],
                enable=item[1],
            )

        return unit_files

    async def _get_manager_interface(self, bus: MessageBus) -> ProxyInterface:
        interface = await systemd_get_object_interface(
            bus,
            "/org/freedesktop/systemd1",
            "systemd1.Manager",
            "systemd1.Manager",
        )
        return interface

    async def _get_properties_interface(self, bus: MessageBus) -> ProxyInterface:
        interface = await systemd_get_object_interface(
            bus,
            "/org/freedesktop/systemd1",
            "systemd1.Manager",
            "DBus.Properties",
        )
        return interface
