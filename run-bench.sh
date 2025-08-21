# Checks the kernel version and runs the corresponding benchmarks

KERNEL_VERSION=$(uname -r)

if [ "$KERNEL_VERSION" != "6.8.0" ] && [ "$KERNEL_VERSION" != "6.8.0-debug" ] && [ "$KERNEL_VERSION" != "6.8.0-interval-vm+" ] && [ "$KERNEL_VERSION" != "6.8.0-interval-vm-debug+" ]; then
  echo "Error: Kernel version is not one of 6.8.0, 6.8.0-debug, 6.8.0-interval-vm+, or 6.8.0-interval-vm-debug+ (found $KERNEL_VERSION)"
  exit 1
fi

if [ "$KERNEL_VERSION" = "6.8.0" ]; then
  for dir in ds_benchmark apache lmbench metis microbench psearchy parsec-benchmark; do
    (cd "$dir" && sudo python3 bench.py)
  done
fi

if [ "$KERNEL_VERSION" = "6.8.0-interval-vm+" ]; then
  for dir in apache lmbench metis microbench psearchy parsec-benchmark; do
    (cd "$dir" && sudo python3 bench.py)
  done
fi

if [ "$KERNEL_VERSION" = "6.8.0-debug" ]; then
  (cd lockstat && sudo python3 bench.py)
fi

if [ "$KERNEL_VERSION" = "6.8.0-interval-vm-debug+" ]; then
  for dir in apache microbench; do
    (cd "$dir" && sudo ./bench_debug.sh)
  done
fi
