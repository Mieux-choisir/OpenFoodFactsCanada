from pymongo import MongoClient

class MongoService:
    """Service pour interagir avec MongoDB"""

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:37017/")
        self.db = self.client["openfoodfacts"]
        self.off_collection = self.db["matched_off_products"]
        self.fdc_collection = self.db["matched_fdc_products"]
        self.merged_collection = self.db["merged_products"]

    def get_matching_product_by_index(self, index):
        """Récupère un produit ayant un match entre OFF et FDC."""
        off_products = list(self.off_collection.find().skip(index).limit(1))
        if not off_products:
            return None

        off_product = off_products[0]
        id_match = off_product["id_match"]
        fdc_product = self.fdc_collection.find_one({"id_match": id_match})

        if not fdc_product:
            return None

        def extract_nutrient(product, nutrient_key):
            """Récupère un nutriment spécifique si présent."""
            return product.get("nutrition_facts", {}).get("nutrients", {}).get(nutrient_key, "")

        return {
            "id_match": id_match,
            "off_name": off_product.get("product_name", ""),
            "fdc_name": fdc_product.get("product_name", ""),
            "off_brand_name": off_product.get("brand_name", ""),
            "fdc_brand_name": fdc_product.get("brand_name", ""),
            "off_ingredients": off_product.get("ingredients", {}).get("ingredients_text", ""),
            "fdc_ingredients": fdc_product.get("ingredients", {}).get("ingredients_text", ""),
            "off_nutrients_energy_100g": extract_nutrient(off_product, "energy_100g"),
            "off_nutrients_carbohydrates_100g": extract_nutrient(off_product, "carbohydrates_100g"),
            "off_nutrients_energy_kcal_100g": extract_nutrient(off_product, "energy_kcal_100g"),
            "off_nutrients_vitamin_a_100g": extract_nutrient(off_product, "vitamin_a_100g"),
            "fdc_nutrients_energy_100g": extract_nutrient(fdc_product, "energy_100g"),
            "fdc_nutrients_carbohydrates_100g": extract_nutrient(fdc_product, "carbohydrates_100g"),
            "fdc_nutrients_energy_kcal_100g": extract_nutrient(fdc_product, "energy_kcal_100g"),
            "fdc_nutrients_vitamin_a_100g": extract_nutrient(fdc_product, "vitamin_a_100g"),
        }