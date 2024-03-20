from textual.reactive import reactive
from textual.containers import Vertical, Horizontal
from textual.widgets import Button

from ttsystemd.systemd.runtime.types import DBusUnitInfo
from ttsystemd.ui.widget.sidebar.units_tree import UnitTypeTree

SIDEBAR_WIDTH = 60


class Sidebar(Vertical):
    systemd_units = reactive(None)

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.unit_tree = UnitTypeTree("Units")

    def compose(self):
        yield self.unit_tree
        with Horizontal():
            yield Button("Expand All")
            yield Button("Collapse All")

    def watch_systemd_units(self, systemd_units: DBusUnitInfo) -> None:
        if systemd_units is not None:
            self.unit_tree.systemd_units = systemd_units

    def on_button_pressed(self, event: Button.Pressed):
        label = event.button.label.plain
        if label == "Expand All":
            self.unit_tree.root.expand_all()
        elif label == "Collapse All":
            self.unit_tree.root.collapse_all()
