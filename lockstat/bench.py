
import subprocess, time
import sys
import statistics
import os

# (command name, command template)
APACHE = ("apache", "cd ../apache && sudo CPUS={} ./run_single_process.sh")
METIS_WRMEM = ("metis", "../metis/obj/app/wrmem -s 4096 -p {}")
PSEARCHY_MKDB = ("psearchy", "cd ../psearchy && sudo CPUS={} ./run.sh")

def read_lock_stat(verbose = False):
    mmap_lock_w = -1
    mmap_lock_r = -1
    n_lines = 0
    NUM_PRINT_LINES = 20

    with open("/proc/lock_stat", "r") as f:
        lines = f.readlines()
    if verbose:
        print("lock_stat:")
    for line in lines:
        if ":" not in line:
            continue
        tokens = line.split()
        if len(tokens) >= 6:
            if verbose and n_lines < NUM_PRINT_LINES:
                print(tokens[0], tokens[2], tokens[5], sep = "\t")
                n_lines += 1
            # Read value for old mmap_lock / mmap_lock / sharded mmap_lock
            if tokens[0] in ("&mm->mmap_lock-W:", "&mm->mmap_lock#2-W:", "&lock->locks[i].rwsem-W:"):
                mmap_lock_w = float(tokens[5])
            elif tokens[0] in ("&mm->mmap_lock-R:", "&mm->mmap_lock#2-R:", "&lock->locks[i].rwsem-R:"):
                mmap_lock_r = float(tokens[5])

    if verbose:
        print("\n\n")
    if mmap_lock_w < 0 or mmap_lock_r < 0:
        print("Warning: mmap_lock stats not found. Did you enable lock statistics?")
    return (mmap_lock_w, mmap_lock_r)

def read_islo_waittime(verbose = False):
    with open("/proc/vmstat", "r") as f:
        lines = f.readlines()
    for line in lines:
        tokens = line.split()
        if tokens[0] == "islo_waittime_nsec":
            if verbose:
               print(line)
            return float(tokens[1]) / 1000
    if verbose:
        print("islo_waittime_nsec not found.")
    return 0.0

def single_run(cmd_template, threads, verbose = False):
    subprocess.call("echo 1 > /proc/sys/kernel/lock_stat", shell=True)
    if verbose:
        print("running ", cmd_template.format(threads))
    subprocess.call("echo 0 > /proc/lock_stat", shell=True)
    islo_waittime = read_islo_waittime(verbose)
    begin = time.perf_counter()
    process = subprocess.run(cmd_template.format(threads), stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    end = time.perf_counter()
    islo_waittime = read_islo_waittime(verbose) - islo_waittime

    if verbose:
        print(process.stdout)
        print("\n")

    (mmap_lock_w, mmap_lock_r) = read_lock_stat(verbose)

    if cmd_template in (METIS_WRMEM[1]):
        tokens = process.stdout.split()
        for i in range(len(tokens)):
            if tokens[i] == "Real:":
                real = int(tokens[i+1]) * 1000
                total = real * threads
                break
    else:
        real = (end - begin) * 1000 * 1000
        total = real * threads
    ratio = (mmap_lock_w + mmap_lock_r + islo_waittime) / total
    
    if verbose:
        print("real: ", real)
        print("mmap_lock_w: ", mmap_lock_w)
        print("mmap_lock_r: ", mmap_lock_r)
        print("mmap_lock (sum): ", mmap_lock_w + mmap_lock_r)
        print("islo_waittime: ", islo_waittime)
        print("total (real*threads): ", total)
        print("ratio ((mmap_lock + islo_waittime)/total): ", ratio)
        print("\n\n")
    return (ratio, real, total)

def run(cmd_name, cmd_template, cpumax, repeat, verbose = False):
    results = {}
    core_counts = list(range(1, 3)) + list(range(4, cpumax + 1, 4))

    # Get the kernel version for the output filename
    kernel_version = subprocess.run(["uname", "-r"], capture_output=True, text=True).stdout.strip()
    output_filename = f"results/{cmd_name}_{kernel_version}.csv"

    for ncore in core_counts:
        ratio_list = []
        real_list = []
        total_list = []
        for run in range(1, repeat + 1):
            print(f"Running with {ncore} cores, run {run}")
            (ratio, real, total) = single_run(cmd_template, ncore, verbose)
            ratio_list.append(ratio)
            real_list.append(real)
            total_list.append(total)

            # Wait 5 seconds between runs
            time.sleep(5)

        # Calculate statistics for the current core count
        ratio = statistics.mean(ratio_list)
        real = statistics.mean(real_list)
        total = statistics.mean(total_list)
        results[ncore] = (ratio, real, total)
    
    # Write results to CSV file
    with open(output_filename, "w") as f:
        f.write("threads,ratio,real,total\n")
        for ncore, (ratio, real, total) in results.items():
            f.write(f"{ncore},{ratio},{real},{total}\n")

    print(f"Results saved to {output_filename}")

if __name__ == "__main__":
    # Set default values if arguments are not provided
    cpumax = int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count() or 64
    repeat = int(sys.argv[2]) if len(sys.argv) > 2 else 20

    for cmd in [APACHE, METIS_WRMEM, PSEARCHY_MKDB]:
        run(cmd[0], cmd[1], cpumax, repeat)
