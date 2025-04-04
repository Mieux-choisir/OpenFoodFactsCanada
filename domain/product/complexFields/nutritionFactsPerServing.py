from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class NutritionFactsPerServing(ComplexField):
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
    calories_serving: Optional[float] = None
    potassium_serving: Optional[float] = None
    added_sugar_serving: Optional[float] = None
