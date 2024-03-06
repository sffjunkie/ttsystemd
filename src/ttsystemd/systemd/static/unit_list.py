from dataclasses import fields

from ttsystemd.systemd.types import SessionType

from ttsystemd.systemd.static.systemctl import systemctl_cmd_json
from ttsystemd.systemd.static.types import JSONUnit, UnitType


async def list_units(session_type: SessionType) -> dict[str, JSONUnit]:
    if session_type == SessionType.USER_SESSION:
        params = ["--user", "list-units"]
    else:
        params = ["list-units"]

    result = await systemctl_cmd_json(params)
    data = None
    if result.returncode == 0:
        data = {}
        field_names = [f.name for f in fields(JSONUnit)[1:]]
        for item in result.json:
            u = {k: v for k, v in zip(field_names, item.values())}
            u["unit_type"] = UnitType(u["unit_name"].split(".")[-1])
            data[u["unit_name"]] = JSONUnit(**u)
    return data
