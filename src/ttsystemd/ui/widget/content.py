from textual.app import ComposeResult
from textual.reactive import reactive, Reactive
from textual.widget import Widget
from textual.widgets import TabbedContent, TabPane
from ttsystemd.systemd.collect import SystemdData
from ttsystemd.ui.pane.system_units import SystemUnitsPane
from ttsystemd.ui.pane.systemd_info import SystemdInfoPane
from ttsystemd.ui.pane.user_units import UserUnitsPane


class Content(Widget):
    systemd_data: Reactive[SystemdData | None] = reactive(None)

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.info_pane = SystemdInfoPane()
        self.system_pane = SystemUnitsPane()
        self.user_pane = UserUnitsPane()

    def compose(self) -> ComposeResult:
        with TabbedContent():
            with TabPane("Systemd Information"):
                yield self.info_pane

            with TabPane("System Units"):
                yield self.system_pane

            with TabPane("User Units"):
                yield self.user_pane

    def watch_systemd_data(self, data: SystemdData) -> None:
        if data is not None:
            self.info_pane.systemd_properties = data.properties
            self.system_pane.systemd_units = data.system_units
            self.user_pane.systemd_units = data.session_units
