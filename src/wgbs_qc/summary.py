# Multi-sample WGBS QC summaries.

# glob finds all coverage files matching a pattern.
from glob import glob

# pandas builds and combines per-sample summary tables.
import pandas as pd

# Import functions from your own package.
from wgbs_qc.io import read_coverage_file
from wgbs_qc.coverage import sample_summary


def multi_sample_summary(pattern: str) -> pd.DataFrame:
    """Load many coverage files and return one QC row per sample."""

    # Find all files matching the user-supplied glob pattern.
    paths = sorted(glob(pattern))

    # Stop early if no files are found; this usually indicates a wrong path.
    if not paths:
        raise FileNotFoundError(f"No coverage files found for pattern: {pattern}")

    # Calculate per-sample QC metrics for each file.
    summaries = []
    for path in paths:
        # Load and validate the coverage file using your existing reader.
        coverage = read_coverage_file(path)

        # Compute the QC summary for this sample.
        summary = sample_summary(coverage)
        summary["sample_id"] = coverage["sample_id"].iloc[0]
        summaries.append(summary)

    # Combine individual summaries into a single DataFrame.
    result = pd.DataFrame(summaries)

    # Reorder columns so sample_id appears first.
    cols = ["sample_id"] + [c for c in result.columns if c != "sample_id"]
    result = result[cols]

    # Return the multi-sample QC table.
    return result