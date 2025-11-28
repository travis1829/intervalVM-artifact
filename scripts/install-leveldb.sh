# about 6 minutes

cd ../leveldb
mkdir -p build && cd build
cmake -DCMAKE_BUILD_TYPE=Release .. && cmake --build .

# Create the db
./db_bench --db=./testdb_2M_4K --benchmarks=fillrandom --num=2000000 --value_size=4096
