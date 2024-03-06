from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.systemctl import systemctl_cmd_text


async def properties(
    session_type: SessionType, unit_name: str
) -> dict[str, str] | None:
    params = ["show", "--", unit_name]
    if session_type == SessionType.USER_SESSION:
        params = ["--user", *params]

    result = await systemctl_cmd_text(params)
    if result.returncode == 0:
        return parse_properties(result.text)
    else:
        raise IOError(f"Unbale to get properties for {unit_name}: {result.text}")


def parse_properties(text: str) -> dict[str, str]:
    result = {}
    for line in text.split("\n"):
        if line:
            k, v = line.split("=", maxsplit=1)
            result[k] = v

    if "Environment" in result:
        environment = {}
        for elem in result["Environment"].split(" "):
            k, v = elem.split("=", maxsplit=1)
            environment[k] = v

        result["Environment"] = environment

    if "Features" in result:
        result["Features"] = result["Features"].split(" ")
    return result
