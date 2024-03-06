import re
import string

_underscorer1 = re.compile(r"(.)([A-Z][a-z]+)")
_underscorer2 = re.compile(r"([a-z0-9])([A-Z])")

SPECIAL_CHARACTERS = "".join(set(string.punctuation) - set(("/", "_")))


def name_to_snake_case(member):
    subbed = _underscorer1.sub(r"\1_\2", member)
    return _underscorer2.sub(r"\1_\2", subbed).lower()
