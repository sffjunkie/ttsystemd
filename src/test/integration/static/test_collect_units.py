import pytest
from ttsystemd.systemd.static.collect.system import JSONSystemCollector


@pytest.mark.asyncio
async def test_static_units_system():
    collector = JSONSystemCollector()
    await collector.collect()
    assert len(collector.system_units) > 0
    assert "systemd-journal-flush.service" in collector.system_units


@pytest.mark.asyncio
async def test_static_units_user():
    collector = JSONSystemCollector()
    await collector.collect()
    assert len(collector.session_units) > 0
    assert "dbus.service" in collector.session_units
