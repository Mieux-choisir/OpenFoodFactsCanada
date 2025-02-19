from scripts.product.complexFields.complex_field import ComplexField
from scripts.product.complexFields.nutrient_level import NutrientLevel
from scripts.product.complexFields.nutrients import Nutrients


class NutritionFacts(ComplexField):
    nutrient_level: NutrientLevel
    nutrients: Nutrients
