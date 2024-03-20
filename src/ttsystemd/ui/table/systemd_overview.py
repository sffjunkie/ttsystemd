from rich import box
from rich.style import Style
from rich.table import Table
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Static
from ttsystemd.systemd.runtime.types import Properties
from ttsystemd import stringify
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES


class SystemdInfoOverviewTable(Container):
    systemd_properties = reactive(None)

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
        self.content = Static()
        self.content.renderable = self.table

    def compose(self) -> ComposeResult:
        yield self.content

    def watch_systemd_properties(self, properties: Properties) -> None:
        if properties:
            self.table.rows = []
            for item in [
                ("Version", properties["Version"]),
                ("Architecture", properties["Architecture"]),
                ("Unit Path", stringify.systemd_unit_path(properties["UnitPath"])),
                (
                    "Environment",
                    stringify.systemd_environment(properties["Environment"]),
                ),
                ("Features", stringify.systemd_features(properties["Features"])),
            ]:
                self.table.add_row(*item)
