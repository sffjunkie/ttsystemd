import string

SPECIAL_CHARACTERS = "".join(set(string.punctuation) - set(("/", "_")))


class DBusObject:
    root: str
    name: str | None
    type: str | None

    def __init__(
        self, object_path: str, name: str | None = None, _type: str | None = None
    ):
        full_path = object_path.find(".") != -1 and name is None and _type is None
        if full_path:
            object_root, object_name, object_type = split_object_path(object_path)
        else:
            object_root = object_path
            object_name = name
            object_type = _type

        self.root = decode_object_path_elem(object_root)  # type: ignore
        if object_name is not None:
            self.name = decode_object_path_elem(object_name)
        else:
            self.name = None
        self.type = object_type

    @property
    def object_path(self):
        return f"{self.root}/{self.name}.{self.type}"

    def encode(self) -> str:
        root = encode_object_path_elem(self.root)
        name = encode_object_path_elem(self.name)
        return merge_object_path(root, name, self.type)

    @staticmethod
    def decode(object_path: str) -> "DBusObject":
        root, name, _type = split_object_path(object_path)
        root = decode_object_path_elem(root)  # type: ignore
        name = decode_object_path_elem(name)
        return DBusObject(root, name, _type)


def encode_object_path(object_path: str) -> str:
    root, name, _type = split_object_path(object_path)
    root = encode_object_path_elem(root)  # type: ignore
    name = encode_object_path_elem(name)
    return merge_object_path(root, name, _type)


def encode_object_path_elem(elem: str | None) -> str | None:
    if elem is None:
        return None

    for char in SPECIAL_CHARACTERS:
        elem = elem.replace(char, f"_{hex(ord(char))[2:].lower()}")
    return elem


def decode_object_path_elem(elem: str | None) -> str | None:
    if elem is None:
        return None

    for char in SPECIAL_CHARACTERS:
        elem = elem.replace(f"_{hex(ord(char))[2:].lower()}", char)
    return elem


def split_object_path(object_path: str) -> tuple[str, str | None, str | None]:
    try:
        root, name = object_path.rsplit("/", maxsplit=1)
    except ValueError:
        root = object_path
        name = None

    if name is not None:
        try:
            name, _type = name.rsplit(".", maxsplit=1)
        except ValueError:
            _type = None
    else:
        _type = None
    return root, name, _type


def merge_object_path(root, name, _type):
    if _type is None:
        return f"{root}/{name}"
    else:
        return f"{root}/{name}.{_type}"
