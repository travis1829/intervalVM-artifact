./install-packages.sh

if [ ! -f "/boot/initrd.img-6.8.0" ]; then
    ./install-linux-6.8.0.sh
fi
if [ ! -f "/boot/initrd.img-6.8.0-debug" ]; then
    ./install-linux-6.8.0-debug.sh
fi
if [ ! -f "/boot/initrd.img-6.8.0-interval-vm+" ]; then
    ./install-linux-ivm.sh
fi
if [ ! -f "/boot/initrd.img-6.8.0-interval-vm-debug+" ]; then
    ./install-linux-ivm-debug.sh
fi

if [ ! -d "/usr/local/apache2" ]; then
    ./install-apache.sh
fi
./install-metis.sh
./install-psearchy.sh
