# Read and validate WGBS coverage files.
# pathlib makes file paths work consistently across operating systems. 
from pathlib import Path

# panads is used to read and manipulate table-shaped data.
import pandas as pd

# This list gives meaningful names to expected Bismark coverage columns.
COVERAGE_COLUMNS = [
    "chromosome",
    "start",
    "end",
    "methylation_percent",
    "methylated_count",
    "unmethylated_count",
]

def read_coverage_file(path: str | Path) -> pd.DataFrame:
    """Read and validate one Bismark-style coverage file."""
    # Convert either a text path or Path object into a Path object.
    path = Path(path)

    # Stop early with a usefule error instead of letting pandas fail unclearly. 
    if not path.exists():
        raise FileNotFoundError(f"Coverage file does not"" exist: {path}")

    # Read a tab-separated file with no header row. 
    coverage = pd.read_csv(
        path,
        sep="\t",
        header=None,
        names=COVERAGE_COLUMNS,
        comment="#",
    )

        # An empty coverage file should be treated as an invalid input.
    if coverage.empty:
        raise ValueError(f"Coverage file is empty: {path}")

    # Define the columns that contain read counts.
    count_columns = ["methylated_count", "unmethylated_count"]

    # Read counts cannot be negative.
    if (coverage[count_columns] < 0).any().any():
        raise ValueError("Methylated and unmethylated counts cannot be negative.")

    # Methylation percentage must fall within the biological percentage range.
    if not coverage["methylation_percent"].between(0, 100).all():
        raise ValueError("Methylation percentages must be between 0 and 100.")

    # Keep the source filename as a sample identifier for multi-sample analysis.
    coverage["sample_id"] = path.stem

    # Return the validated table for downstream QC functions.
    return coverage
