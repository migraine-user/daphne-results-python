import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("combined.csv")

os.makedirs("plots", exist_ok=True)

fused = df[(df.approach == "fused") & (df.sparsity == 1.0) & (df.n == 4096)]

for kernel, g in fused.groupby("kernel"):
    # CTable's coordinate vectors are int64_t. Otherwise default to comparing for double.
    etype = "int64_t" if kernel == "CTable" else "double"
    g = g[g.element_type == etype]

    base = df[(df.approach == "naive") & (df.analysis == "none") &
              (df.kernel == kernel) & (df.element_type == etype) &
              (df.sparsity == 1.0) & (df.n == 4096)]
    if base.empty:
        print(f"{kernel}: no DaphneDSL baseline, skipping")
        continue
    baseline_ns = base["mean_ns"].mean()

    other = g.copy()
    other["overhead_pct"] = (other["mean_ns"] - baseline_ns) / baseline_ns * 100
    other = other.sort_values(by="analysis", key=lambda col: col.str.len())

    plt.figure(figsize=(8, 4))
    plt.bar(other["analysis"], other["overhead_pct"])
    plt.axhline(0, color="black", lw=1)
    plt.xticks(rotation=40, ha="right", fontsize=8, wrap=True)
    plt.ylabel("overhead vs no-analysis (%)")
    plt.title(f"{kernel}: fused C++ analysis vs DaphneDSL baseline ({etype}) (n=4096)", wrap=True)

    plt.tight_layout()
    plt.savefig(f"plots/overhead_{kernel}.png")
    plt.close()
    
    
for kernel, g in fused.groupby("kernel"):
    # CTable's coordinate vectors are int64_t. Otherwise default to comparing for double.
    etype = "int64_t" if kernel == "CTable" else "double"
    g = g[g.element_type == etype]

    base = df[(df.approach == "naive") & (df.analysis == "none") &
              (df.kernel == kernel) & (df.element_type == etype) &
              (df.sparsity == 1.0) & (df.n == 4096)]
    if base.empty:
        print(f"{kernel}: no DaphneDSL baseline, skipping")
        continue
    baseline_ns = base["mean_ns"].mean()

    other = g.copy()
    other["overhead_pct"] = (other["mean_ns"] - baseline_ns) / baseline_ns * 100
    other = (other.groupby("analysis", as_index=False)["overhead_pct"].mean())
    other = other[other.analysis != "numDistinct"] 
    other = other.sort_values(by="analysis", key=lambda col: col.str.len())

    plt.figure(figsize=(8, 4))
    # replace the full analysis string to "all"
    other["analysis"] = other["analysis"].apply(lambda x: "all" if len(x) >= 20 else x)
    plt.bar(other["analysis"], other["overhead_pct"])
    plt.axhline(0, color="black", lw=1)
    # plt.xticks(rotation=40, ha="right", fontsize=8, wrap=True)
    plt.xticks(fontsize=8, ha="right", rotation=40)
    plt.ylabel("overhead vs no-analysis (%)") 
    plt.title(f"{kernel}: fused C++ analysis vs DaphneDSL baseline ({etype}) (n=4096)", wrap=True)
    plt.tight_layout()
    plt.savefig(f"plots/overhead_no_d_{kernel}.png")
    plt.close()
