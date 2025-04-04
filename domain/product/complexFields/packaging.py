from typing import Optional, List

from domain.product.complexFields.complex_field import ComplexField


class Packaging(ComplexField):
    """
    This is a class that stores data on the packaging of a product.

    Attributes:
        non_recyclable_and_non_biodegradable_materials (Optional[int]): The number of non-recyclable or non-biodegradable materials
        packaging (list): Information about the packaging of the product
    """

    non_recyclable_and_non_biodegradable_materials: Optional[int] = None
    packaging: List = []
