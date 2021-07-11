#!/bin/bash
pacman -Syu snapper snap-pac

create_config() {
    umount $1.snapshots
    rm -r $1.snapshots
    snapper -c $2 create-config $1
    btrfs subvolume delete $1.snapshots
    mkdir $1.snapshots
    mount -a
}

create_config / root
create_config /home/ home
