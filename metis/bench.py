import subprocess
import sys
import time
import re
import statistics
import os

# CMD template with placeholder for core count
CMD_TEMPLATE = "./obj/app/wrmem -s 4096 -p {}"

def read_cpuinfo_max_freq():
    path = "/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq"
    try:
        with open(path, "r") as f:
            value = f.read().strip()
            return int(value)*1000
    except FileNotFoundError:
        raise RuntimeError(f"{path} does not exist")
    except ValueError:
        raise RuntimeError(f"Could not parse integer from {path}")

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
        cycles_list = []
        for run in range(1, repeat + 1):
            print(f"Running with {ncore} cores, run {run}")

            # Fill in `ncore` into the command template
            cmd = CMD_TEMPLATE.format(ncore)
            # Run the benchmark command and capture the output
            result = subprocess.run(cmd.split(), capture_output=True, text=True)

            # Extract the number of cycles from the output
            match = re.search(r"cycles:\s*(\d+)", result.stdout)
            if match:
                cycles = int(match.group(1))
                cycles_list.append(cycles)
            else:
                print("Error: 'cycles:' not found in the output.")
                continue

            # Wait 5 seconds between runs
            time.sleep(5)

        # Calculate statistics for the current core count
        if cycles_list:
            avg_cycles = statistics.mean(cycles_list)
            stdev_cycles = statistics.stdev(cycles_list) if len(cycles_list) > 1 else 0
            rsd = stdev_cycles / avg_cycles if avg_cycles != 0 else 0  # Relative standard deviation
            throughput = 4096 / (avg_cycles / read_cpuinfo_max_freq()) if avg_cycles != 0 else 0    # Throughput (MiB/s)

            results[ncore] = (avg_cycles, rsd, throughput)

    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("cores,average_cycles,rsd,throughput\n")
        for ncore, (avg_cycles, rsd, throughput) in results.items():
            f.write(f"{ncore},{avg_cycles},{rsd},{throughput}\n")

    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    run_benchmark(cpumax, repeat)
