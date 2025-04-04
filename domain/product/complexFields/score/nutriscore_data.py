from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class NutriscoreData(ComplexField):
    """
    This is a class that stores data on the NutriScore of a product.

    Attributes:
        energy_100g (Optional[float]): The amount of energy (kJ) in 100g of the product
        proteins_100g (Optional[float]): The amount of proteins (g) in 100g of the product
        saturated_fats_100g (Optional[float]): The amount of saturated fats (g) in 100g of the product
        sodium_100g (Optional[float]): The amount of sodium (g) in 100g of the product
        sugar_100g (Optional[float]): The amount of sugar (g) in 100g of the product
        fruit_percentage (Optional[float]): The percentage of fruits in the product
        is_beverage (Optional[bool]: A boolean indicating if the product is a beverage
        score (Optional[int]: The NutriScore
    """

    energy_100g: Optional[float] = None
    fibers_100g: Optional[float] = None
    proteins_100g: Optional[float] = None
    saturated_fats_100g: Optional[float] = None
    sodium_100g: Optional[float] = None
    sugar_100g: Optional[float] = None
    fruit_percentage: Optional[float] = None
    is_beverage: Optional[bool] = False
    score: Optional[int] = None
