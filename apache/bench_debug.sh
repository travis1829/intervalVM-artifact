# Runs bench.py multiple times with different vm.interval_vm_ctl configurations.

KERNEL_VERSION=$(uname -r)
TARGET_DIR="results"
TARGET_FILE="results/default_results.csv"

# 1. run w/o parallelized faults
sudo sysctl -w vm.interval_vm_ctl=3
sudo python3 bench.py
find "$TARGET_DIR" -type f -name "${KERNEL_VERSION}.*" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    new_name="${name}_no_fault.${ext}"
    mv "$file" "$dir/$new_name"
    echo "Renamed: $file -> $dir/$new_name"
done
if [ -f "$TARGET_FILE" ]; then
    sed -i "s/${KERNEL_VERSION},/${KERNEL_VERSION}_no_fault,/g" "$TARGET_FILE"
fi

# 2. run w/o parallelized alloc
sudo sysctl -w vm.interval_vm_ctl=4
sudo python3 bench.py
find "$TARGET_DIR" -type f -name "${KERNEL_VERSION}.*" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    new_name="${name}_no_alloc.${ext}"
    mv "$file" "$dir/$new_name"
    echo "Renamed: $file -> $dir/$new_name"
done
if [ -f "$TARGET_FILE" ]; then
    sed -i "s/${KERNEL_VERSION},/${KERNEL_VERSION}_no_alloc,/g" "$TARGET_FILE"
fi

# 2. run w/o parallelized modify
sudo sysctl -w vm.interval_vm_ctl=480
sudo python3 bench.py
find "$TARGET_DIR" -type f -name "${KERNEL_VERSION}.*" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    name="${base%.*}"
    ext="${base##*.}"

    new_name="${name}_no_modify.${ext}"
    mv "$file" "$dir/$new_name"
    echo "Renamed: $file -> $dir/$new_name"
done
if [ -f "$TARGET_FILE" ]; then
    sed -i "s/${KERNEL_VERSION},/${KERNEL_VERSION}_no_modify,/g" "$TARGET_FILE"
fi

# Restore sysctl
sudo sysctl -w vm.interval_vm_ctl=0
