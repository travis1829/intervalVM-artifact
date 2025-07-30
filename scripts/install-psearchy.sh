# about 7 minutes

make -C ../psearchy

cd ../psearchy
if [ ! -d "/linux-6.8" ]; then
    git clone --depth 1 --branch v6.8 git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git linux-6.8
    ./mkfiles linux-6.8 > linux-6.8-files.txt
fi
