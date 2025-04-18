import json
import logging
import dask.dataframe as dd
import pandas as pd
import Levenshtein
from pymongo import MongoClient


def extract_data(use_docker: bool = True):
    """Extracts the data from the off_products and fdc_products collections as dataframes"""
    connection_string = (
        "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
    )
    client = MongoClient(connection_string)
    db = client["openfoodfacts"]

    collection = db["off_products"]
    df1 = pd.DataFrame(list(collection.find({"id_match": "99999967647"})))

    collection = db["fdc_products"]
    df2 = pd.DataFrame(list(collection.find({"id_match": "99999967647"})))

    return df1, df2


def levenshtein_similarity(str1: str, str2: str) -> float:
    """Returns a similarity score based on Levenshtein distance"""
    if pd.isna(str1) or pd.isna(str2):
        return 0

    str1, str2 = str(str1), str(str2)

    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 100

    distance = Levenshtein.distance(str1, str2)
    similarity = (1 - (distance / max_len)) * 100

    return similarity


def calculate_similarity(row: pd.Series) -> float:
    """Returns the mean similarity based on several fields"""
    fields_to_compare = [
        col for col in row.index if "_src1" in col and "_id" not in col
    ]
    total_fields = len(fields_to_compare)

    if total_fields == 0:
        return 0

    similarities = [
        levenshtein_similarity(row[col], row[col.replace("_src1", "_src2")])
        for col in fields_to_compare
    ]

    return sum(similarities) / total_fields


def store_mismatched_products(mismatches, use_docker: bool = True):
    """Stocke les produits dont la similarité est inférieure à 100% dans MongoDB"""
    connection_string = (
        "mongodb://mongo:27017/" if use_docker else "mongodb://localhost:37017"
    )
    client = MongoClient(connection_string)
    db = client["openfoodfacts"]
    collection = db["waiting_for_treatement_products"]

    if mismatches:
        collection.insert_many(mismatches)
        logging.info(
            f"{len(mismatches)} produits enregistrés dans mismatched_products."
        )


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    df1, df2 = extract_data()

    ddf1 = dd.from_pandas(df1, npartitions=1)
    ddf2 = dd.from_pandas(df2, npartitions=1)

    ddf1 = ddf1.set_index("id_match")
    ddf2 = ddf2.set_index("id_match")

    merged = ddf1.join(ddf2, lsuffix="_src1", rsuffix="_src2", how="outer")

    for col in merged.columns:
        if "_src1" in col:
            merged[col] = merged[col].astype(str)
        elif "_src2" in col:
            merged[col] = merged[col].astype(str)

    merged["similarity"] = merged.apply(
        calculate_similarity, axis=1, meta=("similarity", "f8")
    )

    merged_df = merged.compute()
    avg = merged_df["similarity"].mean()
    logging.info(f"Average similarity: {avg:.2f}%")

    logging.info("Values comparison :")
    comparison_results = []
    mismatches = []

    for _, row in merged_df.iterrows():
        entry = {
            "id": row.name,
            "similarity": row["similarity"],
            "matches": {},
            "differences": {},
        }

        for col in merged_df.columns:
            if "_src1" in col and "_id" not in col:
                col_pair = col.replace("_src1", "")
                col1 = row[col]
                col2 = row.get(col.replace("_src1", "_src2"), None)

                similarity = levenshtein_similarity(col1, col2)

                if similarity >= 90:
                    entry["matches"][col_pair] = col1
                else:
                    entry["differences"][col_pair] = {
                        "src1": col1,
                        "src2": col2,
                        "similarity": f"{similarity:.2f}%",
                    }

        comparison_results.append(entry)

        if row["similarity"] < 100:
            mismatches.append(entry)

    logging.info(json.dumps(comparison_results, indent=4, ensure_ascii=False))

    # store_mismatched_products(mismatches)


if __name__ == "__main__":
    main()
