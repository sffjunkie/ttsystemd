from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import Reactive, reactive
from ttsystemd.ui.widget.sidebar import Sidebar


class UserUnitsPane(Container):
    systemd_units = reactive(None)
    unit_type = reactive("*")

    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar(id="system_units_sidebar")
        self.units_overview = SystemdUnitsTable()

    def compose(self) -> ComposeResult:
        yield self.sidebar
        with Container():
            yield self.units_overview

    def watch_systemd_units(self, systemd_units: UnitData) -> None:
        if systemd_units is not None:
            self.sidebar.systemd_units = systemd_units
            self.units_overview.systemd_units = systemd_units

    def watch_unit_type(self, unit_type: str) -> None:
        if self.systemd_units is not None:
            self.sidebar.systemd_units = self.systemd_units
            self.units_overview.unit_type = unit_type

    @on(Tree.NodeSelected)
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

        units_overview = self.query_one("UnitsOverview")
        unit_details = self.query_one("UnitDetails")

        if is_unit_type:
            units_overview.display = True
            if item == "Units":
                item = "*"
            self.units_overview.unit_type = item

            unit_details.display = False
        else:
            self.units_overview.display = False
            self.unit_details.unit = self.systemd_units[item]
            self.unit_details.display = True

