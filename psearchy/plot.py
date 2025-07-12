import pandas as pd
import matplotlib.pyplot as plt
import sys
import glob
import psutil # For psutil.cpu_count()
from PyPDF2 import PdfReader, PdfWriter

# Constants for plot styling
label_size = 18
# ytick_size = 14
xtick_size = 14
line_width = 1.2
marker_size = 12

x_label_pad = -0.125
y_label_pad = -0.12
top_layout = 0.975
left_layout = 0.15

version_info = {
    "RadixVM": {"label": "radixvm", "linestyle": "solid", "marker": "^", "color": "lime"},
    "6.8.0": {"label": "linux", "linestyle": "solid", "marker": "x", "color": "red"},
    "6.8.0-interval-vm+": {"label": "linux-ours", "linestyle": "solid", "marker": "s", "color": "blue"},
}

def load_csv_files():
    """Loads all CSV files in the current directory into a dictionary of DataFrames."""
    data = {}
    for file in glob.glob("*.csv"):
        kernel_version = file.split(".csv")[0]  # Use the filename (kernel version) as the key
        data[kernel_version] = pd.read_csv(file)
    return data

def crop_pdf(input_pdf, output_pdf, crop_left=0, crop_right=0, crop_up=0, crop_down=0):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page in reader.pages:
        media_box = page.mediabox
        
        # Modify media box coordinates for cropping
        media_box.lower_left = (
            media_box.lower_left[0] + crop_left,  # Crop from left
            media_box.lower_left[1] + crop_down  # Crop from bottom
        )
        media_box.upper_right = (
            media_box.upper_right[0] - crop_right,  # Crop from right
            media_box.upper_right[1] - crop_up     # Crop from top
        )
        
        writer.add_page(page)
    
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

def draw(output_name, data, cpu_count=48):
    plt.figure(figsize=(5, 5))

    # Adjust layout for fixed axis alignment
    plt.subplots_adjust(left=left_layout, right=0.98, bottom=0.15, top=top_layout)

    # Plot each kernel version's data
    for kernel_version in version_info.keys():
        if kernel_version in data:
            df = data[kernel_version]
            label = version_info[kernel_version]["label"]
            linestyle = version_info[kernel_version]["linestyle"]
            marker = version_info[kernel_version]["marker"]
            color = version_info[kernel_version]["color"]

            df_sorted = df.sort_values(by="cores")
            plt.plot(
                df_sorted["cores"], 
                df_sorted["throughput"], 
                label=label, 
                linewidth=line_width, 
                linestyle=linestyle, 
                markersize=marker_size, 
                marker=marker, 
                markerfacecolor='none',
                color=color
            )

    # Labeling
    plt.xlabel("Threads", fontsize=label_size)
    plt.ylabel("Throughput (jobs/hour)", fontsize=label_size)
    plt.gca().xaxis.set_label_coords(0.5, x_label_pad)
    plt.gca().yaxis.set_label_coords(y_label_pad, 0.5)
    # plt.yticks(fontsize=ytick_size)
    plt.xticks(fontsize=xtick_size, rotation=90)
    plt.grid(alpha=0.5)
    
    # Custom legend order
    handles, labels = plt.gca().get_legend_handles_labels()
    ordered_handles = []
    ordered_labels = []

    for key in version_info.keys():
        label = version_info[key]["label"]
        if label in labels:
            idx = labels.index(label)
            ordered_handles.append(handles[idx])
            ordered_labels.append(labels[idx])
    # plt.legend(ordered_handles, ordered_labels, fontsize=label_size, title_fontsize=label_size-2)

    # Add a shaded region if core count exceeds cpu_count
    if max(df["cores"].max() for df in data.values()) >= cpu_count:
        left, right = plt.xlim()
        plt.axvspan(cpu_count, right, facecolor="#FF00000A", label=f"Exceeds {cpu_count} cores")
        plt.xlim(left, right)

    # Dynamic y-axis limits
    all_cycles = pd.concat([df["throughput"] for df in data.values()])
    y_max = all_cycles.max() * 1.05
    y_min = all_cycles.min() * 0.95
    plt.ylim(y_min, y_max)

    # Save plot as PDF
    plt.savefig(output_name, format='pdf')
    print(f"Plot saved to {output_name}")

    cropped_output_name = output_name.replace(".pdf", "_cropped.pdf")
    crop_pdf(output_name, cropped_output_name, crop_left=23)  # Adjust crop_left as needed
    print(f"Cropped plot saved to {cropped_output_name}")

if __name__ == "__main__":
    # Load CPU count if provided
    cpu_count = int(sys.argv[1]) if len(sys.argv) > 1 else psutil.cpu_count(logical=False) or 32

    # Load all CSV files in the directory
    data = load_csv_files()

    # Draw and save the plot
    output_name = "psearchy.pdf"
    draw(output_name, data, cpu_count)