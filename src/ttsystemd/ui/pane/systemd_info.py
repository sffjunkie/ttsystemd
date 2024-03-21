from textual.widgets import Label
from textual.containers import VerticalScroll
from textual.reactive import reactive, Reactive
from ttsystemd.systemd.runtime.types import Properties

from ttsystemd.ui.table.systemd_defaults import SystemdInfoDefaultsTable
from ttsystemd.ui.table.systemd_overview import SystemdInfoOverviewTable
from ttsystemd.ui.table.systemd_timestamps import SystemdInfoTimestampsTable


class SystemdInfoPane(VerticalScroll):
    systemd_properties: Reactive[Properties | None] = reactive(None)

    def __init__(self):
        self.overview_table = SystemdInfoOverviewTable()
        self.defaults_table = SystemdInfoDefaultsTable()
        self.timestamps_table = SystemdInfoTimestampsTable()
        super().__init__(
            Label("Overview"),
            self.overview_table,
            Label("Defaults"),
            self.defaults_table,
            Label("Timestamps"),
            self.timestamps_table,
        )

    def watch_systemd_properties(self, systemd_properties: Properties):
        if systemd_properties is not None:
            self.overview_table.systemd_properties = systemd_properties
            self.defaults_table.systemd_properties = systemd_properties
            self.timestamps_table.systemd_properties = systemd_properties
