# Warmup
./obj/app/wrmem -s 4096 -p 64 > /dev/null
echo

for ncore in {1..2} {4..64..4}; do
    echo "cores: $ncore"
    ./obj/app/wrmem -s 4096 -p $ncore
    sleep 5
done
