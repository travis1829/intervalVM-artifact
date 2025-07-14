
if [ ! -d "linux-6.8" ]; then
    git clone --depth 1 --branch v6.8 git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git linux-6.8
    ./mkfiles linux-6.8 > linux-6.8-files.txt
fi

CPUS="${CPUS:-64}"

# Remove previous /tmp/db
sudo umount -f /tmp/db
rm -r -f /tmp/db
echo "rm /tmp/db done"

# Create /tmp/db
mkdir /tmp/db
sudo mount -t tmpfs none /tmp/db
for i in $(seq 0 $CPUS)
do
    mkdir /tmp/db/db"$i"
done
echo "/tmp/db created"

# Prefetch files
./prefetch -r linux-6.8
echo "prefetch done"


./mkdb/pedsort -t /tmp/db/db -c $CPUS -m 2048 < linux-6.8-files.txt


#Cleanup
sudo umount -f /tmp/db
rm -r -f /tmp/db
