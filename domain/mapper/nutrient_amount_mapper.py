from decimal import Decimal


class NutrientMapper:
    def __init__(self):
        self.required_nutrients_units = {"carbohydrates": "g", "fat": "g", "salt": "g",
                                         "saturated_fats": "g", "sugar": "g", "vitamin_a": "mcg"}
        self.unit_conversions_to_g = {"mcg": 1000000, "mg": 1000, "cg": 100, "dg": 10}
        self.vitamin_unit_conversions_to_mcg = {"iu": Decimal("3.33")}

    def map_nutrient(self, nutrient_name, nutrient_value, nutrient_unit):
        converted_value = nutrient_value

        if nutrient_name in self.required_nutrients_units.keys() and nutrient_unit != self.required_nutrients_units[nutrient_name]:
            if nutrient_unit in self.unit_conversions_to_g.keys():
                converted_value = nutrient_value / self.unit_conversions_to_g[nutrient_unit]
            elif nutrient_unit in self.vitamin_unit_conversions_to_mcg.keys():
                converted_value = nutrient_value / self.vitamin_unit_conversions_to_mcg[nutrient_unit]
            else:
                converted_value = None

        return converted_value
