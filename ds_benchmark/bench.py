import subprocess
import sys
import time
import re
import statistics
import os

JEMALLOC_LIB = subprocess.run(
    "jemalloc-config --libdir", shell=True, capture_output=True, text=True
).stdout.strip()
JEMALLOC_REV = subprocess.run(
    "jemalloc-config --revision", shell=True, capture_output=True, text=True
).stdout.strip()
LD_PRELOAD_PATH = f"{JEMALLOC_LIB}/libjemalloc.so.{JEMALLOC_REV}"

ISL_ALLOC = ("../linux-6.8-interval_vm/tools/testing/radix-tree/islist {} 0", "alloc", "isl")
ISL_FIND = ("../linux-6.8-interval_vm/tools/testing/radix-tree/islist {} 1", "find", "isl")
ISL_REMOVE = ("../linux-6.8-interval_vm/tools/testing/radix-tree/islist {} 2", "remove", "isl")
MP_ALLOC = ("../linux-6.8-interval_vm/tools/testing/radix-tree/maple_b {} 0", "alloc", "mp")
MP_FIND = ("../linux-6.8-interval_vm/tools/testing/radix-tree/maple_b {} 1", "find", "mp")
MP_REMOVE = ("../linux-6.8-interval_vm/tools/testing/radix-tree/maple_b {} 2", "remove", "mp")

def run_single(command, cpumax, repeat):
    results = {}
    core_counts = list(range(1, 3)) + list(range(4, cpumax + 1, 4))

    output_filename = f"results/{command[1]}/{command[2]}.csv"

    # Set environment variable correctly
    env = os.environ.copy()
    env["LD_PRELOAD"] = LD_PRELOAD_PATH

    # Run a warm-up to reduce initial latency variations
    warmup_cmd = command[0].format(cpumax)
    subprocess.run(warmup_cmd.split(), stdout=subprocess.DEVNULL, env=env)

    for ncore in core_counts:
        thr_list = []
        for run in range(1, repeat + 1):
            print(f"Running with {ncore} cores, run {run}")

            # Fill in `ncore` into the command template
            cmd = command[0].format(ncore)
            # Run the benchmark command and capture the output
            result = subprocess.run(cmd.split(), capture_output=True, text=True, env=env)

            # Check if "error" appears in the output (case insensitive)
            if re.search(r"error", result.stdout) or re.search(r"error", result.stderr):
                print("Warning: Detected 'error' in output (run {run} with {ncore} cores):")
                print(result.stdout)
                print(result.stderr)

            # Extract the number of thr from the output
            match = re.search(r"throughput:\s*(\d+)", result.stdout)
            if match:
                thr = int(match.group(1))
                thr_list.append(thr)
            else:
                print("Error: 'throughput:' not found in the output.")
                continue

            # Wait 5 seconds between runs
            time.sleep(1)

        # Calculate statistics for the current core count
        if thr_list:
            avg_thr = statistics.mean(thr_list)
            stdev_thr = statistics.stdev(thr_list) if len(thr_list) > 1 else 0
            rsd = stdev_thr / avg_thr if avg_thr != 0 else 0  # Relative standard deviation

            results[ncore] = (avg_thr, rsd)

    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("cores,throughput,rsd\n")
        for ncore, (avg_thr, rsd) in results.items():
            f.write(f"{ncore},{avg_thr},{rsd}\n")

    print(f"Results saved to {output_filename}")

def run_all(cpumax=64, repeat=5):
    run_single(ISL_ALLOC, cpumax, repeat)
    run_single(ISL_FIND, cpumax, repeat)
    run_single(ISL_REMOVE, cpumax, repeat)
    run_single(MP_ALLOC, cpumax, repeat)
    run_single(MP_FIND, cpumax, repeat)
    run_single(MP_REMOVE, cpumax, repeat)

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    run_all(cpumax, repeat)
