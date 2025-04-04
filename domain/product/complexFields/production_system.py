from typing import List, Optional

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
