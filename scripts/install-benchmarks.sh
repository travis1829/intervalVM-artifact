# about 25 minutes

./install-packages.sh

if [ ! -d "/usr/local/apache2" ]; then
    ./install-apache.sh
fi
./install-ds_benchmark.sh
./install-lmbench.sh
./install-metis.sh
./install-microbench.sh
./install-psearchy.sh
./install-parsec-benchmark.sh
