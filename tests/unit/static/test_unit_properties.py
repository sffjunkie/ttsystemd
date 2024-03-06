from ttsystemd.systemd.static.unit_properties import parse_properties

TEXT = """SendSIGKILL=yes
SendSIGHUP=no
WatchdogSignal=6
Id=gnome-session-manager@gnome.service
Names=gnome-session-manager@gnome.service
"""


def test_parse_properties():
    result = parse_properties(TEXT)
    assert len(result) == 5
    assert result["WatchdogSignal"] == "6"
