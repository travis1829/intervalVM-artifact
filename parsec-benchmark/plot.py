import pandas as pd
import matplotlib.pyplot as plt

output_name = "parsec.pdf"

# Load the CSV files
baseline = pd.read_csv("results/6.8.0.csv")
interval = pd.read_csv("results/6.8.0-interval-vm+.csv")

# Merge on benchmark name
merged = pd.merge(baseline, interval, on="benchmark", suffixes=("_base", "_int"))

# Compute normalized throughput (inverse of runtime ratio)
merged["normalized_throughput"] = merged["real_base"] / merged["real_int"]

# Sort for nicer plotting
merged = merged.sort_values("normalized_throughput")

# Plot bar chart
plt.figure(figsize=(10, 3))
plt.bar(merged["benchmark"], merged["normalized_throughput"])

# Add labels and title
plt.axhline(1, color="red", linestyle="--", linewidth=1)  # baseline reference
# plt.xlabel("Benchmark")
plt.ylabel("Normalized Throughput")
# plt.title("Normalized Throughput per Benchmark")
plt.xticks(rotation=45, ha="right")

# Show values on top of each bar
for idx, val in enumerate(merged["normalized_throughput"]):
    plt.text(idx, val - 0.008, f"{val:.2f}", ha="center", va="bottom", fontsize=8)

# Increase y-limit by 10% so text fits
ymax = merged["normalized_throughput"].max()
plt.ylim(0, ymax * 1.1)

plt.tight_layout()

plt.savefig(output_name, format='pdf')
print(f"Plot saved to {output_name}")
