from rich.style import Style
from textual.app import App
from textual.reactive import reactive
from ttsystemd.systemd.runtime.types import Properties
from ttsystemd.ui.table.property_2_item import PropertyTable2Item

TIMESTAMPS_PROPERTIES = [
    "FinishTimestamp",
    "FinishTimestampMonotonic",
    "GeneratorsStartTimestamp",
    "GeneratorsStartTimestampMonotonic",
    "GeneratorsFinishTimestamp",
    "GeneratorsFinishTimestampMonotonic",
    "InitRDTimestamp",
    "InitRDTimestampMonotonic",
    "InitRDGeneratorsStartTimestamp",
    "InitRDGeneratorsStartTimestampMonotonic",
    "InitRDGeneratorsFinishTimestamp",
    "InitRDGeneratorsFinishTimestampMonotonic",
    "InitRDSecurityStartTimestamp",
    "InitRDSecurityStartTimestampMonotonic",
    "InitRDSecurityFinishTimestamp",
    "InitRDSecurityFinishTimestampMonotonic",
    "InitRDUnitsLoadStartTimestamp",
    "InitRDUnitsLoadStartTimestampMonotonic",
    "InitRDUnitsLoadFinishTimestamp",
    "InitRDUnitsLoadFinishTimestampMonotonic",
    "KernelTimestamp",
    "KernelTimestampMonotonic",
    "LoaderTimestamp",
    "LoaderTimestampMonotonic",
    "SecurityFinishTimestamp",
    "SecurityFinishTimestampMonotonic",
    "UnitsLoadFinishTimestamp",
    "UnitsLoadFinishTimestampMonotonic",
    "UnitsLoadStartTimestamp",
    "UnitsLoadStartTimestampMonotonic",
    "UnitsLoadTimestamp",
    "UnitsLoadTimestampMonotonic",
    "UserspaceTimestamp",
    "UserspaceTimestampMonotonic",
    "WatchdogLastPingTimestamp",
    "WatchdogLastPingTimestampMonotonic",
]


class SystemdInfoTimestampsTable(PropertyTable2Item):
    systemd_properties = reactive(None)

    def __init__(self):
        _row_bg = Style(
            bgcolor=App().get_css_variables()["primary-background-lighten-1"]
        )
        super().__init__(TIMESTAMPS_PROPERTIES, row_styles=[_row_bg, ""])

    def watch_systemd_properties(self, systemd_properties: Properties):
        if systemd_properties is not None:
            self.fill(systemd_properties)
