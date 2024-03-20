import asyncio
from dataclasses import fields

from ttsystemd.systemd.static.collect.systemctl import systemctl_cmd_json
from ttsystemd.systemd.static.types import JSONUnit, JSONUnitFile, UnitType
from ttsystemd.systemd.types import SessionType


class DBusSystemCollector:
    system_units: dict[str, JSONUnit]
    system_unit_files: dict[str, JSONUnitFile]

    session_units: dict[str, JSONUnit]
    session_unit_files: dict[str, JSONUnitFile]

    def __init__(self):
        self.system_units = {}
        self.system_unit_files = {}
        self.session_units = {}
        self.session_unit_files = {}

    async def collect(self) -> None:
        (
            self.system_unit_files,
            self.system_units,
            self.session_unit_files,
            self.session_units,
        ) = await asyncio.gather(
            self.get_unit_file_list(SessionType.SYSTEM),
            self.get_unit_list(SessionType.SYSTEM),
            self.get_unit_file_list(SessionType.USER_SESSION),
            self.get_unit_list(SessionType.USER_SESSION),
        )

    async def get_unit_list(session_type: SessionType) -> dict[str, JSONUnit]:
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

    async def get_unit_file_list(session_type: SessionType) -> dict[str, JSONUnitFile]:
        if session_type == SessionType.USER_SESSION:
            params = ["--user", "list-unit-files"]
        else:
            params = ["list-unit-files"]

        data = await systemctl_cmd_json(params)

        result = {}
        for item in data.json:
            uf = JSONUnitFile(
                unit_file=item["unit_file"],
                state=item["state"],
                preset=item["state"],
            )
            result[item["unit_file"]] = uf
        return result
