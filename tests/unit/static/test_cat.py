from ttsystemd.systemd.static.unit_cat import parse_cat

TEXT = """# /etc/systemd/system/ModemManager.service
[Unit]
Description=Modem Manager
After=polkit.service
Requires=polkit.service
ConditionVirtualization=!container

[Service]
Type=dbus
BusName=org.freedesktop.ModemManager1
ExecStart=/nix/store/59rqnr71493h9xm9pzbap1qk62mwnfhx-modemmanager-1.22.0/sbin/ModemManager
StandardError=null
Restart=on-abort
CapabilityBoundingSet=CAP_SYS_ADMIN CAP_NET_ADMIN
ProtectSystem=true
ProtectHome=true
PrivateTmp=true
RestrictAddressFamilies=AF_NETLINK AF_UNIX AF_QIPCRTR
NoNewPrivileges=true
User=root

[Install]
WantedBy=multi-user.target
Alias=dbus-org.freedesktop.ModemManager1.service

# /nix/store/6xm8hv5f7q6r294gqqhrfp90lq8m3cp3-system-units/ModemManager.service.d/overrides.conf
[Unit]

[Service]
Environment="LOCALE_ARCHIVE=/nix/store/5x9bvdsk82di20dlmm222wpwcd46xdjg-glibc-locales-2.38-44/lib/locale/locale-archive"
Environment="PATH=/nix/store/bicmg5gd50q6igk0y5mga1v0p1lk8f26-coreutils-9.4/bin:/nix/store/p6fd7piqrin2h0mqxzmvyxyr6pyivndj-findutils-4.9.0/bin:/nix/store/mn911d51n5lklwr3zy4mdhxa77wzancb-gn
ugrep-3.11/bin:/nix/store/vd92lhcxs39hbdnzj8ycak5wvj466s3l-gnused-4.9/bin:/nix/store/m0nicpa4d724rljadlmw1m3qv0ja4syy-systemd-255.2/bin:/nix/store/bicmg5gd50q6igk0y5mga1v0p1lk8f26-coreutils-
9.4/sbin:/nix/store/p6fd7piqrin2h0mqxzmvyxyr6pyivndj-findutils-4.9.0/sbin:/nix/store/mn911d51n5lklwr3zy4mdhxa77wzancb-gnugrep-3.11/sbin:/nix/store/vd92lhcxs39hbdnzj8ycak5wvj466s3l-gnused-4.9
/sbin:/nix/store/m0nicpa4d724rljadlmw1m3qv0ja4syy-systemd-255.2/sbin"
Environment="TZDIR=/nix/store/dwfm7k4s037k0v9zljabzdmndmsfgy84-tzdata-2024a/share/zoneinfo"
"""


def test_json_cat_multiple_files():
    bfs = parse_cat(TEXT)
    assert len(bfs) == 2
