from ttsystemd.ui.table.property_2_item import PropertyTable2Item
from rich.style import Style
from textual.app import App
from textual.reactive import reactive
from ttsystemd.systemd.runtime.types import SystemdDBusProperties

DEFAULTS_PROPERTIES = [
    "DefaultBlockIOAccounting",
    "DefaultCPUAccounting",
    "DefaultDeviceTimeoutUSec",
    "DefaultIOAccounting",
    "DefaultIPAccounting",
    "DefaultLimitAS",
    "DefaultLimitASSoft",
    "DefaultLimitCORE",
    "DefaultLimitCORESoft",
    "DefaultLimitCPU",
    "DefaultLimitCPUSoft",
    "DefaultLimitDATA",
    "DefaultLimitDATASoft",
    "DefaultLimitFSIZE",
    "DefaultLimitFSIZESoft",
    "DefaultLimitLOCKS",
    "DefaultLimitLOCKSSoft",
    "DefaultLimitMEMLOCK",
    "DefaultLimitMEMLOCKSoft",
    "DefaultLimitMSGQUEUE",
    "DefaultLimitMSGQUEUESoft",
    "DefaultLimitNICE",
    "DefaultLimitNICESoft",
    "DefaultLimitNOFILE",
    "DefaultLimitNOFILESoft",
    "DefaultLimitNPROC",
    "DefaultLimitNPROCSoft",
    "DefaultLimitRSS",
    "DefaultLimitRSSSoft",
    "DefaultLimitRTPRIO",
    "DefaultLimitRTPRIOSoft",
    "DefaultLimitRTTIME",
    "DefaultLimitRTTIMESoft",
    "DefaultLimitSIGPENDING",
    "DefaultLimitSIGPENDINGSoft",
    "DefaultLimitSTACK",
    "DefaultLimitSTACKSoft",
    "DefaultMemoryAccounting",
    "DefaultMemoryPressureThresholdUSec",
    "DefaultMemoryPressureWatch",
    "DefaultOOMPolicy",
    "DefaultOOMScoreAdjust",
    "DefaultRestartUSec",
    "DefaultStandardError",
    "DefaultStandardOutput",
    "DefaultStartLimitBurst",
    "DefaultStartLimitIntervalUSec",
    "DefaultTasksAccounting",
    "DefaultTasksMax",
    "DefaultTimeoutAbortUSec",
    "DefaultTimeoutStartUSec",
    "DefaultTimeoutStopUSec",
    "DefaultTimerAccuracyUSec",
]


class SystemdInfoDefaultsTable(PropertyTable2Item):
    systemd_properties = reactive(None)

    def __init__(self):
        _row_bg = Style(
            bgcolor=App().get_css_variables()["primary-background-lighten-1"]
        )
        super().__init__(DEFAULTS_PROPERTIES, row_styles=[_row_bg, ""])

    def watch_systemd_properties(self, systemd_properties: SystemdDBusProperties):
        if systemd_properties is not None:
            self.fill(systemd_properties)
