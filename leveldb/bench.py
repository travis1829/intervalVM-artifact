import subprocess
import sys
import time
import re
import statistics
import os

# CMD_TEMPLATE = "./build/db_bench --db=./build/testdb_2M_4K --benchmarks=readrandom --num=2000000 --value_size=4096 --use_existing_db=1 --threads={}"
CMD_TEMPLATE = "./build/db_bench --db=./build/testdb_2M_4K --benchmarks=readrandomsmall --num=2000000 --value_size=4096 --use_existing_db=1 --threads={}"


def run_benchmark(cpumax, repeat):
    results = {}
    core_counts = list(range(1, 3)) + list(range(4, cpumax + 1, 4))

    # Get the kernel version for the output filename
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()
    output_filename = f"results/{kernel_version}.csv"

    # Run a warm-up to reduce initial latency variations
    warmup_cmd = CMD_TEMPLATE.format(cpumax)
    subprocess.run(warmup_cmd.split(), stdout=subprocess.DEVNULL)

    for ncore in core_counts:
        thr_list = []
        for run in range(1, repeat + 1):
            print(f"Running with {ncore} cores, run {run}")
            cmd = CMD_TEMPLATE.format(ncore)
            result = subprocess.run(cmd.split(), capture_output=True, text=True)

             # Extract all occurrences of "micros/op;" and select the last one
            matches = re.findall(r"([0-9]*\.?[0-9]+)\s+micros/op;", result.stdout)
            if matches:
                lat = float(matches[-1])  # Select the last occurrence and convert to float
                thr = 1000 * 1000 / lat * ncore
                thr_list.append(thr)
            else:
                print("Error: 'micros/op;' not found in the output.")
                continue

            # Wait 5 seconds between runs
            time.sleep(5)

        # Calculate statistics for the current core count
        if thr_list:
            thr = statistics.mean(thr_list)
            stdev_thr = statistics.stdev(thr_list) if len(thr_list) > 1 else 0
            rsd = stdev_thr / thr if thr != 0 else 0  # Relative standard deviation

            results[ncore] = (thr, rsd)

    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("cores,throughput,rsd\n")
        for ncore, (thr, rsd) in results.items():
            f.write(f"{ncore},{thr},{rsd}\n")
    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 5 # TODO: Should use 20, but 20 takes extremely long on Linux 6.8.0.
    
    run_benchmark(cpumax, repeat)
