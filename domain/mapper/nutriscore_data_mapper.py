from decimal import Decimal
from domain.mapper.number_mapper import NumberMapper
from domain.product.complexFields.score.nutriscore_data import NutriscoreData
from domain.utils.converter import Converter
from domain.mapper.nutrient_amount_mapper import NutrientAmountMapper


class NutriscoreDataMapper:
    """
    This is a class that maps products values to NutriscoreData objects.

    Attributes:
        number_mapper (NumberMapper)
        energy_kcal_to_kj (Decimal): The decimal value to convert energy value from kcal to kj

    Methods:
        map_fdc_dict_to_nutriscore_data(food_nutrients): Maps the given food_nutrients list to a NutriscoreData object
        map_off_dict_to_nutriscore_data(product_dict): Maps the given dictionary to a NutriscoreData object
    """

    def __init__(self, number_mapper: NumberMapper):
        self.number_mapper = number_mapper
        self.energy_kcal_to_kj = Decimal(4.1868)

    @staticmethod
    def map_fdc_dict_to_nutriscore_data(food_nutrients: list[dict]) -> NutriscoreData:
        """Maps the given food nutrients list of an FDC product to a NutriscoreData object"""
        nutrient_ids = {
            "fibers_100g": 1079,
            "proteins_100g": 1003,
            "saturated_fats_100g": 1258,
            "sodium_100g": 1093,
            "sugar_100g": 2000,
        }

        nutriscore_data = {
            "score": None,
            "fruit_percentage": None,
            "is_beverage": None,
        }

        energy_kcal = next(
            (
                item["amount"]
                for item in food_nutrients
                if item["nutrient"]["id"] == 1008
            ),
            None,
        )

        if energy_kcal is not None:
            nutriscore_data["energy_kcal_100g"] = float(energy_kcal)

        for field, nutrient_id in nutrient_ids.items():
            value = next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == nutrient_id
                ),
                None,
            )
            unit = next(
                (
                    item["nutrient"]["unitName"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == nutrient_id
                ),
                None,
            )

            nutriscore_data[field] = NutrientAmountMapper().map_nutrient(value, unit)

        return NutriscoreData(**nutriscore_data)

    def map_off_dict_to_nutriscore_data(self, product_dict: dict) -> NutriscoreData:
        """Maps the values in a given OFF (jsonl) product to a NutriscoreData object"""
        nutrients_field = "nutriments"
        nutriscore_score_field = "nutriscore_grade"
        energy_field = "energy-kcal_100g"
        fibers_field = "fiber_100g"
        fruit_percentage_field = "fruits-vegetables-nuts_100g"
        proteins_field = "proteins_100g"
        saturated_fats_field = "saturated-fat_100g"
        sodium_field = "sodium_100g"
        sugar_field = "sugars_100g"

        return NutriscoreData(
            score=(
                self.number_mapper.map_letter_to_number(
                    product_dict.get(nutriscore_score_field)
                )
                if product_dict.get(nutriscore_score_field)
                else None
            ),
            energy_kcal_100g=product_dict.get(nutrients_field, {}).get(energy_field),
            fibers_100g=(
                Converter.safe_float(
                    product_dict.get(nutrients_field, {}).get(fibers_field)
                )
                if product_dict.get(nutrients_field, {}).get(fibers_field) is not None
                else None
            ),
            fruit_percentage=(
                Converter.safe_float(
                    product_dict.get(nutrients_field, {}).get(fruit_percentage_field)
                )
                if product_dict.get(nutrients_field, {}).get(fruit_percentage_field)
                is not None
                else None
            ),
            proteins_100g=product_dict.get(nutrients_field, {}).get(proteins_field),
            saturated_fats_100g=product_dict.get(nutrients_field, {}).get(
                saturated_fats_field
            ),
            sodium_100g=product_dict.get(nutrients_field, {}).get(sodium_field),
            sugar_100g=product_dict.get(nutrients_field, {}).get(sugar_field),
            is_beverage=None,
        )
