import os
from pathlib import Path
from xdg_base_dirs import xdg_cache_home

FORCE_NIXOS = "NIXPKGS_CONFIG" in os.environ


def cache_home() -> Path:
    cache_home = xdg_cache_home() / "ttsystemd"
    if not cache_home.exists():
        cache_home.mkdir()
    return cache_home


def dbus_interface_file_default_paths() -> str:
    if Path("/etc/NIXOS").exists() or FORCE_NIXOS:
        return [
            Path("/run/current-system/sw/share/dbus-1/interfaces/"),
        ]
    else:
        return [
            Path("/usr/local/share/dbus-1/interfaces"),
        ]


def dbus_interface_file_paths() -> str:
    return dbus_interface_file_default_paths() + [cache_home()]


# org.freedesktop.systemd1.Mount.xml
def dbus_load_interface_definition(filename: str) -> str | None:
    p = Path(filename)
    if p.is_absolute() and p.exists():
        with p.open("r") as fp:
            introspection = fp.read(-1)
            return introspection
    else:
        search_paths = dbus_interface_file_paths()
        for path in search_paths:
            load_path = path / filename

            if load_path.exists():
                with load_path.open("r") as fp:
                    introspection = fp.read(-1)
                    return introspection

    return IOError(f"interface definition {filename} not found")


def systemd_interface_for_type(interface_type: str) -> str:
    if not interface_type.startswith("org.freedesktop.systemd1."):
        return f"org.freedesktop.systemd1.{interface_type}"
    else:
        return interface_type


def systemd_load_interface_definition(interface_type: str) -> str | None:
    interface_name = systemd_interface_for_type(interface_type.capitalize())
    interface = dbus_load_interface_definition(interface_name)
    return interface
