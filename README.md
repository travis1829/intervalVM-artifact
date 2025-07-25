

### Installation
Run `cd scripts && sudo ./install-all.sh` to install everything. This does the following:
* Runs `install-packages.sh`, which installs the required packages. Note that this uses `apt-get`, and therefore, only works on ubuntu/debian. On other distros, please edit `install-packages.sh` to use your own package manager.
* Runs `install-kernels.sh`, which installs the Linux kernels needed for evaluation. This simply runs `install-linux-6.8.0.sh`, `install-linux-6.8.0-debug.sh`, `install-linux-ivm.sh`, and `install-linux-ivm-debug.sh` to install each kernel.
* Runs `install-benchmarks.sh`, which installs the benchmarks. This simply runs `install-apache.sh`, `install-ds_benchmark.sh`, `install-lmbench.sh`, `install-metis.sh`, `install-microbench.sh`, and `install-psearchy.sh` to install each benchmark.

Alternatively, you can individually install the components you want by running each script individually.

### Booting
To replicate the figures in our paper, you need to first boot with one of the newly installed kernels.

The following are the list of kernels installed by `install-kernels.sh`.
* `Linux 6.8.0` (baseline)
* `Linux 6.8.0-debug` (baseline with debug tools enabled)
* `Linux 6.8.0-interval-vm+` (our customized kernel)
* `Linux 6.8.0-interval-vm-debug+` (our customized kernel with debug tools enabled)

On ubuntu, simply run one of the `set-boot-kernel-as-*.sh` in `scripts` to change the default boot kernel, and then run `sudo reboot` to reboot with it.
These simply update the `GRUB_DEFAULT` in `/etc/default/grub` and run `sudo update-grub`.

On other distros, please manually edit `/etc/default/grub` and add the following lines.
* `GRUB_TIMEOUT_STYLE=menu`
* `GRUB_TIMEOUT=10   # Gives 10 seconds to choose`

This will allow you to choose a kernel at boot.

### Running Benchmarks
After booting with one of the new kernels, run the script corresponding to each kernel to run the benchmarks.
* For `Linux 6.8.0` and `Linux 6.8.0-interval-vm+`, use `run-bench.sh`.
* For `Linux 6.8.0-debug`, use `run-bench-6.8.0-debug.sh`.
* For `Linux 6.8.0-interval-vm-debug+`, use `run-bench-interval-vm-debug+.sh`.

Alternatively, you can go to one of the benchmark directories (`apache`, `ds_benchmark`, `lmbench`, `lockstat`, `metis`, `microbench`, `psearchy`) and run `sudo python3 bench.py` to run each benchmark.

### Plotting the Results
After running the benchmarks, run `python3 plot.py` in each benchmark directory to output the plots as pdf files.
An exception is `lmbench`, which does not have a `plot.py` script. Instead, run `python3 compare.py` to see the results.

### Description of Benchmarks
The following is a short description of each benchmark and how to compare the results with the ones in the paper.

#### apache
Evaluates apache web server using wrk with two configurations: 1) single process, 2) default.
Compare `apache.pdf` to Fig. 14a, and `results/default_results.csv` to Fig. 14b.

#### ds_benchmark
Evaluates each data structure (maple tree (`mp`), interval skiplist (`isl`)) for each operation type (Query, Alloc, Map).
Compare `latency.pdf` to Fig. 11a, and `Query.pdf`, `Alloc.pdf`, `Map.pdf` to Fig. 11b.

#### lmbench
Runs the lmbench multiple times.
Compare the output of `python3 compare.py` to Fig. 12.

#### lockstat
Evaluates apache, metis, and psearchy under `Linux 6.8.0-debug` and evaluates `wait time / total time`.
Compare `wasted_time_graph.pdf` to Fig. 1.

#### metis
Evaluates metis map-reduce by running the `wrmem` benchmark with 4GiB input size.
Compare `metis.pdf` to Fig. 14c.

#### microbench
Evaluates address space operations with microbenchmarks.
Compare `Alloc.pdf` and `Alloc + Fault + Modify.pdf` to Fig. 13.

#### psearchy
Evaluates psearchy text indexing by indexing the `Linux 6.8.0` source tree.
Compare `psearchy.pdf` to Fig. 14d.

### Uninstall
Run `cd scripts && sudo ./uninstall-all.sh`.
