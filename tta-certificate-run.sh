KERNEL_VERSION=$(uname -r)
if [ "$KERNEL_VERSION" != "6.8.0-debug" ] && [ "$KERNEL_VERSION" != "6.8.0-interval-vm-debug+" ]; then
    echo "Error: Kernel version is not 6.8.0 or 6.8.0-interval-vm-debug+ (found $KERNEL_VERSION)"
    exit 1
fi

# Run benchmark

cd lockstat
sudo python3 bench.py
python3 plot.py
