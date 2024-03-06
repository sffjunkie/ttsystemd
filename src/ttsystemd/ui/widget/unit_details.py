from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label
from textual.reactive import reactive

from ttsystemd.systemd.runtime.types import DBusUnit
from ttsystemd.ui.table.unit_properties import UnitPropertiesTable


class UnitDetails(Widget):
    unit = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        self.unit_properties_table = UnitPropertiesTable()

    def compose(self) -> ComposeResult:
        yield Label("Unit Details")
        yield self.unit_properties_table

    def watch_unit(self, unit: DBusUnit) -> None:
        self.unit_properties_table.unit = unit
