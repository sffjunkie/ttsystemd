import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.unit_properties import properties


@pytest.mark.asyncio
async def test_static_properties_system_journalflush():
    result = await properties(SessionType.SYSTEM, "systemd-journal-flush.service")
    assert len(result) > 0
    assert result["Type"] == "oneshot"


@pytest.mark.asyncio
async def test_static_properties_user_mount():
    result = await properties(SessionType.USER_SESSION, "home.mount")
    assert len(result) > 0
    assert result["Where"] == "/home"
