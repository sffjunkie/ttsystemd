import pytest
from ttsystemd.systemd.runtime.utils import name_to_snake_case


@pytest.mark.parametrize(
    argnames=("input", "output"),
    argvalues=(
        ("Tainted", "tainted"),
        ("FinishTimestamp", "finish_timestamp"),
    ),
)
def test_name_to_snake_case(input: str, output: str):
    assert name_to_snake_case(input) == output
