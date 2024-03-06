from pathlib import Path
from dataclasses import fields

from dbus_next.aio import ProxyInterface

from ttsystemd.systemd.runtime.types import DBusUnitFile, UnitType


async def dbus_manager_list_unit_files(interface: ProxyInterface):
    data = await interface.call_list_unit_files()
    unit_files = {}
    for item in data:
        unit_file_path = Path(item[0])
        unit_name = unit_file_path.name
        unit_files[unit_name] = DBusUnitFile(
            unit_name=unit_name,
            unit_type=unit_file_path.suffix.lstrip("."),
            unit_path=item[0],
            enable=item[1],
        )

    return unit_files


# async def dbus_manager_list_unit_files(interface: ProxyInterface):
#     data = await interface.call_list_unit_files()
#     unit_files = {}
#     field_names = [f.name for f in fields(DBusUnitFile)[1:]]  # skip unit_type
#     for item in data:
#         d = {k: v for k, v in zip(field_names, item)}
#         d["unit_type"] = UnitType(d["unit_name"].split(".")[-1])
#         unit_files[d["unit_name"]] = DBusUnitFile(**d)

#     return unit_files
