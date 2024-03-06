from time import localtime, strftime

MAX = 0xFFFFFFFFFFFFFFFF


def systemd_bool(value: bool) -> str:
    return "true" if bool else "false"


def systemd_max(value: int) -> str:
    if value == MAX:
        return "Max"
    else:
        return str(value)


def systemd_timestamp(value: int) -> str:
    if value == MAX:
        return "Heat Death of Universe"
    elif value != 0:
        seconds = value / 1_000_000
        t = localtime(seconds)
        return strftime("%A %d-%m-%Y %H:%M:%S UTC", t)
    else:
        return "-"


def systemd_monotonic(value: int) -> str:
    if value != 0:
        return str(value)
    else:
        return "-"


def systemd_unit_path(path: list[str]) -> str:
    return "\n".join(sorted(path))


def systemd_environment(env: dict[str, str]) -> str:
    return "\n".join([f"{k}={v}" for k, v in sorted(env.items())])


def systemd_features(features: list[str]) -> str:
    plus = filter(lambda feature: feature.startswith("+"), features)
    minus = filter(lambda feature: feature.startswith("-"), features)
    other = filter(
        lambda feature: not feature.startswith("+") and not feature.startswith("-"),
        features,
    )
    info = [
        ", ".join(sorted(plus)),
        ", ".join(sorted(minus)),
        ", ".join(sorted(other)),
    ]

    return "\n".join(info)
