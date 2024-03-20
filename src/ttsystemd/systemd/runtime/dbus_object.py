import string
from typing import Self

SPECIAL_CHARACTERS = "".join(set(string.punctuation) - set(("/", "_")))


class DBusObject:
    root: str
    name: str
    type: str

    def __init__(
        self, object_path: str, name: str | None = None, _type: str | None = None
    ):
        full_path = object_path.find(".") != -1
        if full_path:
            root, name, _type = split_object_path(object_path)
        else:
            root = object_path
            name = name
            _type = _type
        root = decode_object_path_elem(root)
        name = decode_object_path_elem(name)
        self.root = root
        self.name = name
        self.type = _type

    @property
    def object_path(self):
        return f"{self.root}/{self.name}.{self.type}"

    def encode(self) -> str:
        root = encode_object_path_elem(self.root)
        name = encode_object_path_elem(self.name)
        return merge_object_path(root, name, self.type)

    @staticmethod
    def decode(object_path: str) -> Self:
        root, name, _type = split_object_path(object_path)
        root = decode_object_path_elem(root)
        name = decode_object_path_elem(name)
        return DBusObject(root, name, _type)


def encode_object_path(object_path: str) -> str:
    root, name, _type = split_object_path(object)
    root = encode_object_path_elem(root)
    name = encode_object_path_elem(name)
    return merge_object_path(root, name, _type)


def encode_object_path_elem(elem: str) -> str:
    for char in SPECIAL_CHARACTERS:
        elem = elem.replace(char, f"_{hex(ord(char))[2:].lower()}")
    return elem


def decode_object_path_elem(elem: str) -> str:
    for char in SPECIAL_CHARACTERS:
        elem = elem.replace(f"_{hex(ord(char))[2:].lower()}", char)
    return elem


def split_object_path(object_path: str) -> tuple[str, str, str | None]:
    root, name = object_path.rsplit("/", maxsplit=1)
    try:
        name, _type = name.rsplit(".", maxsplit=1)
    except ValueError:
        _type = None
    return root, name, _type


def merge_object_path(root, name, _type):
    if _type is None:
        return f"{root}/{name}"
    else:
        return f"{root}/{name}.{_type}"
