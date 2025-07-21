KERNEL_VERSION=$(uname -r)
TARGET_DIR="results"

# 1. run w/o arena
sudo sysctl -w vm.interval_vm_ctl=8
sudo python3 bench.py
find "$TARGET_DIR" -type f -name "${KERNEL_VERSION}.*" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    new_name="${name}_no_arena.${ext}"
    mv "$file" "$dir/$new_name"
    echo "Renamed: $file -> $dir/$new_name"
done

# 2. run w/o percpu stats
sudo sysctl -w vm.interval_vm_ctl=16
sudo python3 bench.py
find "$TARGET_DIR" -type f -name "${KERNEL_VERSION}.*" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    new_name="${name}_no_percpu_stat.${ext}"
    mv "$file" "$dir/$new_name"
    echo "Renamed: $file -> $dir/$new_name"
done

# Clear interval_vm_ctl
sudo sysctl -w vm.interval_vm_ctl=0
