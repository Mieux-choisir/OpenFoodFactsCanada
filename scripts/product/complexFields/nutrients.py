from typing import Optional

from scripts.product.complexFields.complex_field import ComplexField


class Nutrients(ComplexField):
    carbohydrates_100g: Optional[float] = None
    energy_100g: Optional[float] = None
    energy_kcal_100g: Optional[float] = None
    vitamin_a_100g: Optional[float] = None
