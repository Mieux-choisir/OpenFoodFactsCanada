from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class NutritionFactsPerServing(ComplexField):
    """
    This is a class that stores data on the nutrition facts per serving of a product.

    Attributes:
        is_for_prepared_food (Optional[bool]): A boolean indication if the nutrition facts per serving are given for prepared food or not
        fat_serving (Optional[float]): The amount of fat (g) in one seving of the product
        saturated_fats_serving (Optional[float]): The amount of saturated fats (g) in one serving of the product
        trans_fats_serving (Optional[float]): The amount of trans fats (g) in one serving of the product
        cholesterol_serving (Optional[float]): The amount of cholesterol (g) in one serving of the product
        sodium_serving (Optional[float]): The amount of sodium (g) in one serving of the product
        carbohydrates_serving (Optional[float]): The amount of carbohydrates (g) in one serving of the product
        fibers_serving (Optional[float]): The amount of fibers (g) in one serving of the product
        sugar_serving (Optional[float]): The amount of sugar (g) in one serving of the product
        proteins_serving (Optional[float]): The amount of proteins (g) in one serving of the product
        calcium_serving (Optional[float]): The amount of calcium (g) in one serving of the product
        iron_serving (Optional[float]): The amount of iron (g) in one serving of the product
        energy_kcal_serving (Optional[float]): The amount of energy (kcal) in one serving of the product
        potassium_serving (Optional[float]): The amount of potassium (g) in one serving of the product
        added_sugar_serving (Optional[float]): The amount of added sugar (g) in one serving of the product
    """

    is_for_prepared_food: Optional[bool] = None
    fat_serving: Optional[float] = None
    saturated_fats_serving: Optional[float] = None
    trans_fats_serving: Optional[float] = None
    cholesterol_serving: Optional[float] = None
    sodium_serving: Optional[float] = None
    carbohydrates_serving: Optional[float] = None
    fibers_serving: Optional[float] = None
    sugar_serving: Optional[float] = None
    proteins_serving: Optional[float] = None
    calcium_serving: Optional[float] = None
    iron_serving: Optional[float] = None
    energy_kcal_serving: Optional[float] = None
    potassium_serving: Optional[float] = None
    added_sugar_serving: Optional[float] = None
