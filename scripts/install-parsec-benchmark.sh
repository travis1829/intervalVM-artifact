
PARSEC="../parsec-benchmark"

cd $PARSEC
./configure
./bin/parsecmgmt -a build -p all
./get-inputs -n
