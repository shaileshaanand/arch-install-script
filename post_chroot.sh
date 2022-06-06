#!/bin/bash
HOSTNAME="MSIArchBox"
USERNAME="shailesh"
PASSWORD="shailesh"
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
echo root:$PASSWORD | chpasswd
useradd -m -g users -G wheel,storage,power -s /bin/zsh $USERNAME
echo $USERNAME:$PASSWORD | chpasswd
mkdir -p /boot/efi
mount /dev/nvme0n1p1 /boot/efi
grub-install --target=x86_64-efi --bootloader-id=ARCHLINUX --efi-directory=/boot/efi --recheck
grub-mkconfig -o /boot/grub/grub.cfg
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/$USERNAME
