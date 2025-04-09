from typing import Optional
from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.nutritionFactsPerHundredGrams import (
    NutritionFactsPerHundredGrams,
)
from domain.product.complexFields.nutritionFactsPerServing import (
    NutritionFactsPerServing,
)


class NutritionFacts(ComplexField):
    """
    This is a class that stores data on the nutrition facts of a product.

    Attributes:
        nutrition_facts_per_hundred_grams (Optional[NutritionFactsPerHundredGrams]): The nutrition facts on the product for 100 grams
        nutrition_facts_per_serving (Optional[NutritionFactsPerServing]): The nutrition facts on the product for a serving
    """

    nutrition_facts_per_hundred_grams: Optional[NutritionFactsPerHundredGrams] = None
    nutrition_facts_per_serving: Optional[NutritionFactsPerServing] = None
