# IntervalVM SOSP2025 Artifact

## Installation
Run
```
cd scripts && sudo ./install-all.sh
```
to install all required components (requires ~65 GiB of disk space). On our 48-core machine, this process takes about 1.5 hours and performs the following steps:
* Runs `install-packages.sh` to install required packages.
> Note: this script uses `apt-get` and is compatible only with Ubuntu/Debian. For other distributions, edit `install-packages.sh` to use the appropriate package manager.
* Runs `install-kernels.sh` to install the Linux kernels used in our evaluation. This script sequentially executes `install-linux-6.8.0.sh`, `install-linux-6.8.0-debug.sh`, `install-linux-ivm.sh`, and `install-linux-ivm-debug.sh`.
* Runs `install-benchmarks.sh` to install the benchmarks. This script sequentially executes `install-apache.sh`, `install-ds_benchmark.sh`, `install-lmbench.sh`, `install-metis.sh`, `install-microbench.sh`, and `install-psearchy.sh`.

Alternatively, you may also install components individually by running the corresponding scripts.

## Booting
To reproduce the figures in the paper, first boot into one of the newly installed kernels.

The following kernels are installed by `install-kernels.sh`:
* `Linux 6.8.0` — baseline
* `Linux 6.8.0-debug` — baseline with debug tools enabled
* `Linux 6.8.0-interval-vm+` — our customized kernel
* `Linux 6.8.0-interval-vm-debug+` — our customized kernel with debug tools enabled

On Ubuntu, simply run one of the `set-boot-kernel-as-*.sh` in `scripts` to set the default boot kernel, and then execute `sudo reboot`.
These scripts update `GRUB_DEFAULT` in `/etc/default/grub` and run `sudo update-grub`.

For other distributions, edit `/etc/default/grub` manually and add:
```
GRUB_TIMEOUT_STYLE=menu
GRUB_TIMEOUT=10   # Gives 10 seconds to choose
```

This enables selecting the desired kernel at boot.

## Running Benchmarks
After booting into one of the new kernels, run:
```
./run-bench.sh
```
This script automatically detects the current kernel and executes the required benchmarks to produce results for the figures.
See `run-bench.sh` for details.

Approximate runtime on our machine:
* `Linux 6.8.0` and `Linux 6.8.0-interval-vm+`: 24 hours
* `Linux 6.8.0-debug`: 12.5 hours
* `Linux 6.8.0-interval-vm-debug+`: 9 hours

Alternatively, you can run individual benchmarks by navigating to one of the benchmark directories (`apache`, `ds_benchmark`, `lmbench`, `lockstat`, `metis`, `microbench`, `psearchy`, `parsec-benchmark`) and executing:
```
sudo python3 bench.py
```

**Exception**: When booted with `Linux 6.8.0-interval-vm-debug+`, use:
```
sudo ./bench_debug.sh
```
instead of `sudo python3 bench.py`.
Note that this script is available only in the `apache` and `microbench` directories.

## Plotting the Results
After benchmarks complete, run:
```
python3 plot.py
```
in each benchmark directory to generate the plots as PDF files.

**Exception**: `lmbench` does not provide a `plot.py`. Instead, run:
```
python3 compare.py
```
to view results.

## Benchmark Descriptions
For each benchmark, we provide:
* a summary of its purpose,
* the kernels under which it should be run,
* the command to execute it,
* the runtime on our machine, and
* instructions for comparing the results with the figures in the paper.

All benchmark results are stored in the `results` directory within each benchmark's directory.

#### apache
* Evaluates Apache web server using wrk with two configurations: 1) single process, 2) default.
* Run under: `Linux 6.8.0`, `Linux 6.8.0-interval-vm+`, or `Linux 6.8.0-interval-vm-debug+`
* Command:
  - `sudo python3 bench.py` for `Linux 6.8.0` and `Linux 6.8.0-interval-vm+`
  - `sudo ./bench_debug.sh` for `Linux 6.8.0-interval-vm-debug+`
* Runtime: 2.5 hours for `bench.py`, 7 hours for `bench_debug.sh`
* Compare: `apache.pdf` to Fig. 15a, and `results/default_results.csv` to Fig. 15b.

#### ds_benchmark
* Evaluates data structures: maple tree (`mp`) and interval skiplist (`isl`) across operations (Query, Alloc, Map).
* Run under: `Linux 6.8.0`
* Command: `sudo python3 bench.py`
* Runtime: 1 hour
* Compare `latency.pdf` to Fig. 12a, and `Query.pdf`, `Alloc.pdf`, `Map.pdf` to Fig. 12b.

#### lmbench
* Runs the lmbench suite multiple times.
* Run under: `Linux 6.8.0` or `Linux 6.8.0-interval-vm+`
* Command: `sudo python3 bench.py`
* Runtime: 6 hours
* Compare the output of `python3 compare.py` to Fig. 13.

#### lockstat
* Runs apache, metis, and psearchy while using `lock_stat` to measure `wait time / total time`.
* Run under: `Linux 6.8.0-debug`
* Command: `sudo python3 bench.py`
* Runtime: 12.5 hours
* Compare `wasted_time_graph.pdf` to Fig. 1.

#### metis
* Evaluates Metis Map-Reduce with the `wrmem` benchmark (4GiB input).
* Run under: `Linux 6.8.0` or `Linux 6.8.0-interval-vm+`
* Command: `sudo python3 bench.py`
* Runtime: 3.5 hours
* Compare `metis.pdf` to Fig. 15c.

#### microbench
* Evaluates address space operations with microbenchmarks.
* Run under: `Linux 6.8.0`, `Linux 6.8.0-interval-vm+`, or `Linux 6.8.0-interval-vm-debug+`
* Command:
  - `sudo python3 bench.py` for `Linux 6.8.0` and `Linux 6.8.0-interval-vm+`
  - `sudo ./bench_debug.sh` for `Linux 6.8.0-interval-vm-debug+`
* Runtime: 1.5 hours for `bench.py`, 2 hours for `bench_debug.sh`
* Compare `Alloc.pdf` and `Alloc + Fault + Modify.pdf` to Fig. 14.

#### psearchy
* Evaluates text indexing using Psearchy on the `Linux 6.8.0` source tree.
* Run under: `Linux 6.8.0` or `Linux 6.8.0-interval-vm+`
* Command: `sudo python3 bench.py`
* Runtime: 5 hours
* Compare `psearchy.pdf` to Fig. 15d.

#### parsec-benchmark
* Evaluates the overall performance of various multithreaded applications.
* Run under: `Linux 6.8.0` or `Linux 6.8.0-interval-vm+`
* Command: `sudo python3 bench.py`
* Runtime: 4 hours
* Compare `parsec.pdf` to Fig. 16.

## Uninstall
Run:
```
cd scripts && sudo ./uninstall-all.sh
```

## Miscellaneous
Our artifact was evaluated in the following environment:

* **Motherboard:** Supermicro X11DPG-OT-CPU
* **CPU:** Dual-socket Intel Xeon Gold 6248R @ 3.0 GHz (48 cores)
* **Memory:** 384 GiB
* **OS:** Ubuntu 24.04.1 LTS

## License
This artifact is distributed under GPL-2.0, except where otherwise noted.
Some benchmarks are derived from prior benchmarks, which retain their original licenses.
Where applicable, those licenses are included in the artifact.
