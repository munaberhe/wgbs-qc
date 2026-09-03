# Test WGBS coverage calculations.

# pandas builds a small in-memory test DataFrame.
import pandas as pd

# Import the functions being tested.
from wgbs_qc.coverage import add_total_coverage, sample_summary


def make_test_coverage() -> pd.DataFrame:
    """Create a small predictable coverage table for unit tests."""

    # Use known values so expected outputs can be calculated by hand.
    return pd.DataFrame(
        {
            "chromosome": ["chr1", "chr1", "chr1", "chr1", "chr1"],
            "start": [100, 200, 300, 400, 500],
            "end": [100, 200, 300, 400, 500],
            "methylation_percent": [80.0, 50.0, 20.0, 100.0, 0.0],
            "methylated_count": [8, 4, 2, 12, 0],
            "unmethylated_count": [2, 1, 3, 8, 1],
            "sample_id": ["test_sample"] * 5,
        }
    )


def test_add_total_coverage_calculates_expected_values():
    """Calculate total coverage as methylated plus unmethylated reads."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Run the function being tested.
    result = add_total_coverage(coverage)

    # Check the expected total coverage at every CpG.
    assert result["total_coverage"].tolist() == [10, 5, 5, 20, 1]


def test_add_total_coverage_does_not_change_input_dataframe():
    """Return a copy instead of altering the caller's input DataFrame."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Run the function.
    add_total_coverage(coverage)

    # The original input should not gain a total_coverage column.
    assert "total_coverage" not in coverage.columns


def test_sample_summary_returns_expected_metrics():
    """Calculate correct QC metrics from known coverage values."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Calculate the QC summary.
    summary = sample_summary(coverage)

    # Verify each expected metric.
    assert summary["n_cpg_sites"] == 5
    assert summary["mean_coverage"] == 8.2
    assert summary["median_coverage"] == 5.0
    assert summary["mean_methylation_percent"] == 50.0
    assert summary["fraction_coverage_ge_10"] == 0.4