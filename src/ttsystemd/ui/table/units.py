from textual.widgets import DataTable
from textual.reactive import reactive
from ttsystemd.systemd.runtime.types import SystemdDBusUnits
from itertools import islice


class SystemdUnitsTable(DataTable):
    systemd_units = reactive(None)
    unit_type = reactive("*")

    def __init__(self):
        super().__init__(
            cursor_type="row",
            zebra_stripes=True,
        )
        self.add_columns("Name", "Type", "Active State", "Load State", "Sub State")

    def watch_systemd_units(self, systemd_units: SystemdDBusUnits):
        if systemd_units is not None:
            self.fill(systemd_units, self.unit_type)

    def watch_unit_type(self, unit_type: str):
        if self.systemd_units is not None:
            self.fill(self.systemd_units, unit_type)

    def fill(self, systemd_units: SystemdDBusUnits, unit_type: str):
        if systemd_units is not None:
            if unit_type != "*":

                def _filter(unit):
                    return unit.unit_type == unit_type

                units = filter(_filter, systemd_units.units.values())
            else:
                units = systemd_units.units.values()

            units = sorted(units, key=lambda unit: unit.unit_name)

            self.clear()
            items = [
                (
                    self._format_unit_name(unit.unit_name),
                    unit.unit_type,
                    unit.active_state,
                    unit.load_state,
                    unit.sub_state,
                )
                for unit in units
            ]
            for item in items:
                self.add_row(*item, height=None)

    def _format_unit_name(self, unit_name: str):
        name, _type = unit_name.rsplit(".", maxsplit=1)

        if len(name) < 60:
            return name

        chunks = [batch for batch in self.chunked(name, 60)]
        return "\n".join(chunks)

    def chunked(self, iterable, n):
        it = iter(iterable)
        while batch := tuple(islice(it, n)):
            yield "".join(batch)
