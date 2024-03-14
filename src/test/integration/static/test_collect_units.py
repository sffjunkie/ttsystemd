import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.static.collect import json_collect_units


@pytest.mark.asyncio
async def test_static_units_system():
    result = await json_collect_units(SessionType.SYSTEM)
    assert len(result.units) > 0
    assert "systemd-journal-flush.service" in result.units


@pytest.mark.asyncio
async def test_static_units_user():
    result = await json_collect_units(SessionType.USER_SESSION)
    assert len(result.units) > 0
    assert "dbus.service" in result.units
