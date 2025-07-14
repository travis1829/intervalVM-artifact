# Creates a .config file based on the current running kernel's .config file,
# and installs the kernel based on the .config file.
# This is for Linux 6.8.0.

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

# Auto update the config file.
yes "" | make oldconfig

cp -v .config .config.6.8.0

# Compile the kernel.
make -j $(nproc)

# Install modules.
sudo make modules_install

# Install kernel.
sudo make install
