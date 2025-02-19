from typing import List, Optional

from scripts.product.complexFields.complex_field import ComplexField


class ProductionSystem(ComplexField):
    labels: List = []
    value: Optional[int] = None
    warning: Optional[str] = None
