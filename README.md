# Requirements

`uv` must be installed to run the python files.

# How to use

Move the directory of benchmark files (csv files) generated in `/tmp/benchmark` into this directory to recreate the plots and data analysis.

Run `sh ./main.sh` to generate all plots and intermediate csv files.

Run `uv run python select_matrix_repr.py` to determine for which instantiations the Daphne compiler could not compile with the `--select_matrix_repr` flag.

# Plots
Under `plots/` are three kind of plots.

`overhead_*.png` are plots that show the overhead of running the analyses relative to a no analysis DaphneDSL script. The `no_d` files do not show the bar for `numDistinct` as it is often too much bigger than the others.

The rest of the csv files are bar graphs showing the difference in performance for the equivalent analyses for all variants (naive, vectorized, fused) that it ran for. Often times, not all of them are available.