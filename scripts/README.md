Run `./install-all.sh` to build and install everything, and `./uninstall-all.sh` to uninstall everything.

# Issues
`install-packages.sh` currently only works for ubuntu/debian. Please use your own package manager for different distros.

Some device drivers (e.g. nvidia gpu drivers) may cause the installation fail, because they reject everything except the kernels they recognize. Please uninstall them if they cause a problem.

Please uninstall anaconda or at least remove it from `$PATH` before installing.
