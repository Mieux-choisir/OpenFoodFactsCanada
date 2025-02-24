import json
import dask.dataframe as dd
import pandas as pd
from pymongo import MongoClient


def extract_data():
    client = MongoClient("mongodb://localhost:37017/")
    db = client["openfoodfacts"]
    
    collection = db["off_products"]
    df1 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))
    
    collection = db["fdc_products"]
    df2 = pd.DataFrame(list(collection.find({}, {"id_match": 1, "_id": 0})))

    return df1, df2


def main():
    df1, df2 = extract_data()

    ddf1 = dd.from_pandas(df1, npartitions=1)
    ddf2 = dd.from_pandas(df2, npartitions=1)

    ddf1 = ddf1.set_index("id_match")
    ddf2 = ddf2.set_index("id_match")

    merged = ddf1.join(ddf2, how="inner")

    matched_ids = merged.compute().index.tolist()

    print("IDs qui matchent entre les deux collections :")
    print(json.dumps(matched_ids, indent=4))

    print (f"{len(matched_ids)} produits matchés entre les deux collections.")


if __name__ == "__main__":
    main()
