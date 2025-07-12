import subprocess
import sys
import time
import re
import statistics
import os

# CMD template with placeholder for core count
CMD_TEMPLATE = "sudo CPUS={} ./run.sh"

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

            # Fill in `ncore` into the command template
            cmd = CMD_TEMPLATE.format(ncore)
            # Run the benchmark command and capture the output
            result = subprocess.run(cmd.split(), capture_output=True, text=True)

             # Extract all occurrences of "throughput:" and select the last one
            matches = re.findall(r"throughput:\s*([0-9]*\.?[0-9]+)", result.stdout)
            if matches:
                thr = float(matches[-1])  # Select the last occurrence and convert to float
                thr_list.append(thr)
            else:
                print("Error: 'cycles:' not found in the output.")
                continue

            # Wait 5 seconds between runs
            time.sleep(5)

        # Calculate statistics for the current core count
        if thr_list:
            percore_thr = statistics.mean(thr_list)
            stdev_thr = statistics.stdev(thr_list) if len(thr_list) > 1 else 0
            rsd = stdev_thr / percore_thr if percore_thr != 0 else 0  # Relative standard deviation
            total_thr = (percore_thr * ncore) if percore_thr != 0 else 0    # Throughput (MiB/s)

            results[ncore] = (percore_thr, rsd, total_thr)

    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("cores,percore_throughtput,rsd,throughput\n")
        for ncore, (percore_thr, rsd, throughput) in results.items():
            f.write(f"{ncore},{percore_thr},{rsd},{throughput}\n")

    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    run_benchmark(cpumax, repeat)
