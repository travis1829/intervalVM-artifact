import subprocess
import sys
import os

def run_benchmark(repeat):
    import platform

    # Get the system's node name (hostname)
    node_name = platform.uname().node
    config_path = f"bin/x86_64-linux-gnu/CONFIG.{node_name}"

    # If config file does not exist, run configuration
    if not os.path.isfile(config_path):
        print("CONFIG file not found. Running configuration...")

        # Prepare input sequence for configuration.
        # Use memory: 1024MB because the default value, which tests the whole memory,
        # takes extremely long. Even a few GBs take a very long time.
        config_inputs = "\n" * 2 + "1024\n" + "\n" * 8 + "no\n"

        try:
            subprocess.run(
                ["make", "results", "-C", "src"],
                input=config_inputs,
                text=True,
                check=True
            )
            repeat = repeat - 1
        except subprocess.CalledProcessError as e:
            print("Configuration failed:", e)
            return

    # Run the benchmark repeat times
    for i in range(repeat):
        print(f"Running rerun iteration {i+1}...")
        try:
            subprocess.run(["make", "rerun", "-C", "src"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Rerun iteration {i+1} failed:", e)
            break

if __name__ == "__main__":
    # Set default values if arguments are not provided
    repeat = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    run_benchmark(repeat)
