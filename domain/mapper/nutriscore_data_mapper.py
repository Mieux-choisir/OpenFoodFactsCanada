from domain.mapper.number_mapper import NumberMapper
from domain.product.complexFields.score.nutriscore_data import NutriscoreData


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
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == energy_id
                ),
                None,
            ),
            fibers=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == fibers_id
                ),
                None,
            ),
            fruit_percentage=None,
            proteins=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == proteins_id
                ),
                None,
            ),
            saturated_fats=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == saturated_fats_id
                ),
                None,
            ),
            sodium=next(
                (
                    item["nutrient"]["number"]
                    for item in food_nutrients
                    if item["nutrient"]["id"] == sodium_id
                ),
                None,
            ),
            sugar=next(
                (
                    item["nutrient"]["number"]
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
        nutriscore_score_field = header.index("nutriscore_grade")
        energy_field = header.index("energy_100g")
        fibers_field = header.index("fiber_100g")
        fruit_percentage_field = header.index("fruits-vegetables-nuts_100g")
        proteins_field = header.index("proteins_100g")
        saturated_fats_field = header.index("saturated-fat_100g")
        sodium_field = header.index("sodium_100g")
        sugar_field = header.index("sugars_100g")

        return NutriscoreData(
            score=(
                self.number_mapper.map_letter_to_number(row[nutriscore_score_field])
                if row[nutriscore_score_field]
                else None
            ),
            energy=self.__get_float_value(row[energy_field]),
            fibers=self.__get_float_value(row[fibers_field]),
            fruit_percentage=self.__get_float_value(row[fruit_percentage_field]),
            proteins=self.__get_float_value(row[proteins_field]),
            saturated_fats=self.__get_float_value(row[saturated_fats_field]),
            sodium=self.__get_float_value(row[sodium_field]),
            sugar=self.__get_float_value(row[sugar_field]),
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
            energy=self.__get_float_value(product_dict[nutrients_field][energy_field]),
            fibers=self.__get_float_value(product_dict[nutrients_field][fibers_field]),
            fruit_percentage=self.__get_float_value(product_dict[nutrients_field][fruit_percentage_field]),
            proteins=self.__get_float_value(product_dict[nutrients_field][proteins_field]),
            saturated_fats=self.__get_float_value(product_dict[nutrients_field][saturated_fats_field]),
            sodium=self.__get_float_value(product_dict[nutrients_field][sodium_field]),
            sugar=self.__get_float_value(product_dict[nutrients_field][sugar_field]),
            is_beverage=None,
        )

    @staticmethod
    def __get_float_value(given_value):
        value = None
        if given_value is not None:
            try:
                value = float(given_value)
            except ValueError:
                pass
        return value
