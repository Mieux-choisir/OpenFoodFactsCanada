from typing import Optional

from domain.product.complexFields.complex_field import ComplexField


class IngredientsOrigin(ComplexField):
    origin: Optional[str] = None
    percent: Optional[int] = None
    transportation_score: Optional[str] = None
