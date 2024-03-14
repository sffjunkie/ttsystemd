import os

import pytest
from ttsystemd.systemd.runtime.cache.interface_definition import (
    systemd_load_interface_definition,
)


@pytest.mark.xfail("VSCODE_PID" in os.environ, reason="Fails under vscode")
def test_systemd_load_interface_definition():
    interface = systemd_load_interface_definition("mount")
    assert interface is not None
