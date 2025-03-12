from pymongo import MongoClient

class MongoService:
    def __init__(self, uri="mongodb://localhost:37017/", db_name="openfoodfacts"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_all_products(self, collection_name):
        collection = self.db[collection_name]
        return list(collection.find({}, {"_id": 0}))

    def save_merged_product(self, merged_product):
        collection = self.db["merged_products"]
        collection.insert_one(merged_product)

    def get_paginated_products(self, collection_name, start, length, search, order_column, order_dir):
        """Récupère une page de produits avec filtre et tri."""
        collection = self.db[collection_name]

        # Colonnes disponibles (doivent correspondre à celles du DataTable)
        columns = ["id_match", "id_original", "product_name", "brand_name", "category_en"]

        # Appliquer la recherche si un terme est fourni
        query = {}
        if search:
            query = {"$or": [{col: {"$regex": search, "$options": "i"}} for col in columns]}

        # Trier les résultats
        sort_order = 1 if order_dir == "asc" else -1
        sort_by = columns[order_column] if order_column < len(columns) else "id_match"

        # Récupérer les données paginées
        total_records = collection.count_documents({})
        filtered_records = collection.count_documents(query)
        products = list(
            collection.find(query, {"_id": 0})  # Exclure `_id` pour éviter erreurs JSON
            .sort(sort_by, sort_order)
            .skip(start)
            .limit(length)
        )

        return {
            "draw": 1,  # Doit être retourné tel quel pour Datatables
            "recordsTotal": total_records,
            "recordsFiltered": filtered_records,
            "data": products
        }