from typing import Optional, Dict, Any

from domain.product.complexFields.complex_field import ComplexField


class IngredientsOrigins(ComplexField):
    """
    This is a class that stores data on the ingredients origins of a product.

    Attributes:
        origins (list[str]): A list of the origins of the ingredients
        percent (Optional[int]): The percent of the origins
        transportation_score (Optional[str]): The transportation score
    """

    origins: list[str] = []
    percent: Optional[int] = None
    transportation_score: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IngredientsOrigins":
        """Creates an IngredientsOrigins object from a data dictionary"""
        if not data:
            return cls()
        return cls(
            origins=data.get("origins", []),
            percent=data.get("percent"),
            transportation_score=data.get("transportation_score"),
        )
