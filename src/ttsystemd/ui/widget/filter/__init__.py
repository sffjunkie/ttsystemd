from textual.message import Message
from textual.widgets import Collapsible, Input

from .checkbox_grid import FilterCheckboxGrid
# from .header import FilterHeader


class FilterWidget(Collapsible):
    """Filter widget

    ▶ InputWidget
    \[ ] Automount  [ ] Device
    \[ ] Mount      [ ] Path
    \[ ] Scope      [x] Service
    \[ ] Slice      [ ] Socket
    \[ ] Target     [ ] Timer
    """

    CSS = """
    Collapsible {
        width: 1fr;
        height: auto;
        background: $boost;
        border-top: hkey $background;
        padding-bottom: 1;
        padding-left: 1;
    }

    Collapsible.-collapsed > Contents {
        display: none;
    }

    FilterWidget {
        padding-bottom: 0;
        margin-bottom: 0;

        Input {
            margin-right: 1;
            margin-bottom: 0;
        }

        FilterCheckboxGrid {
            height: auto;
            layout: grid;
            grid-size: 2;
            grid-columns: 1fr 1fr;
            margin-right: 1;
            background: $sidebar_color;
            overlay: screen;
            constrain: y;
        }

        &.filter_checkbox {
            width: 100%;
        }
    }
    """

    def __init__(self):
        filter_text = Input(placeholder="Unit Name...")
        checkbox_grid = FilterCheckboxGrid()
        super().__init__(
            filter_text,
            checkbox_grid,
            title="Filter",
            id="filter",
        )

    def on_filter_checkbox_grid_changed(self, message: Message):
        self.log.info(
            f"*********************** Checkbox grid changed {message.automount}"
        )
