from typing import Optional

from scripts.product.complexFields.complex_field import ComplexField


class NutrientLevel(ComplexField):
    fat: Optional[float] = None
    salt: Optional[float] = None
    saturated_fats: Optional[float] = None
    sugar: Optional[float] = None
