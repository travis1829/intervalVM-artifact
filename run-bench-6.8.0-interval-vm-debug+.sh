KERNEL_VERSION=$(uname -r)

if [ "$KERNEL_VERSION" != "6.8.0-interval-vm-debug+" ]; then
    echo "Error: Kernel version is not 6.8.0-interval-vm-debug+ (found $KERNEL_VERSION)"
    exit 1
fi

for dir in apache microbench; do
  (cd "$dir" && sudo ./bench_debug.sh)
done
