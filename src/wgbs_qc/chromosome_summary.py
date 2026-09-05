# Per-chromosome WGBS coverage summaries.

# pandas provides DataFrame operations for grouping and aggregation.
import pandas as pd

# Import the total-coverage helper from your package.
from wgbs_qc.coverage import add_total_coverage


def chromosome_summary(coverage: pd.DataFrame) -> pd.DataFrame:
    """Summarize coverage and methylation per chromosome."""

    # Ensure total coverage is available for aggregation.
    coverage = add_total_coverage(coverage)

    # Group by chromosome and compute key metrics.
    result = (
        coverage.groupby("chromosome", observed=True)
        .agg(
            n_cpg_sites=("chromosome", "size"),
            mean_coverage=("total_coverage", "mean"),
            median_coverage=("total_coverage", "median"),
            mean_methylation_percent=("methylation_percent", "mean"),
        )
        .reset_index()
    )

    # Preserve the original chromosome order from the input data.
    chrom_order = coverage["chromosome"].drop_duplicates().tolist()
    result = result.reindex(
        result["chromosome"].map({c: i for i, c in enumerate(chrom_order)}).argsort()
    ).reset_index(drop=True)

    # Return the per-chromosome summary table.
    return result