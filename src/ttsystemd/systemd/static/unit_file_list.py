from ttsystemd.systemd.static.systemctl import systemctl_cmd_json
from ttsystemd.systemd.static.types import JSONUnitFile

from ttsystemd.systemd.types import SessionType


async def list_unit_files(session_type: SessionType) -> dict[str, JSONUnitFile]:
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
