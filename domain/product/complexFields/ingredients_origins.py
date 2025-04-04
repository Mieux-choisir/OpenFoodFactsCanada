from typing import Optional

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
