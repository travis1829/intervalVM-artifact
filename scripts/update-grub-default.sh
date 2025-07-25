#!/bin/bash

set -e

# Check for required argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 \"<version>\""
    echo "Example: $0 \"6.8.0\""
    exit 1
fi

KERNEL_VERSION="$1"
GRUB_FILE="/etc/default/grub"
GRUB_VALUE="GRUB_DEFAULT=\"Advanced options for Ubuntu>Ubuntu, with Linux $KERNEL_VERSION\""

# Update or add GRUB_DEFAULT
if grep -q '^GRUB_DEFAULT=' "$GRUB_FILE"; then
    sudo sed -i "s|^GRUB_DEFAULT=.*|$GRUB_VALUE|" "$GRUB_FILE"
    echo "Updated GRUB_DEFAULT to use: $KERNEL_VERSION"
else
    echo "$GRUB_VALUE" | sudo tee -a "$GRUB_FILE" > /dev/null
    echo "Added GRUB_DEFAULT with: $KERNEL_VERSION"
fi

# Update GRUB
echo "Updating GRUB configuration..."
if [ -x /usr/sbin/update-grub ]; then
    sudo update-grub
elif [ -x /usr/sbin/grub-mkconfig ]; then
    sudo grub-mkconfig -o /boot/grub/grub.cfg
else
    echo "Warning: GRUB update command not found!"
fi
