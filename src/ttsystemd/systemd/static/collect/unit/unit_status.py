from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.collect.systemctl import systemctl_cmd_text


async def status(session_type: SessionType, unit_name: str) -> str | None:
    params = ["status", "--", unit_name]
    if session_type == SessionType.USER_SESSION:
        params = ["--user", *params]

    result = await systemctl_cmd_text(params)
    if result.returncode != 0:
        msg = f"Unable to get status for {unit_name}"
        if result.text is not None:
            msg += f": {result.text}"
        raise IOError(msg)

    return result.text
