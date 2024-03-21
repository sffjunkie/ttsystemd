from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive, Reactive
from textual.widgets import Tree
from ttsystemd.ui.widget.sidebar import Sidebar
from ttsystemd.ui.widget.units_overview import UnitsOverview
from ttsystemd.ui.widget.unit_details import UnitDetails
from ttsystemd.systemd.merge import UnitData


class SystemUnitsPane(Container):
    systemd_units: Reactive[UnitData | None] = reactive(None)
    unit_type: Reactive[str] = reactive("*")

    def __init__(self) -> None:
        super().__init__()
        self.sidebar = Sidebar(id="system_units_sidebar")
        self.units_overview = UnitsOverview()
        self.unit_details = UnitDetails()
        self.unit_details.display = False

    def compose(self) -> ComposeResult:
        yield self.sidebar
        with Container():
            yield self.units_overview
            yield self.unit_details

    def watch_systemd_units(self, systemd_units: UnitData | None) -> None:
        if systemd_units is not None:
            self.sidebar.systemd_units = systemd_units
            self.units_overview.systemd_units = systemd_units

    def watch_unit_type(self, unit_type: str) -> None:
        if self.systemd_units is not None:
            self.sidebar.systemd_units = self.systemd_units
            self.units_overview.unit_type = unit_type

    def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        if self.systemd_units is None:
            return

        if isinstance(message.node.label, str):
            item = message.node.label
        else:
            item = message.node.label.plain

        if item == "No Units Found":
            return

        is_unit_type = item.find(".") == -1

        units_table = self.query_one("UnitsTable")
        unit_details = self.query_one("UnitDetails")

        if is_unit_type:
            units_table.display = True
            if item == "Units":
                item = "*"
            self.units_overview.unit_type = item

            unit_details.display = False
        else:
            units_table.display = False

            self.unit_details.unit = self.systemd_units[item]
            unit_details.display = True
