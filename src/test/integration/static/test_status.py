import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.unit_status import status


@pytest.mark.asyncio
async def test_static_status_system_journalflush():
    result = await status(SessionType.SYSTEM, "systemd-journal-flush.service")
    assert len(result) > 0


@pytest.mark.asyncio
async def test_static_status_user_mount():
    result = await status(SessionType.USER_SESSION, "-.mount")
    assert len(result) > 0
