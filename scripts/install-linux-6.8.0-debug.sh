# Creates a .config file based on the current running kernel's .config file,
# and installs the kernel based on the .config file.
# This is for Linux 6.8.0 with debug options (CONFIG_LOCK_STAT) enabled.
# Note that this causes some runtime overhead.

LINUX="../linux-6.8"
if [ ! -d $LINUX ]; then
    git clone --depth 1 --branch v6.8 git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git ../linux-6.8
fi
cd $LINUX

# Copy the current running kernel's .config file (/boot/config-$(uname -r)).
cp -v /boot/config-$(uname -r) .config

# The following is necessary on some distros.
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS

# Set local name as "-debug"
NEW_VERSION="-debug"
if grep -q '^CONFIG_LOCALVERSION=' ".config"; then
  sed -i "s|^CONFIG_LOCALVERSION=.*|CONFIG_LOCALVERSION=\"$NEW_VERSION\"|" ".config"
  echo "Updated CONFIG_LOCALVERSION to \"$NEW_VERSION\"."
else
  echo "CONFIG_LOCALVERSION=\"$NEW_VERSION\"" >> ".config"
  echo "Added CONFIG_LOCALVERSION=\"$NEW_VERSION\" to $CONFIG_FILE."
fi

# Enable `CONFIG_LOCK_STAT`
sed -i 's/^# CONFIG_LOCK_STAT is not set$/CONFIG_LOCK_STAT=y/' ".config"
if ! grep -q '^CONFIG_LOCK_STAT=y' ".config"; then
  echo "CONFIG_LOCK_STAT=y" >> ".config"
  echo "Added CONFIG_LOCK_STAT=y to $CONFIG_FILE."
fi

# Auto update the config file.
yes "" | make oldconfig

# Test the config file.
if ! grep -q "^CONFIG_LOCK_STAT=y$" ".config"; then
  echo "error: CONFIG_LOCK_STAT=y is NOT present in .config. Aborting."
  exit 1
fi

cp -v .config .config.6.8.0-debug

# Compile the kernel.
make -j $(nproc)

# Install modules.
sudo make modules_install

# Install kernel.
sudo make install
