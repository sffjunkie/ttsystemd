from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.systemctl import systemctl_cmd_text


async def status(session_type: SessionType, unit_name: str) -> str:
    params = ["status", "--", unit_name]
    if session_type == SessionType.USER_SESSION:
        params = ["--user", *params]

    result = await systemctl_cmd_text(params)
    if result.returncode != 0:
        raise IOError(f"Unbale to get status for {unit_name}: {result.text}")

    return result.text
