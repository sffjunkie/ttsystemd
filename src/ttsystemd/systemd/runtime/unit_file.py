from pathlib import Path

from dbus_next.aio import ProxyInterface

from ttsystemd.systemd.runtime.types import DBusUnitFile


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
