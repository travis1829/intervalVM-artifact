KERNEL_VERSION=$(uname -r)

if [ "$KERNEL_VERSION" != "6.8.0" ] && [ "$KERNEL_VERSION" != "6.8.0-interval-vm+" ]; then
    echo "Error: Kernel version is not 6.8.0 or 6.8.0-interval-vm+ (found $KERNEL_VERSION)"
    exit 1
fi

for dir in apache ds_benchmark lmbench metis microbench psearchy; do
  (cd "$dir" && sudo python3 bench.py)
done
