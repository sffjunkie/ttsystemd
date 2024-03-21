from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.types import UnitBackingFile
from ttsystemd.systemd.static.collect.systemctl import systemctl_cmd_text


async def cat(
    session_type: SessionType, unit_name: str
) -> list[UnitBackingFile] | None:
    params = ["cat", "--", unit_name]
    if session_type == SessionType.USER_SESSION:
        params = ["--user", *params]

    result = await systemctl_cmd_text(params)

    # Fails in vscode
    if result.returncode != 0:
        raise IOError(f"Unable to get backing files for {unit_name}: {result.text}")

    if result.text is not None:
        return parse_cat(result.text)
    else:
        return None


def parse_cat(text: str) -> list[UnitBackingFile]:
    backing_file = None
    filename = ""
    contents: list[str] = []
    backing_files = []
    for line in text.split("\n"):
        if line.startswith("#"):
            if backing_file is not None:
                backing_file["filename"] = filename
                backing_file["contents"] = "\n".join(contents)
                backing_files.append(backing_file)

            filename = line[1:].lstrip(" ")
            contents = []
            backing_file = UnitBackingFile()
        else:
            contents.append(line)

    if backing_file is not None:
        backing_files.append(backing_file)
    return backing_files
