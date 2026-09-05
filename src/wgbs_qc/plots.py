# Coverage-distribution plots for WGBS QC.

# pathlib provides reliable cross-platform file-path handling.
from pathlib import Path

# matplotlib creates static plots; pyplot is the main plotting interface.
import matplotlib.pyplot as plt

# Import the total-coverage helper from your package.
from wgbs_qc.coverage import add_total_coverage


def plot_coverage_distribution(coverage, output_path: str, title: str = "Coverage distribution") -> None:
    """Plot a histogram of total coverage and save to a file."""

    # Ensure total coverage is available for plotting.
    coverage = add_total_coverage(coverage)

    # Create a new figure and axis for the histogram.
    fig, ax = plt.subplots(figsize=(6, 4))

    # Plot a histogram of total coverage with sensible binning.
    ax.hist(coverage["total_coverage"], bins=20, edgecolor="black")

    # Label axes and title for clarity.
    ax.set_xlabel("Total coverage")
    ax.set_ylabel("Number of CpG sites")
    ax.set_title(title)

    # Ensure the output directory exists before saving.
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the figure to disk.
    fig.savefig(output_path, dpi=150, bbox_inches="tight")

    # Close the figure to free memory.
    plt.close(fig)