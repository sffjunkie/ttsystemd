import pytest
from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.runtime.manager import dbus_manager_collect_units
from ttsystemd.systemd.static.collect import json_collect_units
from ttsystemd.systemd.merge import merge


@pytest.mark.asyncio
async def test_int_merge_system():
    dbus_units = await dbus_manager_collect_units(SessionType.SYSTEM)
    json_units = await json_collect_units(SessionType.SYSTEM)
    merged = merge(dbus_units, json_units)
    assert len(merged) > 0
    assert "systemd-journald.service" in merged
