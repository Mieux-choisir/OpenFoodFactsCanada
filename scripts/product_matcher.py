import pandas as pd
from pymongo import MongoClient

class ProductMatcher:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:37017/")
        self.db = self.client["openfoodfacts"]
        self.off_collection = self.db["off_products"]
        self.fdc_collection = self.db["fdc_products"]
        self.matched_off_collection = self.db["matched_off_products"]
        self.matched_fdc_collection = self.db["matched_fdc_products"]

    def find_matching_products(self):
        """Identifie les produits communs en fonction de id_match et stocke dans des collections séparées."""
        print("Recherche des produits avec un ID commun...")

        # Extraire les id_match
        df_off = pd.DataFrame(list(self.off_collection.find({}, {"id_match": 1, "_id": 0})))
        df_fdc = pd.DataFrame(list(self.fdc_collection.find({}, {"id_match": 1, "_id": 0})))

        if df_off.empty or df_fdc.empty:
            print("⚠ Aucune donnée trouvée dans l'une des collections.")
            return

        # Trouver les IDs en commun
        matched_ids = set(df_off["id_match"]).intersection(set(df_fdc["id_match"]))

        if not matched_ids:
            print("❌ Aucun produit commun trouvé.")
            return

        print(f"✅ {len(matched_ids)} produits communs trouvés !")

        # Supprimer les anciennes données
        self.matched_off_collection.delete_many({})
        self.matched_fdc_collection.delete_many({})

        # Insérer les produits matchés dans les nouvelles collections
        matched_off_products = list(self.off_collection.find({"id_match": {"$in": list(matched_ids)}}))
        matched_fdc_products = list(self.fdc_collection.find({"id_match": {"$in": list(matched_ids)}}))

        if matched_off_products:
            self.matched_off_collection.insert_many(matched_off_products)

        if matched_fdc_products:
            self.matched_fdc_collection.insert_many(matched_fdc_products)

        print("✅ Données matchées enregistrées avec succès !")


if __name__ == "__main__":
    matcher = ProductMatcher()
    matcher.find_matching_products()
