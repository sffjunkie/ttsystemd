from textual.widgets import ListView, ListItem, Label


class SidebarSectionContent(ListView):
    def __init__(self, title: str, items: list[str] | None = None):
        self.title = title
        self.not_found = self._create_list_item(f"No {title.lower()}s found")

        if items is not None:
            super().__init__(*self._create_list_items(items))
        else:
            super().__init__(self.not_found)

    def _create_list_item(self, title: str) -> ListItem:
        return ListItem(Label(title))

    def _create_list_items(self, items: list[str]) -> list[ListItem]:
        return [self._create_list_item(item) for item in items]

    def update(self, items: list[str] | None = None):
        self.clear()
        self.items = items
        if items is None:
            self.append(self.not_found)
        else:
            self.extend(self._create_list_items(items))


def wrap_dbus_path(text: str, width: int, split_char: str = "/"):
    runs = text.lstrip(split_char).split(split_char)
    line = ""
    lines = []
    for r in runs:
        if len(line) + len(r) > width:
            lines.append(line)
            line = split_char + r
        else:
            line += split_char + r
    lines.append(line)
    return "\n".join(lines)
