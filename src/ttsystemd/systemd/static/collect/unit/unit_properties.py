from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.collect.systemctl import systemctl_cmd_text


async def properties(
    session_type: SessionType, unit_name: str
) -> dict[str, str] | None:
    params = ["show", "--", unit_name]
    if session_type == SessionType.USER_SESSION:
        params = ["--user", *params]

    result = await systemctl_cmd_text(params)
    if result.returncode == 0 and result.text is not None:
        return parse_properties(result.text)
    else:
        msg = f"Unable to get properties for {unit_name}"
        if result.text is not None:
            msg += f": {result.text}"
        raise IOError(msg)


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

        result["Environment"] = environment  # type: ignore

    if "Features" in result:
        result["Features"] = result["Features"].split(" ")  # type: ignore
    return result
