from textual.widgets import Static
from itertools import islice, zip_longest

from rich import box
from rich.style import Style
from rich.table import Table
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES
from ttsystemd.systemd.runtime.utils import name_to_snake_case
from ttsystemd.systemd.runtime.types import Properties


class PropertyTable2Item(Static):
    def __init__(self, property_names: list[str], row_styles: list[Style] | None = None):
        super().__init__()
        self.property_names = property_names
        self.table = Table(
            expand=True,
            box=box.SIMPLE_HEAD,
            show_header=False,
            show_footer=False,
        )
        if row_styles is not None:
            self.table.row_styles = row_styles

        w = max([len(item[0]) for item in MANAGER_PROPERTIES.values()]) + 1
        self.table.add_column(width=w)
        self.table.add_column(width=None, ratio=1)
        self.table.add_column(width=w)
        self.table.add_column(width=None, ratio=1)

    def fill(self, properties: Properties):
        prop_order = zip_longest(
            islice(self.property_names, 0, None, 2),
            islice(self.property_names, 1, None, 2),
        )

        for row in prop_order:
            prop_name = row[0]
            prop_display_func0 = MANAGER_PROPERTIES[prop_name][1]
            if prop_display_func0 is None:
                pass
            items = [
                row[0],
                prop_display_func0(properties[prop_name]),
            ]
            if row[1]:
                prop_name = row[1]
                prop_display_func1 = MANAGER_PROPERTIES[prop_name][1]
                items.append(row[1])
                items.append(prop_display_func1(properties[prop_name]))

            self.table.add_row(*items)
        self.renderable = self.table
