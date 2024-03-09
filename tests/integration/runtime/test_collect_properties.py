import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.runtime.manager import dbus_manager_collect_properties


@pytest.mark.asyncio
async def test_int_units_system():
    result = await dbus_manager_collect_properties(SessionType.SYSTEM)
    assert len(result.properties) > 0
    assert "architecture" in result.properties


@pytest.mark.asyncio
async def test_int_units_user_session():
    result = await dbus_manager_collect_properties(SessionType.USER_SESSION)
    assert len(result.properties) > 0
    assert "version" in result.properties
