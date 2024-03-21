from textual.app import ComposeResult
from textual import on
from textual.reactive import reactive, Reactive
from textual.containers import Horizontal
from textual.widget import Widget
from textual.widgets import Button, DataTable

from ttsystemd.ui.table.units_table import UnitsTable
from ttsystemd.systemd.merge import UnitData


class UnitsOverview(Widget):
    systemd_units: Reactive[UnitData | None] = reactive(None)
    unit_type: Reactive[str] = reactive("*")

    def __init__(self) -> None:
        super().__init__()
        self.units_table = UnitsTable()
        self.details_button = Button(
            "Details...",
            id="show_details",
        )
        self.selected_unit: str | None = None

    def compose(self) -> ComposeResult:
        yield self.units_table
        with Horizontal():
            yield self.details_button

    def watch_systemd_units(self, systemd_units: UnitData) -> None:
        if systemd_units is not None:
            self.units_table.fill(systemd_units, self.unit_type)

    def watch_unit_type(self, unit_type: str) -> None:
        if self.systemd_units is not None:
            self.units_table.fill(self.systemd_units, unit_type)

    @on(DataTable.RowSelected)
    def store_selected_row_key(self, event: DataTable.RowSelected) -> None:
        self.selected_unit = event.row_key.value
