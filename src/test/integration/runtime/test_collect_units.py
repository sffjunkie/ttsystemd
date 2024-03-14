import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.runtime.manager import dbus_manager_collect_units


@pytest.mark.asyncio
async def test_int_units_system():
    result = await dbus_manager_collect_units(SessionType.SYSTEM)
    assert len(result.units) > 0
    assert "systemd-oomd.service" in result.units


@pytest.mark.asyncio
async def test_int_units_user_session():
    result = await dbus_manager_collect_units(SessionType.USER_SESSION)
    assert len(result.units) > 0
    assert "dbus.service" in result.units
