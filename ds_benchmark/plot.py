import sys
import psutil
import plot_latency
import plot_throughput

if __name__ == "__main__":
    output_pdf = "latency.pdf"
    plot_latency.draw_bar_chart(output_pdf)

    cpu_count = int(sys.argv[1]) if len(sys.argv) > 1 else psutil.cpu_count(logical=False) or 32
    plot_throughput.draw(cpu_count)
