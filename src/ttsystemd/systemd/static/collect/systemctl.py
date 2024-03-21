from asyncio import create_subprocess_exec
from asyncio.subprocess import Process, PIPE
import json

from ttsystemd.systemd.static.types import CommandResult


async def systemctl_cmd_text(cmd: list[str]) -> CommandResult:
    args = ["--no-pager", *cmd]
    process = await create_subprocess_exec(
        "systemctl",
        *args,
        stdout=PIPE,
        stderr=PIPE,
    )
    await process.wait()
    if process.returncode == 0 and process.stdout is not None:
        out = await process.stdout.read()
        return CommandResult(
            returncode=process.returncode,
            text=out.decode("utf-8"),
            json=None,
        )
    else:
        return CommandResult(
            returncode=process.returncode,
            text=await _get_err(process),
            json=None,
        )


async def systemctl_cmd_json(cmd: list[str]) -> CommandResult:
    args = ["--no-pager", "-o", "json", *cmd]
    process = await create_subprocess_exec(
        "systemctl",
        *args,
        stdout=PIPE,
        stderr=PIPE,
    )
    await process.wait()
    if process.returncode == 0 and process.stdout is not None:
        out = await process.stdout.read()
        text = out.decode("utf-8")
        return CommandResult(
            returncode=process.returncode,
            text=None,
            json=json.loads(text),
        )
    else:
        return CommandResult(
            returncode=process.returncode,
            text=await _get_err(process),
            json=None,
        )


async def _get_err(process: Process) -> str:
    if process.stderr is not None:
        err = await process.stderr.read()
        return err.decode("utf-8")
    else:
        return ""
