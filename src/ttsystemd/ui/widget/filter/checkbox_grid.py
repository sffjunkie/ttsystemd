from textual.message import Message
from textual.widget import Widget

from .checkbox import FilterTypeCheckbox


class FilterCheckboxGrid(Widget):
    def __init__(self):
        self.checkboxes = {}
        for name in [
            "Automount",
            "Device",
            "Mount",
            "Path",
            "Scope",
            "Service",
            "Slice",
            "Socket",
            "Swap",
            "Target",
            "Timer",
        ]:
            self.checkboxes[name.lower()] = FilterTypeCheckbox(name)
        super().__init__(*self.checkboxes.values())

    def on_checkbox_changed(self, message: Message):
        if isinstance(message.checkbox, FilterTypeCheckbox):
            self.log.info(
                f"*********************** Checkbox changed {message.checkbox.unit_type} to {message.checkbox.value}"
            )

            msg = self.Changed()
            for name in [
                "automount",
                "device",
                "mount",
                "path",
                "scope",
                "service",
                "slice",
                "socket",
                "swap",
                "target",
                "timer",
            ]:
                msg.__setattr__(name, self.checkboxes[name].value)

            self.post_message(msg)

    class Changed(Message):
        def __init__(self):
            self.automount = False
            self.device = False
            self.mount = False
            self.path = False
            self.scope = False
            self.service = False
            self.slice = False
            self.socket = False
            self.swap=False;
            self.target = False
            self.timer = False

            super().__init__()
