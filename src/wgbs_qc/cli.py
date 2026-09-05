# Command-line interface for the WGBS QC toolkit.

# Click provides the command-line interface framework.
import click

# Import core functionality from the package.
from wgbs_qc.io import read_coverage_file
from wgbs_qc.coverage import add_total_coverage
from wgbs_qc.summary import sample_summary, multi_sample_summary
from wgbs_qc.chromosome_summary import chromosome_summary
from wgbs_qc.plots import plot_coverage_distribution


@click.group()
def cli():
    """WGBS QC toolkit."""
    pass


@cli.command()
@click.argument("cov_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="results/summary.txt",
    help="Path to write the summary report.",
)
def summarize(cov_file: str, output: str) -> None:
    """Generate a sample-level QC summary from a .cov file."""

    # Load the coverage data.
    coverage = read_coverage_file(cov_file)

    # Compute per-sample QC metrics.
    summary = sample_summary(coverage)

    # Write the summary to a text file.
    with open(output, "w") as f:
        f.write("WGBS QC Summary\n")
        f.write("================\n\n")
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")

    # Inform the user where the report was written.
    click.echo(f"Summary written to {output}")


@cli.command()
@click.argument("pattern", type=click.Path())
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="results/multi_sample_summary.csv",
    help="Path to write the multi-sample summary CSV.",
)
def multi_summary(pattern: str, output: str) -> None:
    """Generate a multi-sample QC summary from multiple .cov files."""

    # Compute the multi-sample summary.
    summary = multi_sample_summary(pattern)

    # Write the summary to a CSV file.
    summary.to_csv(output, index=False)

    # Inform the user where the report was written.
    click.echo(f"Multi-sample summary written to {output}")


@cli.command()
@click.argument("cov_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="results/chromosome_summary.csv",
    help="Path to write the per-chromosome summary CSV.",
)
def chr_summary(cov_file: str, output: str) -> None:
    """Generate a per-chromosome QC summary from a .cov file."""

    # Load the coverage data.
    coverage = read_coverage_file(cov_file)

    # Compute per-chromosome summaries.
    summary = chromosome_summary(coverage)

    # Write the summary to a CSV file.
    summary.to_csv(output, index=False)

    # Inform the user where the report was written.
    click.echo(f"Chromosome summary written to {output}")


@cli.command()
@click.argument("cov_file", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="results/plots/coverage_distribution.png",
    help="Path to save the coverage-distribution plot.",
)
@click.option(
    "--title",
    "-t",
    type=str,
    default="Coverage distribution",
    help="Title for the plot.",
)
def plot_coverage(cov_file: str, output: str, title: str) -> None:
    """Generate a coverage-distribution histogram from a .cov file."""

    # Load the coverage data.
    coverage = read_coverage_file(cov_file)

    # Create and save the plot.
    plot_coverage_distribution(coverage, output_path=output, title=title)

    # Inform the user where the plot was saved.
    click.echo(f"Coverage plot saved to {output}")


if __name__ == "__main__":
    cli()