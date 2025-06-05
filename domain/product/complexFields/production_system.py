from typing import List, Optional, Dict, Any

from domain.product.complexFields.complex_field import ComplexField


class ProductionSystem(ComplexField):
    """
    This is a class that stores data on the production system of a product.

    Attributes:
        labels (list): List of the labels on the products
        value (Optional[int])
        warning (Optional[str])
    """

    labels: List = []
    value: Optional[int] = None
    warning: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductionSystem":
        """Creates a ProductionSystem object from a data dictionary"""
        if not data:
            return cls()
        return cls(
            labels=data.get("labels", []),
            value=data.get("value"),
            warning=data.get("warning"),
        )
