from rich import box
from rich.style import Style
from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Static, Label
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES


class UnitPropertiesTable(Container):
    unit = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        _row_bg = Style(
            bgcolor=App().get_css_variables()["primary-background-lighten-1"]
        )
        self.table = Table(
            expand=True,
            box=box.SIMPLE_HEAD,
            # leading=1,
            show_header=False,
            show_footer=False,
            row_styles=[_row_bg, ""],
        )
        w = max([len(item[0]) for item in MANAGER_PROPERTIES.values()]) + 1
        self.table.add_column(width=w)
        self.table.add_column(width=None, ratio=1)
        # self.content = Static()
        # self.content.renderable = self.table
        self.content = Label("To Be Added...")

    def compose(self) -> ComposeResult:
        yield self.content

    def watch_unit(self, unit) -> None:
        if unit is not None:
            self.table.rows = []
            for item in [
                ("Version", "?"),
            ]:
                self.table.add_row(*item)
