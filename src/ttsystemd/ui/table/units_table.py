from collections.abc import Iterable
from textual.widgets import DataTable
from textual.widgets.data_table import ColumnKey
from textual.reactive import reactive, Reactive
from itertools import islice
from ttsystemd.systemd.merge import UnitInfo, UnitData


class UnitsTable(DataTable):
    systemd_units: Reactive[UnitData | None] = reactive(None)
    unit_type: Reactive[str] = reactive("*")

    def __init__(self) -> None:
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

        self.sort_key = ColumnKey("name")
        self.sort_reverse = False

    def on_data_table_header_selected(
        self, selection: DataTable.HeaderSelected
    ) -> None:
        if selection.column_index == 0:
            return

        if selection.column_key == self.sort_key:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_key = selection.column_key
            self.sort_reverse = False
        self.sort(self.sort_key, reverse=self.sort_reverse)

    def fill(self, systemd_units: UnitData, unit_type: str) -> None:
        units: Iterable[UnitInfo]
        if systemd_units is not None:
            if unit_type != "*":

                def _filter(unit: UnitInfo):
                    return unit.type == unit_type

                units = filter(_filter, systemd_units.values())
            else:
                units = systemd_units.values()

            units = sorted(units, key=lambda unit: unit.name)

            self.clear()
            for unit in units:
                item = None
                if unit.dbus_unit is not None:
                    item = (
                        status_symbol(unit.dbus_unit.active_state),
                        self._format_unit_name(unit.name),
                        unit.dbus_unit.unit_type,
                        unit.dbus_unit.active_state,
                        unit.dbus_unit.load_state,
                        unit.dbus_unit.sub_state,
                    )
                elif unit.json_unit is not None:
                    item = (
                        status_symbol(unit.json_unit.active),
                        self._format_unit_name(unit.name),
                        unit.json_unit.unit_type,
                        unit.json_unit.active,
                        unit.json_unit.load,
                        unit.json_unit.sub,
                    )

                if item is not None:
                    self.add_row(*item, height=None, key=unit.name)

    def _format_unit_name(self, unit_name: str) -> str:
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
