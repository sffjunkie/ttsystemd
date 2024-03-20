import pytest
from ttsystemd.systemd.runtime.dbus_object import (
    DBusObject,
    encode_object_path_elem,
    decode_object_path_elem,
    split_object_path,
    merge_object_path,
)


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("/run/sub/test/service.device", "/run/sub/test/service.device"),
        ("/run/sub/test.service", "/run/sub/test.service"),
        ("/run/sub/te@st.service", "/run/sub/te@st.service"),
    ),
)
def test_dbusobject_object_path_full_path(input: str, output: str):
    dbo = DBusObject(input)
    assert output == dbo.object_path


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        (("/root", "an_object", "device"), "/root/an_object.device"),
        (("/root", "an_ob@ject", "device"), "/root/an_ob@ject.device"),
    ),
)
def test_dbusobject_object_path_components(input: tuple[str, str, str], output: str):
    dbo = DBusObject(*input)
    assert output == dbo.object_path


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("/root/an_object.device", "/root/an_object.device"),
        ("/root/an_ob@ject.device", "/root/an_ob_40ject.device"),
    ),
)
def test_dbusobject_encode(input: str, output: str):
    dbo = DBusObject(input)
    assert output == dbo.encode()


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("/root/an_object.device", "/root/an_object.device"),
        ("/root/an_ob_40ject.device", "/root/an_ob@ject.device"),
    ),
)
def test_dbusobject_decode(input: str, output: str):
    dbo = DBusObject.decode(input)
    assert output == dbo.object_path


@pytest.mark.parametrize(
    argnames=("path", "output"),
    argvalues=(
        ("/root/test.device", ("/root", "test", "device")),
        ("/root/te@st.device", ("/root", "te@st", "device")),
    ),
)
def test_split_object_path(path: str, output: str):
    assert output == split_object_path(path)


@pytest.mark.parametrize(
    argnames=("path", "output"),
    argvalues=(
        (("/root", "test", "device"), "/root/test.device"),
        (("/root", "te@st", "device"), "/root/te@st.device"),
        (("/root", "te@st", None), "/root/te@st"),
    ),
)
def test_merge_object_path(path: str, output: str):
    assert output == merge_object_path(path[0], path[1], path[2])


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("te_40st.device", "te@st.device"),
        ("/root/te_3ast.service", "/root/te:st.service"),
    ),
)
def test_decode_object_path_elem(input: str, output: str):
    assert output == decode_object_path_elem(input)


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("/root/te@st", "/root/te_40st"),
        ("/root/te:st", "/root/te_3ast"),
    ),
)
def test_encode_object_path_elem(input: str, output: str):
    assert output == encode_object_path_elem(input)
