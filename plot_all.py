import os
import pandas as pd
import matplotlib.pyplot as plt
 
df = pd.read_csv("combined.csv")
os.makedirs("plots", exist_ok=True)
 
groups = df[df.sparsity == 1.0].groupby(
    ["kernel", "op", "analysis", "element_type"], dropna=False)
 
for (kernel, op, analysis, etype), g in groups:
    plt.figure(figsize=(6, 4))
    for approach in ["naive", "vectorized", "fused"]:
        s = g[g.approach == approach].sort_values("n")
        if not s.empty:
            plt.plot(s.n, s.mean_ns / 1e6, marker="o", label=approach) 
    plt.xlabel("n")
    plt.ylabel("time (ms)")
    plt.title(f"{kernel} {op} | {analysis} | {etype}", wrap=True)
    plt.legend()
    plt.tight_layout()
 
    name = f"plots/{kernel}_{op}_{analysis}_{etype}.png".replace("+", "-")
    plt.savefig(name, dpi=120)
    plt.close()
