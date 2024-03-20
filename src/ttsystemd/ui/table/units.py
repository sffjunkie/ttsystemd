from textual.widgets import DataTable
from textual.reactive import reactive
from ttsystemd.systemd.runtime.types import DBusUnitInfo
from itertools import islice


class SystemdUnitsTable(DataTable):
    systemd_units = reactive(None)
    unit_type = reactive("*")

    def __init__(self):
        super().__init__(
            cursor_type="row",
            zebra_stripes=True,
        )
        self.add_column(" ", key="status")
        self.add_column("Name", key="name")
        self.add_column("Type", key="type")
        self.add_column("Active State", key="active_state")
        self.add_column("Load State", key="load_state")
        self.add_column("Sub State", key="sub_state")

        self.sort_key = "name"
        self.sort_reverse = False

    def watch_systemd_units(self, systemd_units: DBusUnitInfo):
        if systemd_units is not None:
            self.fill(systemd_units, self.unit_type)

    def watch_unit_type(self, unit_type: str):
        if self.systemd_units is not None:
            self.fill(self.systemd_units, unit_type)

    def on_data_table_header_selected(self, selection: DataTable.HeaderSelected):
        if selection.column_index == 0:
            return

        if selection.column_key.value == self.sort_key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key = selection.column_key.value
            self.sort_reverse = False
        self.sort(self.sort_key, reverse=self.sort_reverse)

    def fill(self, systemd_units: DBusUnitInfo, unit_type: str):
        if systemd_units is not None:
            if unit_type != "*":

                def _filter(unit):
                    return unit.unit_type == unit_type

                units = filter(_filter, systemd_units.values())
            else:
                units = systemd_units.values()

            units = sorted(units, key=lambda unit: unit.unit_name)

            self.clear()
            items = [
                (
                    status_symbol(unit.active_state),
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


def status_symbol(active_state: str):
    if active_state == "active":
        return "[green]●[/green]"
    if active_state == "deactivating":
        return "[white]●[/white]"
    elif active_state == "inactive" or active_state == "maintenance":
        return "○"
    elif active_state == "failed" or active_state == "error":
        return "[red]×[/red]"
    elif active_state == "reloading":
        return "[green]↻[/green]"
    else:
        return ""
