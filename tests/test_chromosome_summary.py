# Test per-chromosome WGBS coverage summaries.

# pandas builds small in-memory coverage tables.
import pandas as pd

# Import the function being tested.
from wgbs_qc.chromosome_summary import chromosome_summary


def make_test_coverage() -> pd.DataFrame:
    """Create a small predictable coverage table for unit tests."""

    # Use known values so expected outputs can be calculated by hand.
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


def test_chromosome_summary_returns_expected_shape_and_columns():
    """Return one row per chromosome with expected QC columns."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Compute per-chromosome summaries.
    result = chromosome_summary(coverage)

    # Expect two rows (chr1 and chr2).
    assert result.shape[0] == 2

    # Expect the key QC columns to be present.
    assert "chromosome" in result.columns
    assert "n_cpg_sites" in result.columns
    assert "mean_coverage" in result.columns
    assert "median_coverage" in result.columns
    assert "mean_methylation_percent" in result.columns

    # Check chromosome labels.
    assert set(result["chromosome"]) == {"chr1", "chr2"}


def test_chromosome_summary_calculates_correct_metrics():
    """Calculate correct per-chromosome metrics from known values."""

    # Build the controlled test input.
    coverage = make_test_coverage()

    # Compute per-chromosome summaries.
    result = chromosome_summary(coverage)

    # chr1: two CpGs, coverages 10 and 5 -> mean 7.5, median 7.5
    chr1 = result[result["chromosome"] == "chr1"].iloc[0]
    assert chr1["n_cpg_sites"] == 2
    assert chr1["mean_coverage"] == 7.5
    assert chr1["median_coverage"] == 7.5
    assert chr1["mean_methylation_percent"] == 65.0  # (80 + 50) / 2

    # chr2: three CpGs, coverages 5, 20, 1 -> mean 8.666..., median 5
    chr2 = result[result["chromosome"] == "chr2"].iloc[0]
    assert chr2["n_cpg_sites"] == 3
    assert abs(chr2["mean_coverage"] - (5 + 20 + 1) / 3) < 1e-6
    assert chr2["median_coverage"] == 5.0
    assert chr2["mean_methylation_percent"] == 40.0  # (20 + 100 + 0) / 3