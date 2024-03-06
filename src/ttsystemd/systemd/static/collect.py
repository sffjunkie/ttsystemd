from ttsystemd.systemd.types import SessionType

from .types import SystemdJSONUnits
from .unit_list import list_units
from .unit_file_list import list_unit_files


async def json_collect_units(session_type: SessionType) -> SystemdJSONUnits:
    unit_files = await list_unit_files(session_type)
    units = await list_units(session_type)

    info = SystemdJSONUnits(
        unit_files=unit_files,
        units=units,
    )
    return info
