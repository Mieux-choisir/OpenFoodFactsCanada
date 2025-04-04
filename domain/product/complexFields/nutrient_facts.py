from typing import Optional

from domain.product.complexFields.nutritionFactsPerHundredGrams import (
    NutritionFactsPerHundredGrams,
)
from domain.product.complexFields.nutritionFactsPerServing import (
    NutritionFactsPerServing,
)
from domain.product.complexFields.complex_field import ComplexField


class NutritionFacts(ComplexField):
    nutrition_facts_per_hundred_grams: NutritionFactsPerHundredGrams = None
    nutrition_facts_per_serving: NutritionFactsPerServing = None
