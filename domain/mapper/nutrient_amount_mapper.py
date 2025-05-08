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
        }

    def map_nutrient(self, nutrient_value, nutrient_unit: str):
        """Maps the given nutrient value to its corresponding value in grams"""
        if nutrient_value is None or nutrient_unit is None:
            return None

        converted_value = None
        nutrient_unit = nutrient_unit.strip().lower()

        if nutrient_unit == "g":
            converted_value = nutrient_value
        elif nutrient_unit == "iu":
            converted_value = (
                Decimal(nutrient_value) * Decimal("0.3") / Decimal("1000000")
            )
        elif nutrient_unit in self.unit_conversions_to_g:
            converted_value = (
                Decimal(nutrient_value) / self.unit_conversions_to_g[nutrient_unit]
            )

        return float(converted_value) if converted_value is not None else None
