import os
import subprocess
import sys
import time
import re
import statistics

MBENCH = ("./mbench {}", "mbench")
MFMBENCH = ("./mfmbench {}", "mfmbench")
F_MBENCH = ("./f_mbench {}", "f_mbench")
F_MFMBENCH = ("./f_mfmbench {}", "f_mfmbench")

MAX_MAP_COUNT = 4194304

def run_single(command, cpumax, repeat):
    results = {}
    core_counts = list(range(1, 3)) + list(range(4, cpumax + 1, 4))

    # Get the kernel version for the output filename
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()
    output_filename = f"results/{command[1]}/{kernel_version}.csv"

    # Run a warm-up to reduce initial latency variations
    warmup_cmd = command[0].format(cpumax)
    subprocess.run(warmup_cmd.split(), stdout=subprocess.DEVNULL)

    for ncore in core_counts:
        thr_list = []
        for run in range(1, repeat + 1):
            print(f"Running with {ncore} cores, run {run}")

            # Fill in `ncore` into the command template
            cmd = command[0].format(ncore)
            # Run the benchmark command and capture the output
            result = subprocess.run(cmd.split(), capture_output=True, text=True)

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

def change_max_map_count(value):
    try:
        # Get the current value
        result = subprocess.run(
            ["sudo", "sysctl", "vm.max_map_count"],
            check=True,
            capture_output=True,
            text=True
        )
        # Parse the output like: 'vm.max_map_count = 65530'
        old_value = int(result.stdout.strip().split("=")[1])

        # Set the new value
        subprocess.run(
            ["sudo", "sysctl", f"vm.max_map_count={value}"],
            check=True
        )

        print(f"vm.max_map_count changed from {old_value} to {value}")
        return old_value

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to run sysctl: {e}")

def run_all(cpumax, repeat):
    # Temporarily increase vm.max_map_count, because we're going to mmap() a lot.
    old_max_map_count = change_max_map_count(MAX_MAP_COUNT)

    run_single(MBENCH, cpumax, repeat)
    run_single(MFMBENCH, cpumax, repeat)
    run_single(F_MBENCH, cpumax, repeat)
    run_single(F_MFMBENCH, cpumax, repeat)

    change_max_map_count(old_max_map_count)

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    run_all(cpumax, repeat)
