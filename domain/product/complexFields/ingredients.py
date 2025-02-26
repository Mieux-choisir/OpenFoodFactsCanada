from typing import Optional, List

from domain.product.complexFields.complex_field import ComplexField


class Ingredients(ComplexField):
    ingredients_text: Optional[str] = None
    ingredients_list: List[str] = []
