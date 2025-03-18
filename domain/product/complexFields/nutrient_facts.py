from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.nutrient_level import NutrientLevel
from domain.product.complexFields.nutrients import Nutrients


class NutritionFacts(ComplexField):
    nutrient_level: NutrientLevel = NutrientLevel()
    nutrients: Nutrients = Nutrients()
