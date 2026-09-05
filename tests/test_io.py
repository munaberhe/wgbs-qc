# Test WGBS coverage-file input and validation

# pytest provides helpers for checking expected errors.
import pytest

# Import the function being tested from the actual package code. 
from wgbs_qc.io import read_coverage_file

def test_read_coverage_file_returns_expected_columns():
    """Load a valid coverage file with expected columns and row counts."""

    # Read the small sunthetic WGBS coverage file.
    result = read_coverage_file("data/example_sample_1.cov")

    # Check that the returned table contains the expected metadata fields.
    assert "chromosome" in result.columns
    assert "methylation_percent" in result.columns
    assert "methylated_count" in result.columns
    assert "unmethylated_count" in result.columns
    assert "sample_id" in result.columns

    # The synthetic input file contains five CpG records.
    assert len(result) == 5

    # use the DataFrame returned by read_coverage_file(). 
    assert result["sample_id"].iloc[0] == "example_sample_1"

def test_missing_coverage_file_raises_file_not_found_error():
    """Raise a clear error when the input path does not exist."""

    # Confirm that a non-existent file is rejected.
    with pytest.raises(FileNotFoundError):
        read_coverage_file("data/not_a_real_sample.cov")
