from textual.message import Message
from textual.widgets._collapsible import CollapsibleTitle

from .checkbox_grid import FilterCheckboxGrid


class FilterHeader(CollapsibleTitle):
    def __init__(
        self,
        collapsed_symbol: str,
        expanded_symbol: str,
        collapsed: bool,
    ):
        self._id = "aa"
        super().__init__(
            collapsed_symbol=collapsed_symbol,
            expanded_symbol=expanded_symbol,
            collapsed=collapsed,
        )

    class Toggle(Message):
        """Request toggle."""

    class Changed(Message):
        checkbox_info: FilterCheckboxGrid.Changed

    class Collapsed(Message):
        collapsed: bool

    def on_filter_header_expanded(msg: Message): ...
