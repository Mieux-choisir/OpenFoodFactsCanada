from typing import Optional, Dict, List

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
