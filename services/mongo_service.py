from pymongo import MongoClient

class MongoService:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:37017/")
        self.db = self.client["openfoodfacts"]
        self.off_collection = self.db["matched_off_products"]
        self.fdc_collection = self.db["matched_fdc_products"]
        self.merged_collection = self.db["merged_products"]

    def get_next_matching_product(self):
        """Récupère un produit ayant un match entre OFF et FDC."""
        off_product = self.off_collection.find_one()
        if not off_product:
            return None  # Aucun produit restant

        id_match = off_product["id_match"]
        fdc_product = self.fdc_collection.find_one({"id_match": id_match})

        if not fdc_product:
            return None  # Erreur : pas de produit correspondant en FDC

        return {
            "id_match": id_match,
            "off_name": off_product.get("product_name", ""),
            "fdc_name": fdc_product.get("product_name", ""),
            "off_brand_name": off_product.get("brand_name", ""),
            "fdc_brand_name": off_product.get("brand_name", ""),
            "off_ingredients": off_product.get("ingredients", {}).get("ingredients_text", ""),
            "fdc_ingredients": fdc_product.get("ingredients", {}).get("ingredients_text", ""),
            "off_calories": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_100g", ""), # À retirer
            "fdc_calories": fdc_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_100g", ""), # À retirer
            "off_nutrients_energy_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_100g", ""),
            "off_nutrients_carbohydrates_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("carbohydrates_100g", ""),
            "off_nutrients_energy_kcal_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_kcal_100g", ""),
            "off_nutrients_vitamin_a_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("vitamin_a_100g", ""),
            "fdc_nutrients_energy_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_100g",""),
            "fdc_nutrients_carbohydrates_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("carbohydrates_100g", ""),
            "fdc_nutrients_energy_kcal_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("energy_kcal_100g", ""),
            "fdc_nutrients_vitamin_a_100g": off_product.get("nutrition_facts", {}).get("nutrients", {}).get("vitamin_a_100g", ""),
        }
