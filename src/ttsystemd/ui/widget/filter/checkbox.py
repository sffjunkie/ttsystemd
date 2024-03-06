from textual.message import Message
from textual.widgets import Checkbox


class FilterTypeCheckbox(Checkbox):
    def __init__(self, label: str, **kwargs):
        self.unit_type = label.lower()
        super().__init__(label=label, value=True, classes="filter_checkbox")

    # class Changed(Message):
    #     def __init__(self, unit_type: str, value: bool):
    #         self.unit_type = unit_type
    #         self.value = value
    #         super().__init__()

    # def on_checkbox_changed(self):
    #     self.log.info("Checkbox")
    #     self.post_message(self.Changed(self.unit_type, self.value))

    # def on_toggle_button_clicked(self, msg: Message):
    #     self.log.info("Checkbox")
