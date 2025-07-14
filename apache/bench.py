import subprocess
import sys
import time
import re
import statistics
import os

def run_single_process(cpumax, repeat):
    CMD_TEMPLATE = "sudo CPUS={} ./run_single_process.sh"
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

             # Extract all occurrences of "Requests/sec:" and select the last one
            matches = re.findall(r"Requests/sec:\s*([0-9]*\.?[0-9]+)", result.stdout)
            if matches:
                thr = float(matches[-1])  # Select the last occurrence and convert to float
                thr_list.append(thr)
            else:
                print("Error: 'Requests/sec:' not found in the output.")
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

def run_default(repeat):
    CMD_TEMPLATE = "sudo ./run_default.sh"
    thr_list = []

    # Get the kernel version
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()

    for run in range(1, repeat + 1):
        print(f"Running with default config, run {run}")
        result = subprocess.run(CMD_TEMPLATE.split(), capture_output=True, text=True)

        # Extract all occurrences of "Requests/sec:" and select the last one
        matches = re.findall(r"Requests/sec:\s*([0-9]*\.?[0-9]+)", result.stdout)
        if matches:
            thr = float(matches[-1])  # Select the last occurrence and convert to float
            thr_list.append(thr)
        else:
            print("Error: 'Requests/sec:' not found in the output.")
            continue

        # Wait 5 seconds between runs
        time.sleep(5)

    # Calculate statistics
    if thr_list:
        thr = statistics.mean(thr_list)
        stdev_thr = statistics.stdev(thr_list) if len(thr_list) > 1 else 0
        rsd = stdev_thr / thr if thr != 0 else 0  # Relative standard deviation

        # Append results to CSV
        output_file = "results/default_results.csv"
        file_exists = os.path.isfile(output_file)

        with open(output_file, "a") as f:
            if not file_exists:
                f.write("kernel,throughput,rsd\n")
            f.write(f"{kernel_version},{thr},{rsd}\n")

        print(f"Results appended to {output_file}")
    else:
        print("No data collected.")

if __name__ == "__main__":
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    run_single_process(cpumax, repeat)
    run_default(repeat)
