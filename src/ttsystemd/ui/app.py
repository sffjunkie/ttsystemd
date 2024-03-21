from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive, Reactive
from textual.widgets import Footer, Header
from ttsystemd.ui.widget.content import Content
from ttsystemd.systemd.collect import collect, SystemdData


class SystemdApp(App):
    CSS_PATH = "ttsystemd.tcss"
    TITLE = "TT Systemd"
    SUB_TITLE = "a Systemd explorer"

    BINDINGS = [
        Binding(key="ctrl+q", action="quit", description="Quit the app"),
    ]

    systemd_data: Reactive[SystemdData | None] = reactive(None)

    def __init__(self) -> None:
        super().__init__()
        self.content = Content(id="content")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container(id="body"):
            yield self.content

    async def on_mount(self):
        self.content.systemd_data = self.systemd_data

    async def on_load(self) -> None:
        self.systemd_data = await collect()
