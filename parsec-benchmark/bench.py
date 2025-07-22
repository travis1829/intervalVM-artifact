# < 4 hours (on e01)

import subprocess
import sys
import time
import re
import statistics
import os
import psutil # For psutil.cpu_count()

# Benchmarks that can run with any number of threads
CMD = [
    ("blackscholes", "sudo ./bin/parsecmgmt -a run -p blackscholes -i native -n {}"),
    ("bodytrack", "sudo ./bin/parsecmgmt -a run -p bodytrack -i native -n {}"),
    ("canneal", "sudo ./bin/parsecmgmt -a run -p canneal -i native -n {}"),
    ("dedup", "sudo ./bin/parsecmgmt -a run -p dedup -i simlarge -n {}"), # Use simlarge instead of native since native has almost nothing to dedup
    ("ferret", "sudo ./bin/parsecmgmt -a run -p ferret -i native -n {}"),
    ("freqmine", "sudo ./bin/parsecmgmt -a run -p freqmine -i native -n {}"),
    ("raytrace", "sudo ./bin/parsecmgmt -a run -p raytrace -i native -n {}"),
    ("streamcluster", "sudo ./bin/parsecmgmt -a run -p streamcluster -i native -n {}"),
    ("swaptions", "sudo ./bin/parsecmgmt -a run -p swaptions -i native -n {}"),
    ("vips", "sudo ./bin/parsecmgmt -a run -p vips -i native -n {}"),
    ("x264", "sudo ./bin/parsecmgmt -a run -p x264 -i native -n {}"),
]

# Benchmarks that require the number of threads to be a power of 2
CMD_POWER_2 = [
    ("facesim", "sudo ./bin/parsecmgmt -a run -p facesim -i native -n {}"),
    ("fluidanimate", "sudo ./bin/parsecmgmt -a run -p fluidanimate -i native -n {}"),
]


def run_single(cmd_name, cmd_template, ncore, repeat):
    # Run a warm-up to reduce initial latency variations
    warmup_cmd = cmd_template.format(ncore)
    subprocess.run(warmup_cmd.split(), stdout=subprocess.DEVNULL)

    res_list = []
    for run in range(1, repeat + 1):
        print(f"Running {cmd_name}, run {run}")
        cmd = cmd_template.format(ncore)
        result = subprocess.run(cmd.split(), capture_output=True, text=True)

        matches = re.findall(r"real\s+(\d+)m([\d.]+)s", result.stdout)
        if not matches:
            print("Error: 'real:' not found in the output.")
            continue
        minutes, seconds = matches[-1]
        total_seconds = int(minutes) * 60 + float(seconds)
        res_list.append(total_seconds)

        # Wait 5 seconds between runs
        time.sleep(5)

    # Calculate statistics for benchmark
    total_seconds = statistics.mean(res_list) if len(res_list) else 0
    stdev = statistics.stdev(res_list) if len(res_list) > 1 else 0
    rsd = stdev / total_seconds if total_seconds != 0 else 0
    return (ncore, total_seconds, stdev, rsd)

def run_benchmark(cpumax, repeat):
    results = {}

    # Get the kernel version for the output filename
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()
    output_filename = f"results/{kernel_version}.csv"

    for (cmd_name, cmd_template) in CMD:
        results[cmd_name] = run_single(cmd_name, cmd_template, cpumax, repeat)
    cpumax_reduced_to_power_of_two = 1 << (cpumax.bit_length() - 1)
    for (cmd_name, cmd_template) in CMD_POWER_2:
        results[cmd_name] = run_single(cmd_name, cmd_template, cpumax_reduced_to_power_of_two, repeat)

    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("benchmark,cores,real,stdev,rsd\n")
        for benchmark, (cores, real, stdev, rsd) in results.items():
            f.write(f"{benchmark},{cores},{real},{stdev},{rsd}\n")

    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else psutil.cpu_count(logical=False) or 32
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    run_benchmark(cpumax, repeat)
