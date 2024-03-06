from dataclasses import dataclass
from ttsystemd.systemd.runtime.types import SystemdDBusUnits, DBusUnit, DBusUnitFile
from ttsystemd.systemd.static.types import SystemdJSONUnits, JSONUnit, JSONUnitFile


@dataclass
class UnitInfo:
    dbus_unit: DBusUnit | None
    dbus_unit_file: DBusUnitFile | None
    json_unit: JSONUnit | None
    json_unit_file: JSONUnitFile | None


# We shouldn't get to the else statements, but we'll add them for completeness
def merge(dbus_units: SystemdDBusUnits, json_units: SystemdJSONUnits):
    all_units = {}
    for dbus_unit_name, dbus_unit in dbus_units.units.items():
        all_units[dbus_unit_name] = UnitInfo(
            dbus_unit=dbus_unit,
            dbus_unit_file=None,
            json_unit=None,
            json_unit_file=None,
        )

    for dbus_unit_name, dbus_unit_file in dbus_units.unit_files.items():
        if dbus_unit_name in all_units:
            all_units[dbus_unit_name].dbus_unit_file = dbus_unit_file
        else:
            all_units[dbus_unit_name] = UnitInfo(
                dbus_unit=None,
                dbus_unit_file=dbus_unit_file,
                json_unit=None,
                json_unit_file=None,
            )

    for json_unit_name, json_unit in json_units.units.items():
        if json_unit_name in all_units:
            all_units[json_unit_name].json_unit = json_unit
        else:
            all_units[json_unit_name] = UnitInfo(
                dbus_unit=None,
                dbus_unit_file=None,
                json_unit=json_unit,
                json_unit_file=None,
            )

    for json_unit_name, json_unit_file in json_units.unit_files.items():
        if json_unit_name in all_units:
            all_units[json_unit_name].json_unit_file = json_unit_file
        else:
            all_units[json_unit_name] = UnitInfo(
                dbus_unit=None,
                dbus_unit_file=None,
                json_unit=None,
                json_unit_file=json_unit_file,
            )

    return all_units
