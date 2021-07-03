#!/usr/bin/env python3

from typing import List, NamedTuple, Tuple
from collections import namedtuple
from pathlib import Path
import subprocess
from unittest.mock import patch, Mock


def execute(cmd, **kwargs):
    print("Running: ", " ".join(cmd))
    return subprocess.run(cmd, **kwargs)


class Mount(NamedTuple):
    mount_point: Path
    physical_location: Path
    subvolume: Path


BTRFS_MOUNT_OPTIONS = [
    "ssd",
    "noatime",
    "discard=async",
    "space_cache",
    "commit=120",
    "compress=zstd",
    "subvol={subvol}"
]


def create_subvolume(path: Path):
    execute(["btrfs", "su", "cr", str(path)])


def create_mounts(install_partition: Path, mount_points: List[Tuple[str]], subvolume_prefix: Path, mount_prefix: Path, swap: Path):
    mounts = [Mount(Path(mount_point), install_partition, subvolume_prefix/subvolume)
              for mount_point, subvolume in mount_points]

    # Path(mount_prefix).mkdir(parents=True, exist_ok=True)
    if swap:
        execute(["mkfs.swap", str(swap)])
        execute(["swapon", str(swap)])
    execute(
        ["mkdir", "-p", str(mount_prefix)])
    execute(["mount", str(install_partition), str(mount_prefix)])
    create_subvolume(mount_prefix/subvolume_prefix)
    for mount in mounts:
        create_subvolume(mount_prefix/mount.subvolume)
    execute(["umount", "-R", str(mount_prefix)])

    for mount in mounts:
        # (mount_prefix/mount.mount_point).mkdir(parents=True)
        execute(
            ["mkdir", "-p", str(mount_prefix/mount.mount_point.relative_to("/"))])
        execute([
            "mount",
            "-o",
            ",".join(BTRFS_MOUNT_OPTIONS).format(subvol=mount.subvolume),
            str(install_partition),
            str(mount_prefix/mount.mount_point.relative_to("/"))
        ])


if __name__ == "__main__":
    mount_prefix = Path("/mnt")
    subvol_prefix = Path("@arch")
    swap = None
    packages = [
        "base",
        "base-devel",
        "linux",
        "linux-firmware",
        "vim",
        "dhcpcd",
        "iwd",
        "zsh",
    ]
    create_mounts(
        Path("/dev/nvme0n1p2"),
        [
            ("/", "@root"),
            ("/home", "@home"),
            ("/.snapshots", "@root_snapshots"),
            ("/home/.snapshots", "@home_snapshots"),
            ("/var/log", "@var_log"),
            ("/var/cache/pacman/pkg", "@pkg_cache"),
        ],
        subvol_prefix,
        mount_prefix,
        swap=swap
    )
    execute(["pacstrap", str(mount_prefix)]+packages)
    fstab = execute(["genfstab", "-U", str(mount_prefix)],
                    capture_output=True, text=True).stdout
    with open(mount_prefix/"etc/fstab", "a") as fstab_file:
        fstab_file.write(fstab)
