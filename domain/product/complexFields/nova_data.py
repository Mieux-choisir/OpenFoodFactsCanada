from typing import Optional, Dict, List, Any

from domain.product.complexFields.complex_field import ComplexField


class NovaData(ComplexField):
    """
    This is a class that stores data on the Nova data of a product.

    Attributes:
        score (Optional[int]): The Nova group
        group_markers (dict): The group markers of the product
    """

    score: Optional[int] = None
    group_markers: Dict[str, List] = {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NovaData":
        if not data:
            return cls()
        return cls(
            score=data.get("score"),
            group_markers=data.get("group_markers", {}),
        )
