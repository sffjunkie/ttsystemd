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

    def on_tree_node_selected(self, message: Tree.NodeSelected):
        unit_type = message.node.label.plain
        if unit_type == "Units":
            unit_type = "*"
        self.units_overview.unit_type = unit_type
