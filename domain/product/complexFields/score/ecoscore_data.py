from typing import Optional, List, Dict

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients_origins import IngredientsOrigins
from domain.product.complexFields.packaging import Packaging
from domain.product.complexFields.production_system import ProductionSystem


class EcoscoreData(ComplexField):
    score: Optional[int] = None
    ingredients_origins: IngredientsOrigins = None
    packaging: Optional[Packaging] = None
    production_system: Optional[ProductionSystem] = None
    threatened_species: Dict = {}
