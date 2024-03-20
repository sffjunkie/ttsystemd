from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Footer, Header
from ttsystemd.systemd.runtime.collect.system import DBusSystemCollector
from ttsystemd.ui.widget.content import Content

# from ttsystemd.systemd.static.collect import json_collect_units


class SystemdApp(App):
    CSS_PATH = "ttsystemd.tcss"
    TITLE = "TT Systemd"
    SUB_TITLE = "a Systemd explorer"

    BINDINGS = [
        Binding(key="ctrl+q", action="quit", description="Quit the app"),
    ]

    dbus_collector = reactive(None)

    def __init__(self):
        super().__init__()
        self.content = Content(id="content")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container(id="body"):
            yield self.content

    def action_quit(self) -> None:
        self.exit()

    async def on_mount(self):
        # self.systemd_data = await self.get_data()
        self.content.systemd_collector = self.dbus_collector

    async def on_load(self):
        self.dbus_collector = DBusSystemCollector()
        await self.dbus_collector.collect()

