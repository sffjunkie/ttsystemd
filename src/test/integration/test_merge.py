import pytest
from ttsystemd.systemd.merge import merge
from ttsystemd.systemd.runtime.collect.system import DBusSystemCollector
from ttsystemd.systemd.runtime.types import DBusUnitInfo
from ttsystemd.systemd.static.collect.system import JSONSystemCollector
from ttsystemd.systemd.static.types import JSONUnitInfo


@pytest.mark.asyncio
async def test_int_merge_system():
    dbus_collector = DBusSystemCollector()
    await dbus_collector.collect()

    dbus_unit_info = DBusUnitInfo(
        units=dbus_collector.system_units,
        unit_files=dbus_collector.system_unit_files,
    )

    json_collector = JSONSystemCollector()
    await json_collector.collect()

    json_unit_info = JSONUnitInfo(
        units=json_collector.system_units,
        unit_files=json_collector.system_unit_files
    )

    merged = merge(dbus_unit_info, json_unit_info)
    assert len(merged) > 0
    assert "systemd-journald.service" in merged
