import pytest
from ttsystemd.systemd.runtime.collect.system import DBusSystemCollector


@pytest.mark.asyncio
async def test_int_manager_properties():
    collector = DBusSystemCollector()
    await collector.collect()
    assert len(collector.properties) > 0
    assert "architecture" in collector.properties

