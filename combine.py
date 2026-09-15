import re
import glob
import pandas as pd

# collect all c++ fusion csv files into one.
cpp = []
for path in glob.glob("stats/*.csv"):
    df = pd.read_csv(path)
    # for CTable, just put the resulting matrix type as an Op so it is consistent with the other tables.
    if "result_repr" in df:
        df = df.rename(columns={"result_repr": "op"})
    df["kernel"] = path.split("/")[-1].replace("MatAnalysisAcc.csv","").replace("AnalysisAcc.csv", "")
    df["approach"] = "fused"
    cpp.append(df)
cpp = pd.concat(cpp)

# collect all daphne fusion csv files into one.
dsl = []
for path in glob.glob("daphneDSL/stats/*.csv"):
    df = pd.read_csv(path)
    df["kernel"] = path.split("/")[-1].replace(".csv", "")
    df["approach"] = df["mode"]
    dsl.append(df)
dsl = pd.concat(dsl)

# merge all csvs into one
both = pd.concat([cpp, dsl])

# replace all empty or NaNs with "none" and sort order of analyses
def clean_analysis(s):
    if pd.isna(s) or str(s).strip() in ("", "nan"):
        return "none"
    parts = [p for p in re.split(r"[,\s+]+", str(s).strip()) if p]
    return "+".join(sorted(parts))

both["analysis"] = both["analysis"].map(clean_analysis)
# make everything uppercase
both["op"] = both["op"].fillna("").astype(str).str.upper()

both.to_csv("combined.csv", index=False)