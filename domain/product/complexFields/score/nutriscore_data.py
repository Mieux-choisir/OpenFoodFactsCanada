from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class NutriscoreData(ComplexField):
    energy_100g: Optional[float] = None
    fibers_100g: Optional[float] = None
    proteins_100g: Optional[float] = None
    saturated_fats_100g: Optional[float] = None
    sodium_100g: Optional[float] = None
    sugar_100g: Optional[float] = None
    fruit_percentage: Optional[float] = 0.0
    is_beverage: Optional[bool] = False
    score: Optional[int] = None
