import json
import dask.dataframe as dd
import pandas as pd
from pymongo import MongoClient


def extract_data():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["openfoodfacts"]
    collection = db["off_products"]
    df1 = pd.DataFrame(list(collection.find({"id":"0010700859051"})))
    collection = db["fdc_products"]
    df2 = pd.DataFrame(list(collection.find({"id":"0010700859051"})))

    return df1, df2


def calculate_similarity(row):
    total_fields = len(row) // 2
    matches = sum(
        row[col] == row[col.replace("_src1", "_src2")]
        for col in row.index if "_src1" in col
    )
    return (matches / total_fields) * 100


def main():
    df1, df2 = extract_data()

    ddf1 = dd.from_pandas(df1, npartitions=1)
    ddf2 = dd.from_pandas(df2, npartitions=1)

    ddf1 = ddf1.set_index("id")
    ddf2 = ddf2.set_index("id")

    merged = ddf1.join(ddf2, lsuffix="_src1", rsuffix="_src2", how="outer")

    for col in merged.columns:
        if "_src1" in col:
            merged[col] = merged[col].astype(str)
        elif "_src2" in col:
            merged[col] = merged[col].astype(str)

    merged["similarity"] = merged.apply(calculate_similarity, axis=1, meta=("similarity", "f8"))

    merged_df = merged.compute()
    avg = merged_df["similarity"].mean()
    print(f"Average similarity: {avg:.2f}%")

    print(merged_df.to_json(orient="records", indent=4))


if __name__ == "__main__":
    main()