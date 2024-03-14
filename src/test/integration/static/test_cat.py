import os
import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.unit_cat import cat


@pytest.mark.asyncio
async def test_unit_cat_system_boot_mount():
    result = await cat(SessionType.SYSTEM, "boot.mount")
    assert len(result) > 0


@pytest.mark.asyncio
@pytest.mark.xfail("VSCODE_PID" in os.environ, reason="Fails under vscode")
async def test_unit_cat_user_boot_mount():
    result = await cat(SessionType.USER_SESSION, "dbus.service")
    assert len(result) > 0
