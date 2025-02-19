from typing import Optional, Dict, List

from domain.product.complexFields.complex_field import ComplexField


class NovaData(ComplexField):
    score: Optional[int] = None
    group_markers: Dict[str, List] = {}
