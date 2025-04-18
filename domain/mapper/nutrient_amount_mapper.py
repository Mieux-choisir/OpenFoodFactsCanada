from decimal import Decimal


class NutrientAmountMapper:
    """
    This is a class that maps products values to NutrientAmount objects.

    Attributes:
       unit_conversions_to_g (IngredientNormalizer)

    Methods:
       map_nutrient(nutrient_value, nutrient_unit): Maps the given nutrient value to its corresponding value in grams
    """

    def __init__(self):
        self.unit_conversions_to_g = {
            "mcg": 1000000,
            "mg": 1000,
            "cg": 100,
            "dg": 10,
            "iu": Decimal(3.33),
        }

    def map_nutrient(self, nutrient_value, nutrient_unit: str):
        """Maps the given nutrient value to its corresponding value in grams"""
        converted_value = None

        if nutrient_unit is not None and nutrient_unit.strip().lower() == "g":
            converted_value = nutrient_value
        elif (
            nutrient_unit is not None
            and nutrient_unit.lower() in self.unit_conversions_to_g.keys()
        ):
            converted_value = nutrient_value / self.unit_conversions_to_g[nutrient_unit]

        return converted_value
