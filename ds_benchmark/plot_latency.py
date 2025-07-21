import pandas as pd
import matplotlib.pyplot as plt
import glob

# Constants for plot styling
label_size = 25
ytick_size = 18
xtick_size = 25
bar_width = 0.4
colors = {"isl": "blue", "mp": "red"}
hatches = {"isl": "//", "mp": "x"}

benchmarks = ["find", "alloc", "remove"]
benchmark_titles = {"find": "Query", "alloc": "Alloc", "remove": "Map"}
version_labels = {"isl": "Interval Skiplist", "mp": "Maple Tree"}

def load_single_core_latency(benchtype):
    """Loads CSV files and calculates single-core latency (1 / throughput at core=1)."""
    latencies = {}
    for file in glob.glob(f"results/{benchtype}/*.csv"):
        kernel_version = file.split(".csv")[0].split("/")[-1]  # Extract version from filename
        df = pd.read_csv(file)
        single_core_row = df[df["cores"] == 1]
        if not single_core_row.empty:
            latencies[kernel_version] = 1000000 / single_core_row["throughput"].values[0]
    return latencies

def draw_bar_chart(output_name):
    fig, ax = plt.subplots(figsize=(8, 6))
    x_labels = benchmark_titles.values()
    x_indexes = range(len(x_labels))
    
    bars = []
    for i, version in enumerate(["isl", "mp"]):
        latencies = [load_single_core_latency(bench)[version] for bench in benchmarks]
        x_positions = [x + (i * bar_width) for x in x_indexes]
        bars.append(ax.bar(x_positions, latencies, width=bar_width, color='white', edgecolor=colors[version], hatch=hatches[version], label=version_labels[version]))
    
    # Formatting
    # ax.set_xlabel("Benchmark", fontsize=label_size)
    ax.set_ylabel("Latency (μs)", fontsize=label_size)
    ax.set_xticks([x + bar_width / 2 for x in x_indexes])
    ax.set_xticklabels(x_labels, fontsize=xtick_size)
    ax.legend(fontsize=label_size)
    ax.tick_params(axis='y', labelsize=ytick_size)
    ax.grid(axis='y', alpha=0.5)
    
    # plt.title("Single Core Latency Comparison", fontsize=20)
    plt.tight_layout()
    plt.savefig(output_name, format='pdf')
    print(f"Bar chart saved to {output_name}")

if __name__ == "__main__":
    output_pdf = "latency.pdf"
    draw_bar_chart(output_pdf)
