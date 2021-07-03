#!/bin/bash
HOSTNAME="MSIArchBox"
ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
hwclock --systohc --utc
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo $HOSTNAME > /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1 localhost" >> /etc/hosts
echo "127.0.1.1 $HOSTNAME.localdomain $HOSTNAME" >> /etc/hosts
systemctl enable dhcpcd