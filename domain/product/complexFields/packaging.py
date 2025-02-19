from typing import Optional, List

from domain.product.complexFields.complex_field import ComplexField


class Packaging(ComplexField):
    non_recyclable_and_non_biodegradable_materials: Optional[int] = None
    packaging: List = []