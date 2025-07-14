# about 12 minutes

# Creates a .config file based on the current running kernel's .config file,
# and installs the kernel based on the .config file.
# This is for Linux 6.8.0 with interval_vm and debug options (CONFIG_LOCK_STAT, CONFIG_INTERVAL_VM_CTL) enabled.
# Note that this causes some runtime overhead.

LINUX="../linux-6.8-interval_vm"
if [ ! -d $LINUX ]; then
    cat ../linux-6.8-interval_vm.tar.gz* | tar zxf - -C ..
fi
cd $LINUX

# Copy the current running kernel's .config file (/boot/config-$(uname -r)).
cp -v /boot/config-$(uname -r) .config

# The following is necessary on some distros.
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS

# Set local name as "-interval-vm-debug"
NEW_VERSION="-interval-vm-debug"
if grep -q '^CONFIG_LOCALVERSION=' ".config"; then
  sed -i "s|^CONFIG_LOCALVERSION=.*|CONFIG_LOCALVERSION=\"$NEW_VERSION\"|" ".config"
  echo "Updated CONFIG_LOCALVERSION to \"$NEW_VERSION\"."
else
  echo "CONFIG_LOCALVERSION=\"$NEW_VERSION\"" >> ".config"
  echo "Added CONFIG_LOCALVERSION=\"$NEW_VERSION\" to $CONFIG_FILE."
fi

# Add the git hash tag.
# sed -i 's/^# CONFIG_LOCALVERSION_AUTO is not set$/CONFIG_LOCALVERSION_AUTO=y/' ".config"

# Disable `CONFIG_PER_VMA_LOCK`, as we want to use `CONFIG_INTERVAL_VM` instead.
sed -i 's/^CONFIG_PER_VMA_LOCK=y$/# CONFIG_PER_VMA_LOCK is not set/' ".config"

# Enable `CONFIG_LOCK_STAT`
sed -i 's/^# CONFIG_LOCK_STAT is not set$/CONFIG_LOCK_STAT=y/' ".config"
if ! grep -q '^CONFIG_LOCK_STAT=y' ".config"; then
  echo "CONFIG_LOCK_STAT=y" >> ".config"
  echo "Added CONFIG_LOCK_STAT=y to $CONFIG_FILE."
fi

# Enable `CONFIG_CONCURRENT_MMAP_STATS`
sed -i 's/^# CONFIG_CONCURRENT_MMAP_STATS is not set$/CONFIG_CONCURRENT_MMAP_STATS=y/' ".config"
if ! grep -q '^CONFIG_CONCURRENT_MMAP_STATS=y' ".config"; then
  echo "CONFIG_CONCURRENT_MMAP_STATS=y" >> ".config"
  echo "Added CONFIG_CONCURRENT_MMAP_STATS=y to $CONFIG_FILE."
fi

# Enable `CONFIG_INTERVAL_VM_CTL`
sed -i 's/^# CONFIG_INTERVAL_VM_CTL is not set$/CONFIG_INTERVAL_VM_CTL=y/' ".config"
if ! grep -q '^CONFIG_INTERVAL_VM_CTL=y' ".config"; then
  echo "CONFIG_INTERVAL_VM_CTL=y" >> ".config"
  echo "Added CONFIG_INTERVAL_VM_CTL=y to $CONFIG_FILE."
fi

# Auto update the config file.
yes "" | make oldconfig

# Test the config file.
if ! grep -q "^CONFIG_SHARDED_MMAP_LOCK=y$" ".config"; then
  echo "error: CONFIG_SHARDED_MMAP_LOCK=y is NOT present in .config. Aborting."
  exit 1
fi
if ! grep -q "^CONFIG_INTERVAL_VM=y$" ".config"; then
  echo "error: CONFIG_INTERVAL_VM=y is NOT present in .config. Aborting."
  exit 1
fi
if ! grep -q "^CONFIG_LOCK_STAT=y$" ".config"; then
  echo "error: CONFIG_LOCK_STAT=y is NOT present in .config. Aborting."
  exit 1
fi
if ! grep -q "^CONFIG_CONCURRENT_MMAP_STATS=y$" ".config"; then
  echo "error: CONFIG_CONCURRENT_MMAP_STATS=y is NOT present in .config. Aborting."
  exit 1
fi
if ! grep -q "^CONFIG_INTERVAL_VM_CTL=y$" ".config"; then
  echo "error: CONFIG_INTERVAL_VM_CTL=y is NOT present in .config. Aborting."
  exit 1
fi

cp -v .config .config.ivm-debug

# Compile the kernel.
make -j $(nproc)

# Install modules.
sudo make modules_install

# Install kernel.
sudo make install
