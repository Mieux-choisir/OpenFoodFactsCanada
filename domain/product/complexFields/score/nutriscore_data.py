from typing import Optional, Dict, Any

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

    energy_kcal_100g: Optional[float] = None
    fibers_100g: Optional[float] = None
    proteins_100g: Optional[float] = None
    saturated_fats_100g: Optional[float] = None
    sodium_100g: Optional[float] = None
    sugar_100g: Optional[float] = None
    fruit_percentage: Optional[float] = None
    is_beverage: Optional[bool] = False
    score: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NutriscoreData":
        if not data:
            return cls()
        return cls(
            energy_kcal_100g=data.get("energy_kcal_100g"),
            fibers_100g=data.get("fibers_100g"),
            proteins_100g=data.get("proteins_100g"),
            saturated_fats_100g=data.get("saturated_fats_100g"),
            sodium_100g=data.get("sodium_100g"),
            sugar_100g=data.get("sugar_100g"),
            fruit_percentage=data.get("fruit_percentage"),
            is_beverage=data.get("is_beverage", False),
            score=data.get("score"),
        )
