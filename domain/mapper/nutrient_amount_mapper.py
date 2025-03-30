from decimal import Decimal


class NutrientAmountMapper:
    def __init__(self):
        self.unit_conversions_to_g = {
            "mcg": 1000000,
            "mg": 1000,
            "cg": 100,
            "dg": 10,
            "iu": Decimal(3.33),
        }

    def map_nutrient(self, nutrient_value, nutrient_unit: str):
        converted_value = nutrient_value

        if nutrient_unit is not None and nutrient_unit.lower() != "g":
            converted_value = self.__map_nutrient_to_g(nutrient_value, nutrient_unit)

        return converted_value

    def __map_nutrient_to_g(self, nutrient_value, nutrient_unit):
        converted_value = None

        if nutrient_unit in self.unit_conversions_to_g.keys():
            converted_value = nutrient_value / self.unit_conversions_to_g[nutrient_unit]

        return converted_value
