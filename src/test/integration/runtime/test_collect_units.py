import pytest
from ttsystemd.systemd.runtime.collect.system import DBusSystemCollector


@pytest.mark.asyncio
async def test_int_units_system():
    collector = DBusSystemCollector()
    await collector.collect()
    assert len(collector.system_units) > 0
    assert "systemd-oomd.service" in collector.system_units


@pytest.mark.asyncio
async def test_int_units_user_session():
    collector = DBusSystemCollector()
    await collector.collect()
    assert len(collector.session_units) > 0
    assert "dbus.service" in collector.session_units

