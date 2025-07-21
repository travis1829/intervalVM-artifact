sudo rm -rf ../apache/httpd-2.4.62
rm -rf ../apache/wrk
sudo rm -rf /usr/local/apache2

if [ -d ../ds_benchmark/jemalloc ]; then
    # sudo make uninstall -C ../ds_benchmark/jemalloc
    rm -rf ../ds_benchmark/jemalloc
fi

make clean -C ../metis

make clean -C ../psearchy
rm -rf ../psearchy/linux-6.8
rm -f ../psearchy/linux-6.8-files.txt

rm -rf ../linux-6.8
rm -rf ../linux-6.8-interval_vm

sudo rm -f /boot/System.map-6.8.0 /boot/config-6.8.0 /boot/initrd.img-6.8.0 /boot/vmlinuz-6.8.0
sudo rm -rf /lib/modules/6.8.0

sudo rm -f /boot/System.map-6.8.0-debug /boot/config-6.8.0-debug /boot/initrd.img-6.8.0-debug /boot/vmlinuz-6.8.0-debug
sudo rm -rf /lib/modules/6.8.0-debug

sudo rm -f /boot/System.map-6.8.0-interval-vm+ /boot/config-6.8.0-interval-vm+ /boot/initrd.img-6.8.0-interval-vm+ /boot/vmlinuz-6.8.0-interval-vm+
sudo rm -rf /lib/modules/6.8.0-interval-vm+

sudo rm -f /boot/System.map-6.8.0-interval-vm-debug+ /boot/config-6.8.0-interval-vm-debug+ /boot/initrd.img-6.8.0-interval-vm-debug+ /boot/vmlinuz-6.8.0-interval-vm-debug+
sudo rm -rf /lib/modules/6.8.0-interval-vm-debug+
