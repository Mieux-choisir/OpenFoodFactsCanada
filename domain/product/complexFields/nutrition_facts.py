from typing import Optional, Dict, Any
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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NutritionFacts":
        if not data:
            return cls()
        nhg_data = data.get("nutrition_facts_per_hundred_grams")
        nserving_data = data.get("nutrition_facts_per_serving")
        return cls(
            nutrition_facts_per_hundred_grams=(
                NutritionFactsPerHundredGrams.from_dict(nhg_data) if nhg_data else None
            ),
            nutrition_facts_per_serving=(
                NutritionFactsPerServing.from_dict(nserving_data) if nserving_data else None
            ),
        )
