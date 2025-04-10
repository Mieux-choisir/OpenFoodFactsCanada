from typing import Optional, Dict

from domain.product.complexFields.complex_field import ComplexField
from domain.product.complexFields.ingredients_origins import IngredientsOrigins
from domain.product.complexFields.packaging import Packaging
from domain.product.complexFields.production_system import ProductionSystem


class EcoscoreData(ComplexField):
    """
    This is a class that stores data on the Ecoscore of a product.

    Attributes:
        score (Optional[int]): The ecoscore
        ingredients_origins (IngredientsOrigins): The ingredients origins
        packaging (Optional[Packaging]): Information about the packaging
        production_system (Optional[ProductionSystem]): Information about the production system
        threatened_species (dict): The threatened species
    """

    score: Optional[int] = None
    ingredients_origins: IngredientsOrigins = None
    packaging: Optional[Packaging] = None
    production_system: Optional[ProductionSystem] = None
    threatened_species: Dict = {}
