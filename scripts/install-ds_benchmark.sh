if ! jemalloc-config --libdir; then
    git clone --depth 1 --branch 5.3.0 https://github.com/jemalloc/jemalloc.git
    cd jemalloc
    ./autogen.sh
    make
    sudo make install
    cd ..
fi

LINUX="../linux-6.8-interval_vm"
if [ ! -d $LINUX ]; then
    cat ../linux-6.8-interval_vm.tar.gz* | tar zxf - -C ..
fi
cd $LINUX

make -C tools/testing/radix-tree