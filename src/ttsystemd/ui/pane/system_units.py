from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Tree
from ttsystemd.systemd.runtime.types import DBusUnitInfo
from ttsystemd.ui.table.units import SystemdUnitsTable
from ttsystemd.ui.widget.sidebar import Sidebar
from ttsystemd.ui.widget.unit_details import UnitDetails


class SystemUnitsPane(Container):
    systemd_units = reactive(None)
    unit_type = reactive("*")

    def __init__(self):
        super().__init__()
        self.sidebar = Sidebar(id="system_units_sidebar")
        self.units_overview = SystemdUnitsTable()
        self.unit_details = UnitDetails()
        self.unit_details.display = False

    def compose(self):
        yield self.sidebar
        with Container():
            yield self.units_overview
            yield self.unit_details

    def watch_systemd_units(self, systemd_units: DBusUnitInfo):
        if systemd_units is not None:
            self.sidebar.systemd_units = systemd_units
            self.units_overview.systemd_units = systemd_units

    def watch_unit_type(self, unit_type: str):
        if self.systemd_units is not None:
            self.sidebar.systemd_units = self.systemd_units
            self.units_overview.unit_type = unit_type

    def on_tree_node_selected(self, message: Tree.NodeSelected):
        item = message.node.label.plain
        if item == "No Units Found":
            return

        is_unit_type = item.find(".") == -1

        units_table = self.query_one("SystemdUnitsTable")
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
