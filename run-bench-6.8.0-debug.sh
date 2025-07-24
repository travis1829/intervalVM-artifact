KERNEL_VERSION=$(uname -r)

if [ "$KERNEL_VERSION" != "6.8.0-debug" ]; then
    echo "Error: Kernel version is not 6.8.0-debug (found $KERNEL_VERSION)"
    exit 1
fi

(cd lockstat && sudo python3 bench.py)
