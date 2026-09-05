# Test multi-sample WGBS QC summaries.

# pandas builds small in-memory coverage tables.
import pandas as pd

# pytest provides helpers for checking expected errors.
import pytest

# Import the function being tested.
from wgbs_qc.summary import multi_sample_summary


def test_multi_sample_summary_returns_expected_shape_and_columns():
    """Return one row per sample with expected QC columns."""

    # Compute QC summaries for the two synthetic example files.
    result = multi_sample_summary("data/example_sample_*.cov")

    # Expect two rows (one per example file).
    assert result.shape[0] == 2

    # Expect the key QC columns to be present.
    assert "sample_id" in result.columns
    assert "n_cpg_sites" in result.columns
    assert "mean_coverage" in result.columns
    assert "median_coverage" in result.columns
    assert "mean_methylation_percent" in result.columns
    assert "fraction_coverage_ge_10" in result.columns

    # Check that sample identifiers are derived correctly from filenames.
    assert set(result["sample_id"]) == {"example_sample_1", "example_sample_2"}


def test_multi_sample_summary_raises_when_no_files_found():
    """Raise FileNotFoundError when the glob pattern matches nothing."""

    # Confirm that an invalid pattern triggers a clear error.
    with pytest.raises(FileNotFoundError):
        multi_sample_summary("data/nonexistent_pattern_*.cov")