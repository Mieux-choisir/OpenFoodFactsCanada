from typing import Optional, List, Dict

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients_origin import IngredientsOrigin
from domain.product.complexFields.packaging import Packaging
from domain.product.complexFields.production_system import ProductionSystem


class EcoscoreData(ComplexField):
    score: Optional[int] = None
    origin_of_ingredients: List[IngredientsOrigin] = []
    packaging: Optional[Packaging] = None
    production_system: Optional[ProductionSystem] = None
    threatened_species: Dict = {}
