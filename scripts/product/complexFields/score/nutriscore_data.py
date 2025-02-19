from typing import Optional

from scripts.product.complexFields.complex_field import ComplexField


class NutriscoreData(ComplexField):
    energy: Optional[float] = None
    fibers: Optional[float] = None
    proteins: Optional[float] = None
    saturated_fats: Optional[float] = None
    sodium: Optional[float] = None
    sugar: Optional[float] = None
    fruit_percentage: Optional[float] = 0.0
    is_beverage: Optional[bool] = False
    score: Optional[int] = None