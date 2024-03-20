from textual.reactive import reactive
from ttsystemd.systemd.runtime.types import DBusUnitInfo
from textual.widgets import Tree


class UnitTypeTree(Tree):
    systemd_units = reactive(None)

    def __init__(
        self,
        label: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ):
        super().__init__(
            label,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.guide_depth = 3
        self.auto_expand = False
        self.root.expand()

    def watch_systemd_units(self, systemd_units: DBusUnitInfo) -> None:
        if systemd_units is not None:
            self.clear()
            if systemd_units is not None:
                self.sections = {
                    "automount": [],
                    "device": [],
                    "mount": [],
                    "path": [],
                    "scope": [],
                    "service": [],
                    "slice": [],
                    "socket": [],
                    "swap": [],
                    "target": [],
                    "timer": [],
                }

                for name, unit in systemd_units.items():
                    self.sections[unit.unit_type].append(name)

                for section, items in self.sections.items():
                    self.sections[section] = list(sorted(items))

                for section, items in self.sections.items():
                    s = self.root.add(section, expand=False)
                    if items:
                        for item in items:
                            s.add_leaf(item)
                    else:
                        s.add_leaf("No Units Found")
