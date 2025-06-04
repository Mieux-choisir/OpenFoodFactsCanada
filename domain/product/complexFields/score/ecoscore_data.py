from typing import Optional, Dict, Any

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EcoscoreData":
        """Creates an EcoscoreData object from a data dictionary"""
        if not data:
            return cls()
        score = data.get("score")
        ingredients_origins_data = data.get("ingredients_origins")
        ingredients_origins = (
            IngredientsOrigins.from_dict(ingredients_origins_data)
            if ingredients_origins_data is not None
            else None
        )
        packaging_data = data.get("packaging")
        packaging = (
            Packaging.from_dict(packaging_data) if packaging_data is not None else None
        )
        production_system_data = data.get("production_system")
        production_system = (
            ProductionSystem.from_dict(production_system_data)
            if production_system_data is not None
            else None
        )
        threatened_species = data.get("threatened_species", {})
        return cls(
            score=score,
            ingredients_origins=ingredients_origins,
            packaging=packaging,
            production_system=production_system,
            threatened_species=threatened_species,
        )
