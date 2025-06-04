from typing import Optional, List, Dict, Any

from domain.product.complexFields.complex_field import ComplexField


class Ingredients(ComplexField):
    ingredients_text: Optional[str] = None
    ingredients_list: List[str] = []

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Ingredients":
        """Creates an Ingredients object from a data dictionary"""
        if not data:
            return cls()
        return cls(
            ingredients_text=data.get("ingredients_text"),
            ingredients_list=data.get("ingredients_list", []),
        )
