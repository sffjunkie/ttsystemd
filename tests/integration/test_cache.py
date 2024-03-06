import os

import pytest
from ttsystemd.systemd.cache import load_systemd_interface_definition


@pytest.mark.xfail("VSCODE_PID" in os.environ, reason="Fails under vscode")
def test_load_systemd_interface_file():
    interface = load_systemd_interface_definition("mount")
    assert interface is not None
