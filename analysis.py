import pandas as pd
import glob
# Statistics on daphneDSL benchmark
cols = ["mode","op","element_type","analysis","n","sparsity","seed","time_ns","select-matrix-repr"]
# we group by everything aside from seed and time
relevant_cols = ["mode","op","element_type","analysis","n","sparsity","select-matrix-repr"]
df = pd.read_csv("daphneDSL/AggCol.csv")
# then we aggregate on the time
df.groupby(relevant_cols, dropna=False)["time_ns"].agg(mean_ns="mean", std_ns="std").reset_index()
import os
os.makedirs("daphneDSL/stats", exist_ok=True)
for path in glob.glob("daphneDSL/*.csv"):
    df = pd.read_csv(path)
    agg = df.groupby(relevant_cols, dropna=False)["time_ns"].agg(mean_ns="mean", std_ns="std").reset_index()
    file_name = path.split("/")[1]
    agg.to_csv(f"daphneDSL/stats/{file_name}", index=False)
# Statistics on my c++ side fused benchmarks
os.makedirs("stats", exist_ok=True)
for path in glob.glob("*Acc.csv"):
    df = pd.read_csv(path)
    # for CTable the cols are different so we dynamically deal with the columns.
    relevant_cols = df.columns.to_list()
    relevant_cols.remove("time_ns")
    agg = df.groupby(relevant_cols, dropna=False)["time_ns"].agg(mean_ns="mean", std_ns="std").reset_index()
    file_name = path
    agg.to_csv(f"stats/{file_name}", index=False)
# Remove `AnalysisFlag::` for sanity.
for path in glob.glob("stats/*.csv"):
    with open(path,"r") as f:
        s = f.read().replace("AnalysisFlag::","")
    with open(path,"w") as f:
        f.write(s)


