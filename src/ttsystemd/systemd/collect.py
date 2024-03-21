from dataclasses import dataclass
from typing import Any
import asyncio
from ttsystemd.systemd.runtime.collect.system import DBusSystemCollector
from ttsystemd.systemd.static.collect.system import JSONSystemCollector
from ttsystemd.systemd.merge import merge, UnitInfo
from ttsystemd.systemd.runtime.types import DBusUnitInfo
from ttsystemd.systemd.static.types import JSONUnitInfo

Properties = dict[str, Any]


@dataclass
class SystemdData:
    properties: Properties
    system_units: dict[str, UnitInfo]
    session_units: dict[str, UnitInfo]


async def collect() -> SystemdData:
    runtime_collector = DBusSystemCollector()
    static_collector = JSONSystemCollector()
    await asyncio.gather(
        runtime_collector.collect(),
        static_collector.collect(),
    )

    dbus_system_info = DBusUnitInfo(
        units=runtime_collector.system_units,
        unit_files=runtime_collector.system_unit_files,
    )
    dbus_session_info = DBusUnitInfo(
        units=runtime_collector.session_units,
        unit_files=runtime_collector.session_unit_files,
    )

    json_system_info = JSONUnitInfo(
        units=static_collector.system_units,
        unit_files=static_collector.system_unit_files,
    )
    json_session_info = JSONUnitInfo(
        units=static_collector.session_units,
        unit_files=static_collector.session_unit_files,
    )

    system_merged = merge(dbus_system_info, json_system_info)
    session_merged = merge(dbus_session_info, json_session_info)

    return SystemdData(
        runtime_collector.properties,
        system_merged,
        session_merged,
    )
