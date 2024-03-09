import asyncio
from textual.app import App
from textual.binding import Binding
from textual.widgets import Footer, Header
from textual.containers import Container

from ttsystemd.systemd.runtime.types import SystemdDBusProperties
from ttsystemd.ui.widget.content import Content

from ttsystemd.systemd.types import SessionType
from ttsystemd.systemd.runtime.manager import (
    dbus_manager_collect_properties,
    dbus_manager_collect_units,
)
# from ttsystemd.systemd.static.collect import json_collect_units


class SystemdApp(App):
    CSS_PATH = "ttsystemd.tcss"
    TITLE = "TT Systemd"
    SUB_TITLE = "a Systemd explorer"

    BINDINGS = [
        Binding(key="ctrl+q", action="quit", description="Quit the app"),
    ]

    def __init__(self):
        super().__init__()
        self.content = Content(id="content")

    def compose(self) -> None:
        yield Header()
        yield Footer()
        with Container(id="body"):
            yield self.content

    def action_quit(self) -> None:
        self.exit()

    async def on_load(self):
        self.systemd_data = await self.get_data()

    async def on_mount(self):
        # self.systemd_data = await self.get_data()
        self.content.systemd_data = self.systemd_data

    async def get_data(self) -> list[SystemdDBusProperties]:
        return await asyncio.gather(
            dbus_manager_collect_properties(SessionType.SYSTEM),
            dbus_manager_collect_units(SessionType.SYSTEM),
            dbus_manager_collect_units(SessionType.USER_SESSION),
        )
