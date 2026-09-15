import pandas as pd
import glob

for path in glob.glob("daphneDSL/*.csv"):
    df = pd.read_csv(path)
    if "select-matrix-repr" not in df.columns:
        continue

    # normalize to real booleans. Otherwise it doesn't work.
    repr_off = df["select-matrix-repr"].map({"True": True, "False": False,
                                             True: True, False: False})
    false_rows = df[repr_off == False]
    if false_rows.empty:
        continue

    print(f"{path}:")
    combos = false_rows[["op", "element_type"]].drop_duplicates().sort_values(["op", "element_type"])
    print(combos.to_string(index=False))
    print()