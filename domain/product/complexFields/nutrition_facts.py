from typing import Optional, Dict, Any
from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.nutrition_facts_per_hundred_grams import (
    NutritionFactsPerHundredGrams,
)
from domain.product.complexFields.nutrition_facts_per_serving import (
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
        """Creates a NutritionFacts object from a data dictionary"""
        if not data:
            return cls()
        hundred_grams_data = data.get("nutrition_facts_per_hundred_grams")
        serving_data = data.get("nutrition_facts_per_serving")
        return cls(
            nutrition_facts_per_hundred_grams=(
                NutritionFactsPerHundredGrams.from_dict(hundred_grams_data)
                if hundred_grams_data
                else None
            ),
            nutrition_facts_per_serving=(
                NutritionFactsPerServing.from_dict(serving_data)
                if serving_data
                else None
            ),
        )
