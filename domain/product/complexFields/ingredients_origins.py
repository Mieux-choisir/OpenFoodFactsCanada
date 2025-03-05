from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class IngredientsOrigins(ComplexField):
    origins: list[str] = []
    percent: Optional[int] = None
    transportation_score: Optional[str] = None
