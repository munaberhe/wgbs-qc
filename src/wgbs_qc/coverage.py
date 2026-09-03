# Calculate WGBS coverage metrics.

# pandas provides DataFrame and Series data structures.
import pandas as pd


def add_total_coverage(coverage: pd.DataFrame) -> pd.DataFrame:
    """Add total CpG coverage without modifying the caller's DataFrame."""

    # Copy the input so the original DataFrame remains unchanged.
    result = coverage.copy()

    # Total CpG coverage is methylated plus unmethylated read counts.
    result["total_coverage"] = (
        result["methylated_count"] + result["unmethylated_count"]
    )

    # Return the DataFrame with the additional coverage column.
    return result


def sample_summary(coverage: pd.DataFrame) -> pd.Series:
    """Calculate core WGBS QC metrics for one sample."""

    # Ensure total coverage is available for all downstream metrics.
    coverage = add_total_coverage(coverage)

    # Collect QC metrics in a labelled pandas Series.
    summary = pd.Series(
        {
            # Count CpG observations in the sample.
            "n_cpg_sites": len(coverage),

            # Calculate average depth across CpG sites.
            "mean_coverage": coverage["total_coverage"].mean(),

            # Calculate middle depth after sorting CpG coverage values.
            "median_coverage": coverage["total_coverage"].median(),

            # Calculate average percentage methylation across CpG sites.
            "mean_methylation_percent": coverage["methylation_percent"].mean(),

            # Calculate proportion of CpGs supported by at least 10 reads.
            "fraction_coverage_ge_10": (
                coverage["total_coverage"].ge(10).mean()
            ),
        }
    )

    # Return the labelled QC metrics.
    return summary
