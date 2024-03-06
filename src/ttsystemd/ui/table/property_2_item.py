from textual.widgets import Static
from itertools import islice, zip_longest

from rich import box
from rich.style import Style
from rich.table import Table
from ttsystemd.systemd.runtime.properties import MANAGER_PROPERTIES
from ttsystemd.systemd.runtime.utils import name_to_snake_case


class PropertyTable2Item(Static):
    def __init__(self, properties, row_styles: list[Style] | None = None):
        super().__init__()
        self.properties = properties
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

    def fill(self, prop_data: list[str]):
        system_data = prop_data.properties

        prop_order = list(
            zip_longest(
                islice(self.properties, 0, None, 2),
                islice(self.properties, 1, None, 2),
            )
        )

        for row in prop_order:
            prop_id0 = name_to_snake_case(row[0])
            prop_display_func0 = MANAGER_PROPERTIES[prop_id0][1]
            items = [
                row[0],
                prop_display_func0(system_data[prop_id0]),
            ]
            if row[1]:
                prop_id1 = name_to_snake_case(row[1])
                prop_display_func1 = MANAGER_PROPERTIES[prop_id1][1]
                items.append(row[1])
                items.append(prop_display_func1(system_data[prop_id1]))

            self.table.add_row(*items)
        self.renderable = self.table
