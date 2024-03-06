import asyncio
import json

from ttsystemd.systemd.static.types import CommandResult


async def systemctl_cmd_text(cmd: list[str]) -> CommandResult:
    args = ["--no-pager", *cmd]
    process = await asyncio.create_subprocess_exec(
        "systemctl",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.wait()
    if process.returncode == 0:
        out = await process.stdout.read()
        return CommandResult(
            returncode=process.returncode,
            text=out.decode("utf-8"),
        )
    else:
        err = await process.stderr.read()
        return CommandResult(
            returncode=process.returncode,
            text=err.decode("utf-8"),
        )


async def systemctl_cmd_json(cmd: list[str]) -> CommandResult:
    args = ["--no-pager", "-o", "json", *cmd]
    process = await asyncio.create_subprocess_exec(
        "systemctl",
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.wait()
    if process.returncode == 0:
        out = await process.stdout.read()
        text = out.decode("utf-8")
        return CommandResult(
            returncode=process.returncode,
            text=text,
            json=json.loads(text),
        )
    else:
        err = await process.stderr.read()
        return CommandResult(
            returncode=process.returncode,
            text=err.decode("utf-8"),
        )
