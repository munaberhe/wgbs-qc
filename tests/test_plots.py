# Tests for coverage-distribution plots.

# tempfile provides a safe temporary directory for test outputs.
import tempfile
from pathlib import Path

# Import the function being tested and its helper.
from wgbs_qc.plots import plot_coverage_distribution
from wgbs_qc.coverage import add_total_coverage

# pandas builds small in-memory coverage tables.
import pandas as pd


def make_test_coverage() -> pd.DataFrame:
    """Create a small predictable coverage table for unit tests."""

    return pd.DataFrame(
        {
            "chromosome": ["chr1", "chr1", "chr2", "chr2", "chr2"],
            "start": [100, 200, 300, 400, 500],
            "end": [100, 200, 300, 400, 500],
            "methylation_percent": [80.0, 50.0, 20.0, 100.0, 0.0],
            "methylated_count": [8, 4, 2, 12, 0],
            "unmethylated_count": [2, 1, 3, 8, 1],
            "sample_id": ["test_sample"] * 5,
        }
    )


def test_plot_coverage_distribution_creates_file():
    """Ensure plot_coverage_distribution creates a PNG file."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Use a temporary directory for the test output.
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_coverage_dist.png"

        # Call the plotting function.
        plot_coverage_distribution(coverage, str(output_path), title="Test coverage")

        # Confirm the file was created.
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        