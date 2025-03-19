from decimal import Decimal


class NutrientAmountMapper:
    def __init__(self):
        self.required_nutrients_units = {
            "carbohydrates_100g": "g",
            "fat_100g": "g",
            "salt_100g": "g",
            "saturated_fats_100g": "g",
            "sugar_100g": "g",
            "vitamin_a_100g": "mcg",
            "sodium_100g": "g",
            "proteins_100g": "g",
            "fiber_100g": "g",
            "monounsaturated_fat_100g": "g",
            "polyunsaturated_fat_100g": "g",
            "trans_fat_100g": "g",
            "cholesterol_100g": "mg",
            "calcium_100g": "mg",
            "iron_100g": "mg",
            "potassium_100g": "mg",
            "vitamin_b1_100g": "mg",
            "vitamin_b2_100g": "mg",
            "vitamin_b6_100g": "mg",
            "vitamin_b9_100g": "mcg",
            "vitamin_b12_100g": "mcg",
            "vitamin_c_100g": "mg",
            "vitamin_pp_100g": "mg",
            "phosphorus_100g": "mg",
            "magnesium_100g": "mg",
            "zinc_100g": "mg",
            "folates_100g": "mcg",
            "pantothenic_acid_100g": "mg",
            "soluble_fiber_100g": "g",
            "insoluble_fiber_100g": "g",
            "copper_100g": "mg",
            "manganese_100g": "mg",
            "polyols_100g": "g",
            "selenium_100g": "mcg",
            "phylloguinone_100g": "g",
            "iodine_100g": "mcg",
            "biotin_100g": "mcg",
            "caffeine_100g": "mg",
            "molibdenum_100g": "mcg",
            "chromium_100g": "mcg",
        }
        self.unit_conversions_to_g = {"mcg": 1000000, "mg": 1000, "cg": 100, "dg": 10}
        self.vitamin_unit_conversions_to_mcg = {"iu": Decimal("3.33")}

    def map_nutrient(self, nutrient_name, nutrient_value, nutrient_unit):
        converted_value = nutrient_value

        if (
            nutrient_name in self.required_nutrients_units.keys()
            and nutrient_unit != self.required_nutrients_units[nutrient_name]
        ):
            if nutrient_unit in self.unit_conversions_to_g.keys():
                converted_value = (
                    nutrient_value / self.unit_conversions_to_g[nutrient_unit]
                )
            elif nutrient_unit in self.vitamin_unit_conversions_to_mcg.keys():
                converted_value = (
                    nutrient_value / self.vitamin_unit_conversions_to_mcg[nutrient_unit]
                )
            else:
                converted_value = None

        return converted_value
