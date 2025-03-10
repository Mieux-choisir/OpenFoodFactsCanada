from domain.mapper.number_mapper import NumberMapper
from domain.product.complexFields.score.nutriscore_data import NutriscoreData
from domain.utils.converter import Converter


class NutriscoreDataMapper:
    def __init__(self, number_mapper: NumberMapper):
        self.number_mapper = number_mapper

    @staticmethod
    def map_fdc_dict_to_nutriscore_data(food_nutrients: list[dict]) -> NutriscoreData:
        energy_id = 1008
        fibers_id = 1079
        proteins_id = 1003
        saturated_fats_id = 1258
        sodium_id = 1093
        sugar_id = 2000

        return NutriscoreData(
            score=None,
            energy=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == energy_id
                ),
                None,
            ),
            fibers=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == fibers_id
                ),
                None,
            ),
            fruit_percentage=None,
            proteins=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == proteins_id
                ),
                None,
            ),
            saturated_fats=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == saturated_fats_id
                ),
                None,
            ),
            sodium=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == sodium_id
                ),
                None,
            ),
            sugar=next(
                (
                    item["amount"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == sugar_id
                ),
                None,
            ),
            is_beverage=None,
        )

    def map_off_row_to_nutriscore_data(
        self, row: list[str], header: list[str]
    ) -> NutriscoreData:
        nutriscore_score_index = header.index("nutriscore_grade")
        energy_index = header.index("energy_100g")
        fibers_index = header.index("fiber_100g")
        fruit_percentage_index = header.index("fruits-vegetables-nuts_100g")
        proteins_index = header.index("proteins_100g")
        saturated_fats_index = header.index("saturated-fat_100g")
        sodium_index = header.index("sodium_100g")
        sugar_index = header.index("sugars_100g")

        return NutriscoreData(
            score=(
                self.number_mapper.map_letter_to_number(row[nutriscore_score_index])
                if row[nutriscore_score_index]
                else None
            ),
            energy=Converter.safe_float(row[energy_index]),
            fibers=row[fibers_index],
            fruit_percentage=(
                row[fruit_percentage_index]
                if fruit_percentage_index < len(row)
                else None
            ),
            proteins=row[proteins_index],
            saturated_fats=Converter.safe_float(row[saturated_fats_index]),
            sodium=row[sodium_index],
            sugar=row[sugar_index],
            is_beverage=None,
        )

    def map_off_dict_to_nutriscore_data(self, product_dict: dict) -> NutriscoreData:
        nutrients_field = "nutriments"
        nutriscore_score_field = "nutriscore_grade"
        energy_field = "energy_100g"
        fibers_field = "fiber_100g"
        fruit_percentage_field = "fruits-vegetables-nuts_100g"
        proteins_field = "proteins_100g"
        saturated_fats_field = "saturated-fat_100g"
        sodium_field = "sodium_100g"
        sugar_field = "sugars_100g"

        return NutriscoreData(
            score=(
                self.number_mapper.map_letter_to_number(
                    product_dict[nutriscore_score_field]
                )
                if product_dict[nutriscore_score_field]
                else None
            ),
            energy=product_dict[nutrients_field][energy_field],
            fibers=product_dict[nutrients_field][fibers_field],
            fruit_percentage=product_dict[nutrients_field][fruit_percentage_field],
            proteins=product_dict[nutrients_field][proteins_field],
            saturated_fats=product_dict[nutrients_field][saturated_fats_field],
            sodium=product_dict[nutrients_field][sodium_field],
            sugar=product_dict[nutrients_field][sugar_field],
            is_beverage=None,
        )
